"""自定义 AI 工具"""
from typing import List, Dict, Any, Optional
from browser_use import tool


class CustomTools:
    """自定义 AI 工具集合"""

    @staticmethod
    @tool
    def verify_element_text(selector: str, expected: str, context) -> Dict[str, Any]:
        """
        验证元素文本内容

        Args:
            selector: CSS 选择器
            expected: 期望的文本内容
            context: 浏览器上下文

        Returns:
            验证结果
        """
        try:
            element = context.page.locator(selector)
            actual = element.text_content()
            success = actual.strip() == expected.strip()

            return {
                "success": success,
                "expected": expected,
                "actual": actual,
                "selector": selector
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "selector": selector
            }

    @staticmethod
    @tool
    def extract_table_data(table_selector: str, context) -> List[List[str]]:
        """
        提取表格数据

        Args:
            table_selector: 表格 CSS 选择器
            context: 浏览器上下文

        Returns:
            表格数据（二维列表）
        """
        try:
            rows = context.page.locator(f"{table_selector} tr").all()
            data = []
            for row in rows:
                cells = row.locator("td, th").all_text_contents()
                data.append(cells)
            return data
        except Exception as e:
            return [[f"Error: {str(e)}"]]

    @staticmethod
    @tool
    def get_element_attribute(selector: str, attribute: str, context) -> str:
        """
        获取元素属性值

        Args:
            selector: CSS 选择器
            attribute: 属性名
            context: 浏览器上下文

        Returns:
            属性值
        """
        try:
            element = context.page.locator(selector)
            return element.get_attribute(attribute) or ""
        except Exception as e:
            return f"Error: {str(e)}"

    @staticmethod
    @tool
    def count_elements(selector: str, context) -> int:
        """
        统计匹配元素数量

        Args:
            selector: CSS 选择器
            context: 浏览器上下文

        Returns:
            元素数量
        """
        try:
            return context.page.locator(selector).count()
        except Exception:
            return 0

    @staticmethod
    @tool
    def is_element_visible(selector: str, context) -> bool:
        """
        检查元素是否可见

        Args:
            selector: CSS 选择器
            context: 浏览器上下文

        Returns:
            是否可见
        """
        try:
            element = context.page.locator(selector)
            return element.is_visible()
        except Exception:
            return False

    @staticmethod
    @tool
    def wait_for_element(selector: str, timeout: int = 5000, context) -> Dict[str, Any]:
        """
        等待元素出现

        Args:
            selector: CSS 选择器
            timeout: 超时时间（毫秒）
            context: 浏览器上下文

        Returns:
            等待结果
        """
        try:
            element = context.page.locator(selector)
            element.wait_for(timeout=timeout)
            return {
                "success": True,
                "selector": selector,
                "found": True
            }
        except Exception as e:
            return {
                "success": False,
                "selector": selector,
                "found": False,
                "error": str(e)
            }

    @staticmethod
    @tool
    def scroll_to_element(selector: str, context) -> bool:
        """
        滚动到指定元素

        Args:
            selector: CSS 选择器
            context: 浏览器上下文

        Returns:
            是否成功
        """
        try:
            element = context.page.locator(selector)
            element.scroll_into_view_if_needed()
            return True
        except Exception:
            return False

    @staticmethod
    @tool
    def get_page_info(context) -> Dict[str, Any]:
        """
        获取页面信息

        Args:
            context: 浏览器上下文

        Returns:
            页面信息
        """
        page = context.page
        return {
            "url": page.url,
            "title": page.title(),
            "viewport": page.viewport_size,
        }

    @staticmethod
    @tool
    def take_screenshot(name: str = "screenshot", context) -> str:
        """
        截取屏幕截图

        Args:
            name: 截图名称
            context: 浏览器上下文

        Returns:
            截图保存路径
        """
        try:
            path = f"./screenshots/{name}.png"
            context.page.screenshot(path=path)
            return path
        except Exception as e:
            return f"Error: {str(e)}"


class ToolRegistry:
    """工具注册表"""

    _tools: Dict[str, Any] = {}

    @classmethod
    def register(cls, name: str, tool_func):
        """注册工具"""
        cls._tools[name] = tool_func

    @classmethod
    def get(cls, name: str) -> Optional[Any]:
        """获取工具"""
        return cls._tools.get(name)

    @classmethod
    def get_all(cls) -> List[Any]:
        """获取所有工具"""
        return list(cls._tools.values())

    @classmethod
    def get_all_names(cls) -> List[str]:
        """获取所有工具名称"""
        return list(cls._tools.keys())


# 注册默认工具
def register_default_tools():
    """注册默认工具到注册表"""
    ToolRegistry.register("verify_element_text", CustomTools.verify_element_text)
    ToolRegistry.register("extract_table_data", CustomTools.extract_table_data)
    ToolRegistry.register("get_element_attribute", CustomTools.get_element_attribute)
    ToolRegistry.register("count_elements", CustomTools.count_elements)
    ToolRegistry.register("is_element_visible", CustomTools.is_element_visible)
    ToolRegistry.register("wait_for_element", CustomTools.wait_for_element)
    ToolRegistry.register("scroll_to_element", CustomTools.scroll_to_element)
    ToolRegistry.register("get_page_info", CustomTools.get_page_info)
    ToolRegistry.register("take_screenshot", CustomTools.take_screenshot)
