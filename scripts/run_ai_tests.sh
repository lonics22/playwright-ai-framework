#!/bin/bash
# 运行 AI 驱动测试脚本

echo "==================================="
echo "  运行 AI 驱动测试"
echo "==================================="

# 检查是否在项目根目录
if [ ! -f "pytest.ini" ]; then
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查环境变量
if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "警告: 未设置 OPENAI_API_KEY 或 ANTHROPIC_API_KEY"
    echo "AI 测试需要配置 LLM API 密钥"
    echo ""
    echo "请设置环境变量:"
    echo "  export OPENAI_API_KEY='your_key_here'"
    echo "  或"
    echo "  export ANTHROPIC_API_KEY='your_key_here'"
    echo ""
fi

# 默认参数
TEST_PATH="tests/ai_driven/"
LLM_PROVIDER="openai"
VERBOSE="-v"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --path)
            TEST_PATH="$2"
            shift 2
            ;;
        --llm)
            LLM_PROVIDER="$2"
            shift 2
            ;;
        --headless)
            export BROWSER=headless
            shift
            ;;
        --verbose)
            VERBOSE="-vv"
            shift
            ;;
        --help)
            echo "用法: ./run_ai_tests.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --path PATH       指定测试路径 (默认: tests/ai_driven/)"
            echo "  --llm PROVIDER    指定 LLM 提供商 (openai/anthropic/local)"
            echo "  --headless        无头模式运行"
            echo "  --verbose         详细输出"
            echo "  --help            显示帮助"
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            exit 1
            ;;
    esac
done

echo ""
echo "测试路径: $TEST_PATH"
echo "LLM 提供商: $LLM_PROVIDER"
echo ""

# 清理旧的测试结果
echo "清理旧的测试结果..."
rm -rf reports/allure-results/*
rm -rf reports/ai-insights/*

# 运行测试
echo "开始运行 AI 测试..."
pytest "$TEST_PATH" \
    $VERBOSE \
    -m ai \
    --llm="$LLM_PROVIDER" \
    --tb=short \
    --alluredir=reports/allure-results \
    --strict-markers

TEST_EXIT_CODE=$?

echo ""
echo "==================================="

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "  AI 测试通过!"
else
    echo "  AI 测试失败!"
fi

echo "==================================="
echo ""

# 生成报告
echo "生成报告..."

# Allure 报告
if command -v allure &> /dev/null; then
    allure generate reports/allure-results -o reports/allure-report --clean
    echo "Allure 报告已生成: reports/allure-report"
fi

# AI 洞察报告
if [ -f "reports/ai-insights/ai-insights-report.html" ]; then
    echo "AI 洞察报告: reports/ai-insights/ai-insights-report.html"
fi

echo ""
echo "运行 'allure open reports/allure-report' 查看详细报告"

exit $TEST_EXIT_CODE
