"""pytest 配置与 fixture"""
import pytest
import pytest_asyncio
import allure
from playwright.sync_api import sync_playwright
from playwright.async_api import async_playwright
from core.driver.browser_use_adapter import AIAgentAdapter
from core.reporting.allure_helper import AllureHelper
from core.reporting.ai_report_plugin import get_plugin
from config.settings import Settings


# ==================== Session Fixtures ====================

@pytest.fixture(scope="session")
def browser_config():
    """浏览器全局配置"""
    return Settings.get_browser_config()


@pytest.fixture(scope="session")
def env_config():
    """环境配置"""
    return Settings.get_env_config()


# ==================== Function Fixtures (Sync) ====================

@pytest.fixture(scope="function")
def page(browser_config):
    """
    每个测试的独立页面实例（同步）
    测试结束后自动截图（如果失败）并清理
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=browser_config.get("chromium", {}).get("headless", False),
            slow_mo=browser_config.get("chromium", {}).get("slow_mo", 0),
        )

        context = browser.new_context(
            viewport=browser_config.get("chromium", {}).get(
                "viewport", {"width": 1920, "height": 1080}
            )
        )

        page = context.new_page()

        yield page

        # 测试结束后的清理
        context.close()
        browser.close()


@pytest.fixture(scope="function")
def ai_agent(request, page):
    """
    AI Agent fixture - 按需初始化
    只有当测试标记了 @pytest.mark.ai 时才创建
    """
    marker = request.node.get_closest_marker("ai")
    if marker:
        provider = marker.kwargs.get("llm", "openai")
        adapter = AIAgentAdapter(
            llm_provider=provider,
            headless=False,
            use_vision=True,
        )
        yield adapter
        # 清理
        import asyncio
        asyncio.run(adapter.close())
    else:
        yield None


@pytest.fixture(scope="function")
def smart_page(page, ai_agent):
    """
    智能页面对象 - 自动选择传统或 AI 模式
    """
    from pages.ai_page import AIPage
    return AIPage(page, ai_agent)


@pytest.fixture(scope="function")
def base_page(page):
    """
    基础页面对象
    """
    from pages.base_page import BasePage
    return BasePage(page)


@pytest.fixture(scope="function")
def header_component(page):
    """
    头部组件
    """
    from pages.components.header import Header
    return Header(page)


@pytest.fixture(scope="function")
def footer_component(page):
    """
    底部组件
    """
    from pages.components.footer import Footer
    return Footer(page)


# ==================== Function Fixtures (Async) ====================

@pytest_asyncio.fixture(scope="function")
async def async_page(browser_config):
    """
    每个测试的独立页面实例（异步）
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=browser_config.get("chromium", {}).get("headless", False),
            slow_mo=browser_config.get("chromium", {}).get("slow_mo", 0),
        )

        context = await browser.new_context(
            viewport=browser_config.get("chromium", {}).get(
                "viewport", {"width": 1920, "height": 1080}
            )
        )

        page = await context.new_page()

        yield page

        await context.close()
        await browser.close()


@pytest_asyncio.fixture(scope="function")
async def async_ai_agent(request, async_page):
    """
    异步 AI Agent fixture
    """
    marker = request.node.get_closest_marker("ai")
    if marker:
        provider = marker.kwargs.get("llm", "openai")
        adapter = AIAgentAdapter(
            llm_provider=provider,
            headless=False,
            use_vision=True,
        )
        yield adapter
        await adapter.close()
    else:
        yield None


@pytest_asyncio.fixture(scope="function")
async def async_smart_page(async_page, async_ai_agent):
    """
    异步智能页面对象
    """
    from pages.ai_page import AIPage
    return AIPage(async_page, async_ai_agent)


# ==================== pytest Hooks ====================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    测试失败时自动附加截图和 AI 分析
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # 尝试获取 page fixture
        page = item.funcargs.get("page") or item.funcargs.get("async_page")

        if page:
            try:
                # 同步截图
                if hasattr(page, "screenshot"):
                    screenshot = page.screenshot()
                    allure.attach(
                        screenshot,
                        name="失败截图",
                        attachment_type=allure.attachment_type.PNG
                    )

                    # 附加页面源码
                    try:
                        html = page.content()
                        allure.attach(
                            html,
                            name="页面源码",
                            attachment_type=allure.attachment_type.HTML
                        )
                    except:
                        pass
            except Exception as e:
                allure.attach(
                    str(e),
                    name="截图失败原因",
                    attachment_type=allure.attachment_type.TEXT
                )

        # AI 失败分析（如测试标记了 ai）
        if item.get_closest_marker("ai"):
            try:
                error_message = str(report.longrepr) if report.longrepr else "Unknown error"
                allure.attach(
                    f"AI 失败分析功能需要在项目中集成 AI 分析模块\n\n错误信息: {error_message[:500]}",
                    name="AI 失败分析",
                    attachment_type=allure.attachment_type.TEXT
                )
            except:
                pass


def pytest_configure(config):
    """
    pytest 配置
    """
    # 注册自定义 marker
    config.addinivalue_line(
        "markers", "ai(llm=openai): 标记 AI 驱动测试（需要 LLM 配置）"
    )
    config.addinivalue_line(
        "markers", "hybrid: 标记混合模式测试"
    )
    config.addinivalue_line(
        "markers", "self_healing: 标记自我修复定位测试"
    )


def pytest_sessionfinish(session, exitstatus):
    """
    测试会话结束时生成 AI 洞察报告
    """
    try:
        plugin = get_plugin()
        if plugin.execution_records:
            json_path = plugin.save_report("ai-insights-report.json")
            html_path = plugin.generate_html_report("ai-insights-report.html")
            print(f"\n📊 AI 洞察报告已生成:")
            print(f"   JSON: {json_path}")
            print(f"   HTML: {html_path}")
    except Exception as e:
        print(f"生成 AI 洞察报告时出错: {e}")
