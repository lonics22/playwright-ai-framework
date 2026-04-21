#!/bin/bash
# 运行传统自动化测试脚本

echo "==================================="
echo "  运行传统自动化测试"
echo "==================================="

# 检查是否在项目根目录
if [ ! -f "pytest.ini" ]; then
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 默认参数
TEST_PATH="tests/traditional/"
MARKERS=""
PARALLEL=""
VERBOSE="-v"

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --path)
            TEST_PATH="$2"
            shift 2
            ;;
        --markers)
            MARKERS="-m $2"
            shift 2
            ;;
        --parallel)
            PARALLEL="-n auto --dist=loadgroup"
            shift
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
            echo "用法: ./run_tests.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --path PATH       指定测试路径 (默认: tests/traditional/)"
            echo "  --markers MARKERS 指定 pytest markers"
            echo "  --parallel        启用并行执行"
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
echo "Markers: $MARKERS"
echo "并行: $PARALLEL"
echo ""

# 清理旧的测试结果
echo "清理旧的测试结果..."
rm -rf reports/allure-results/*

# 运行测试
echo "开始运行测试..."
pytest "$TEST_PATH" \
    $VERBOSE \
    $MARKERS \
    $PARALLEL \
    --tb=short \
    --alluredir=reports/allure-results \
    --strict-markers

TEST_EXIT_CODE=$?

echo ""
echo "==================================="

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "  测试通过!"
else
    echo "  测试失败!"
fi

echo "==================================="
echo ""

# 生成 Allure 报告
echo "生成 Allure 报告..."
if command -v allure &> /dev/null; then
    allure generate reports/allure-results -o reports/allure-report --clean
    echo "Allure 报告已生成: reports/allure-report"
    echo "运行 'allure open reports/allure-report' 查看报告"
else
    echo "提示: 安装 Allure 命令行工具以生成报告"
fi

exit $TEST_EXIT_CODE
