"""Playwright 基础驱动封装"""
from typing import Optional, Dict, Any
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from playwright.async_api import async_playwright, Browser as AsyncBrowser
from playwright.async_api import BrowserContext as AsyncBrowserContext, Page as AsyncPage
from config.settings import Settings


class PlaywrightDriver:
    """Playwright 同步驱动封装"""

    def __init__(self, browser_type: str = "chromium", **kwargs):
        self.browser_type = browser_type
        self.config = self._load_config(**kwargs)
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None

    def _load_config(self, **kwargs) -> Dict[str, Any]:
        """加载浏览器配置"""
        config = Settings.get_browser_config()
        browser_config = config.get(self.browser_type, {})
        # 允许传入的参数覆盖配置
        browser_config.update(kwargs)
        return browser_config

    def start(self) -> Page:
        """启动浏览器并返回页面实例"""
        self._playwright = sync_playwright().start()

        # 获取浏览器类型
        browser_launcher = getattr(self._playwright, self.browser_type)

        # 启动浏览器
        launch_options = {
            "headless": self.config.get("headless", False),
            "slow_mo": self.config.get("slow_mo", 0),
            "args": self.config.get("args", []),
        }

        if self.config.get("downloads_path"):
            launch_options["downloads_path"] = self.config.get("downloads_path")

        self._browser = browser_launcher.launch(**launch_options)

        # 创建上下文
        context_options = self._get_context_options()
        self._context = self._browser.new_context(**context_options)

        # 创建页面
        self._page = self._context.new_page()

        return self._page

    def _get_context_options(self) -> Dict[str, Any]:
        """获取上下文配置选项"""
        config = Settings.get_browser_config()
        context_config = config.get("context", {})

        options = {
            "viewport": self.config.get("viewport", {"width": 1920, "height": 1080}),
            "locale": context_config.get("locale", "zh-CN"),
            "timezone_id": context_config.get("timezone_id", "Asia/Shanghai"),
        }

        if context_config.get("permissions"):
            options["permissions"] = context_config.get("permissions")

        if context_config.get("geolocation"):
            options["geolocation"] = context_config.get("geolocation")

        if context_config.get("color_scheme"):
            options["color_scheme"] = context_config.get("color_scheme")

        return options

    def stop(self):
        """关闭浏览器"""
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    @property
    def page(self) -> Page:
        """获取当前页面"""
        return self._page

    @property
    def browser(self) -> Browser:
        """获取浏览器实例"""
        return self._browser

    @property
    def context(self) -> BrowserContext:
        """获取上下文实例"""
        return self._context

    def take_screenshot(self, path: str = None):
        """截图"""
        if self._page:
            return self._page.screenshot(path=path)
        return None

    def wait_for_selector(self, selector: str, timeout: int = 30000):
        """等待元素出现"""
        if self._page:
            return self._page.wait_for_selector(selector, timeout=timeout)
        return None


class AsyncPlaywrightDriver:
    """Playwright 异步驱动封装"""

    def __init__(self, browser_type: str = "chromium", **kwargs):
        self.browser_type = browser_type
        self.config = self._load_config(**kwargs)
        self._playwright = None
        self._browser: Optional[AsyncBrowser] = None
        self._context: Optional[AsyncBrowserContext] = None
        self._page: Optional[AsyncPage] = None

    def _load_config(self, **kwargs) -> Dict[str, Any]:
        """加载浏览器配置"""
        config = Settings.get_browser_config()
        browser_config = config.get(self.browser_type, {})
        browser_config.update(kwargs)
        return browser_config

    async def start(self) -> AsyncPage:
        """异步启动浏览器"""
        self._playwright = await async_playwright().start()

        browser_launcher = getattr(self._playwright, self.browser_type)

        launch_options = {
            "headless": self.config.get("headless", False),
            "slow_mo": self.config.get("slow_mo", 0),
            "args": self.config.get("args", []),
        }

        if self.config.get("downloads_path"):
            launch_options["downloads_path"] = self.config.get("downloads_path")

        self._browser = await browser_launcher.launch(**launch_options)

        context_options = self._get_context_options()
        self._context = await self._browser.new_context(**context_options)

        self._page = await self._context.new_page()

        return self._page

    def _get_context_options(self) -> Dict[str, Any]:
        """获取上下文配置选项"""
        config = Settings.get_browser_config()
        context_config = config.get("context", {})

        options = {
            "viewport": self.config.get("viewport", {"width": 1920, "height": 1080}),
            "locale": context_config.get("locale", "zh-CN"),
            "timezone_id": context_config.get("timezone_id", "Asia/Shanghai"),
        }

        if context_config.get("permissions"):
            options["permissions"] = context_config.get("permissions")

        if context_config.get("geolocation"):
            options["geolocation"] = context_config.get("geolocation")

        if context_config.get("color_scheme"):
            options["color_scheme"] = context_config.get("color_scheme")

        return options

    async def stop(self):
        """异步关闭浏览器"""
        if self._context:
            await self._context.close()
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    @property
    def page(self) -> AsyncPage:
        """获取当前页面"""
        return self._page

    async def take_screenshot(self, path: str = None):
        """异步截图"""
        if self._page:
            return await self._page.screenshot(path=path)
        return None
