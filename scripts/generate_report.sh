#!/bin/bash
# 生成 Allure 测试报告脚本

echo "==================================="
echo "  生成 Allure 测试报告"
echo "==================================="

# 检查是否在项目根目录
if [ ! -d "reports/allure-results" ]; then
    echo "错误: 未找到测试结果 (reports/allure-results)"
    echo "请先运行测试: ./run_tests.sh"
    exit 1
fi

# 检查 Allure 是否安装
if ! command -v allure &> /dev/null; then
    echo "错误: 未找到 Allure 命令行工具"
    echo ""
    echo "安装方法:"
    echo "  Mac:    brew install allure"
    echo "  Linux:  sudo apt-add-repository ppa:qameta/allure"
    echo "          sudo apt-get update"
    echo "          sudo apt-get install allure"
    echo "  其他:   参考 https://docs.qameta.io/allure/"
    exit 1
fi

# 默认参数
OUTPUT_DIR="reports/allure-report"
SERVE=false
CLEAN=true

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --output)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --serve)
            SERVE=true
            shift
            ;;
        --no-clean)
            CLEAN=false
            shift
            ;;
        --help)
            echo "用法: ./generate_report.sh [选项]"
            echo ""
            echo "选项:"
            echo "  --output DIR      指定输出目录 (默认: reports/allure-report)"
            echo "  --serve           生成后启动报告服务器"
            echo "  --no-clean        不清除旧报告"
            echo "  --help            显示帮助"
            exit 0
            ;;
        *)
            echo "未知选项: $1"
            exit 1
            ;;
    esac
done

# 生成报告
echo ""
echo "生成 Allure 报告..."
echo "输入: reports/allure-results"
echo "输出: $OUTPUT_DIR"
echo ""

if [ "$CLEAN" = true ]; then
    GENERATE_CMD="allure generate reports/allure-results -o $OUTPUT_DIR --clean"
else
    GENERATE_CMD="allure generate reports/allure-results -o $OUTPUT_DIR"
fi

echo "执行: $GENERATE_CMD"
$GENERATE_CMD

if [ $? -ne 0 ]; then
    echo ""
    echo "错误: 生成报告失败"
    exit 1
fi

echo ""
echo "==================================="
echo "  报告生成成功!"
echo "==================================="
echo ""
echo "报告位置: $OUTPUT_DIR"
echo ""

# 启动报告服务器
if [ "$SERVE" = true ]; then
    echo "启动报告服务器..."
    echo "按 Ctrl+C 停止服务器"
    echo ""
    allure open "$OUTPUT_DIR"
else
    echo "查看报告:"
    echo "  1. 运行: allure open $OUTPUT_DIR"
    echo "  2. 或直接在浏览器打开: $OUTPUT_DIR/index.html"
fi

echo ""
