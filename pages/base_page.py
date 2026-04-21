"""基础页面对象"""
from typing import Optional, List
from playwright.sync_api import Page, Locator, expect
from core.elements.smart_locator import SmartLocator
from core.reporting.allure_helper import AllureHelper


class BasePage:
    """基础页面对象 - 传统操作封装"""

    def __init__(self, page: Page):
        self.page = page
        self.smart_locator = SmartLocator(page)
        self.url: Optional[str] = None
        self.title: Optional[str] = None

    def navigate_to(self, url: str = None):
        """
        导航到页面

        Args:
            url: 页面 URL，如果不提供则使用 self.url
        """
        target_url = url or self.url
        if not target_url:
            raise ValueError("URL must be provided either in constructor or navigate_to method")

        self.page.goto(target_url)
        return self

    def wait_for_page_load(self, timeout: int = 30000):
        """
        等待页面加载完成

        Args:
            timeout: 超时时间
        """
        self.page.wait_for_load_state("networkidle", timeout=timeout)
        return self

    def find(self, selector: str) -> Locator:
        """
        查找元素

        Args:
            selector: CSS 选择器

        Returns:
            Locator 对象
        """
        return self.smart_locator.find(selector)

    def find_all(self, selector: str) -> List[Locator]:
        """
        查找所有匹配元素

        Args:
            selector: CSS 选择器

        Returns:
            Locator 列表
        """
        return self.smart_locator.find_all(selector)

    def click(self, selector: str, timeout: int = 30000):
        """
        点击元素

        Args:
            selector: CSS 选择器
            timeout: 超时时间
        """
        with AllureHelper.step_context(f"点击元素: {selector}"):
            element = self.find(selector)
            element.click(timeout=timeout)
        return self

    def fill(self, selector: str, value: str, timeout: int = 30000):
        """
        填写输入框

        Args:
            selector: CSS 选择器
            value: 输入值
            timeout: 超时时间
        """
        with AllureHelper.step_context(f"填写 {selector} 为: {value}"):
            element = self.find(selector)
            element.fill(value, timeout=timeout)
        return self

    def clear(self, selector: str, timeout: int = 30000):
        """
        清空输入框

        Args:
            selector: CSS 选择器
            timeout: 超时时间
        """
        with AllureHelper.step_context(f"清空输入框: {selector}"):
            element = self.find(selector)
            element.clear(timeout=timeout)
        return self

    def get_text(self, selector: str) -> str:
        """
        获取元素文本

        Args:
            selector: CSS 选择器

        Returns:
            元素文本
        """
        element = self.find(selector)
        return element.text_content() or ""

    def get_attribute(self, selector: str, attribute: str) -> Optional[str]:
        """
        获取元素属性

        Args:
            selector: CSS 选择器
            attribute: 属性名

        Returns:
            属性值
        """
        element = self.find(selector)
        return element.get_attribute(attribute)

    def is_visible(self, selector: str) -> bool:
        """
        检查元素是否可见

        Args:
            selector: CSS 选择器

        Returns:
            是否可见
        """
        try:
            element = self.find(selector)
            return element.is_visible()
        except Exception:
            return False

    def is_enabled(self, selector: str) -> bool:
        """
        检查元素是否可用

        Args:
            selector: CSS 选择器

        Returns:
            是否可用
        """
        try:
            element = self.find(selector)
            return element.is_enabled()
        except Exception:
            return False

    def wait_for_element(self, selector: str, timeout: int = 30000):
        """
        等待元素出现

        Args:
            selector: CSS 选择器
            timeout: 超时时间
        """
        return self.smart_locator.wait_for_element(selector, timeout=timeout)

    def wait_for_element_visible(self, selector: str, timeout: int = 30000):
        """
        等待元素可见

        Args:
            selector: CSS 选择器
            timeout: 超时时间
        """
        element = self.find(selector)
        element.wait_for(state="visible", timeout=timeout)
        return self

    def wait_for_element_hidden(self, selector: str, timeout: int = 30000):
        """
        等待元素隐藏

        Args:
            selector: CSS 选择器
            timeout: 超时时间
        """
        element = self.find(selector)
        element.wait_for(state="hidden", timeout=timeout)
        return self

    def scroll_to_element(self, selector: str):
        """
        滚动到元素

        Args:
            selector: CSS 选择器
        """
        element = self.find(selector)
        element.scroll_into_view_if_needed()
        return self

    def select_option(self, selector: str, value: str):
        """
        选择下拉框选项

        Args:
            selector: CSS 选择器
            value: 选项值
        """
        element = self.find(selector)
        element.select_option(value)
        return self

    def upload_file(self, selector: str, file_path: str):
        """
        上传文件

        Args:
            selector: CSS 选择器
            file_path: 文件路径
        """
        element = self.find(selector)
        element.set_input_files(file_path)
        return self

    def take_screenshot(self, name: str = "screenshot"):
        """
        截图

        Args:
            name: 截图名称
        """
        AllureHelper.attach_screenshot(self.page, name)
        return self

    def assert_text_present(self, text: str, timeout: int = 5000):
        """
        断言页面包含指定文本

        Args:
            text: 期望文本
            timeout: 超时时间
        """
        expect(self.page.locator("body")).to_contain_text(text, timeout=timeout)
        return self

    def assert_element_present(self, selector: str):
        """
        断言元素存在

        Args:
            selector: CSS 选择器
        """
        expect(self.page.locator(selector)).to_be_visible()
        return self

    def get_page_title(self) -> str:
        """
        获取页面标题

        Returns:
            页面标题
        """
        return self.page.title()

    def get_page_url(self) -> str:
        """
        获取页面 URL

        Returns:
            页面 URL
        """
        return self.page.url

    def refresh(self):
        """刷新页面"""
        self.page.reload()
        return self

    def go_back(self):
        """返回上一页"""
        self.page.go_back()
        return self

    def go_forward(self):
        """前进"""
        self.page.go_forward()
        return self
