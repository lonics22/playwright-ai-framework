@echo off
REM 运行传统自动化测试脚本 (Windows)

echo ===================================
echo   运行传统自动化测试
echo ===================================

REM 检查是否在项目根目录
if not exist "pytest.ini" (
    echo 错误: 请在项目根目录运行此脚本
    exit /b 1
)

REM 默认参数
set TEST_PATH=tests\traditional\
set MARKERS=
set PARALLEL=
set VERBOSE=-v

REM 解析参数
:parse_args
if "%~1"=="" goto run_tests
if "%~1"=="--path" (
    set TEST_PATH=%~2
    shift
    shift
    goto parse_args
)
if "%~1"=="--markers" (
    set MARKERS=-m %~2
    shift
    shift
    goto parse_args
)
if "%~1"=="--parallel" (
    set PARALLEL=-n auto --dist=loadgroup
    shift
    goto parse_args
)
if "%~1"=="--headless" (
    set BROWSER=headless
    shift
    goto parse_args
)
if "%~1"=="--verbose" (
    set VERBOSE=-vv
    shift
    goto parse_args
)
if "%~1"=="--help" (
    echo 用法: run_tests.bat [选项]
    echo.
    echo 选项:
    echo   --path PATH       指定测试路径 (默认: tests\traditional\)
    echo   --markers MARKERS 指定 pytest markers
    echo   --parallel        启用并行执行
    echo   --headless        无头模式运行
    echo   --verbose         详细输出
    echo   --help            显示帮助
    exit /b 0
)
echo 未知选项: %~1
exit /b 1

:run_tests
echo.
echo 测试路径: %TEST_PATH%
echo Markers: %MARKERS%
echo 并行: %PARALLEL%
echo.

REM 清理旧的测试结果
echo 清理旧的测试结果...
if exist "reports\allure-results" rmdir /s /q "reports\allure-results"
mkdir "reports\allure-results"

REM 运行测试
echo 开始运行测试...
pytest "%TEST_PATH%" %VERBOSE% %MARKERS% %PARALLEL% --tb=short --alluredir=reports\allure-results --strict-markers

set TEST_EXIT_CODE=%ERRORLEVEL%

echo.
echo ===================================
if %TEST_EXIT_CODE%==0 (
    echo   测试通过!
) else (
    echo   测试失败!
)
echo ===================================
echo.

REM 生成 Allure 报告
echo 生成 Allure 报告...
where allure >nul 2>nul
if %ERRORLEVEL%==0 (
    allure generate reports\allure-results -o reports\allure-report --clean
    echo Allure 报告已生成: reports\allure-report
    echo 运行 'allure open reports\allure-report' 查看报告
) else (
    echo 提示: 安装 Allure 命令行工具以生成报告
)

exit /b %TEST_EXIT_CODE%
