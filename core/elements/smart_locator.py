"""智能元素定位器 - 结合传统定位与 AI 视觉定位"""
import hashlib
from typing import List, Optional, Dict, Any
from playwright.sync_api import Page, Locator
from playwright.async_api import Page as AsyncPage, Locator as AsyncLocator


class ElementNotFoundException(Exception):
    """元素未找到异常"""
    pass


class SmartLocator:
    """智能元素定位器 - 结合传统定位与 AI 视觉定位"""

    def __init__(self, page: Page, ai_adapter=None):
        self.page = page
        self.ai = ai_adapter
        self.element_registry: Dict[str, Dict] = {}  # 元素历史定位缓存

    def find(
        self,
        selector: str,
        fallback_description: str = None,
        timeout: int = 30000
    ) -> Locator:
        """
        智能查找元素
        1. 优先使用传统选择器
        2. 失败时尝试备用选择器
        3. 启用 AI 时，使用 AI 视觉定位

        Args:
            selector: 主选择器
            fallback_description: 失败时的元素描述（用于 AI 定位）
            timeout: 超时时间

        Returns:
            Playwright Locator 对象
        """
        # 1. 尝试主选择器
        try:
            locator = self.page.locator(selector)
            locator.wait_for(timeout=min(timeout, 5000))
            if locator.count() > 0:
                return locator.first
        except Exception:
            pass

        # 2. 尝试备用选择器
        if selector in self.element_registry:
            selectors = self.element_registry[selector].get("selectors", [])
            for backup_selector in selectors:
                if backup_selector != selector:
                    try:
                        locator = self.page.locator(backup_selector)
                        locator.wait_for(timeout=min(timeout, 3000))
                        if locator.count() > 0:
                            # 更新最后成功的选择器
                            self.element_registry[selector]["last_success"] = backup_selector
                            return locator.first
                    except Exception:
                        continue

        # 3. 尝试 AI 视觉定位
        if fallback_description and self.ai:
            try:
                return self._ai_find(fallback_description)
            except Exception:
                pass

        raise ElementNotFoundException(f"无法定位元素: {selector}")

    def find_all(self, selector: str) -> List[Locator]:
        """
        查找所有匹配的元素

        Args:
            selector: CSS 选择器

        Returns:
            Locator 列表
        """
        return self.page.locator(selector).all()

    def _ai_find(self, description: str) -> Locator:
        """
        使用 AI 通过视觉描述定位元素

        Args:
            description: 元素视觉描述

        Returns:
            Playwright Locator
        """
        # TODO: 实现 AI 视觉定位
        # 1. 截图
        # 2. AI 分析获取坐标
        # 3. 转换为 Playwright Locator
        raise NotImplementedError("AI 视觉定位需要集成视觉模型")

    def register_element(self, name: str, selectors: List[str], checksum: str = None):
        """
        注册元素多维度特征，用于自我修复

        Args:
            name: 元素名称
            selectors: 多个选择器列表（优先级排序）
            checksum: 元素内容哈希
        """
        self.element_registry[name] = {
            "selectors": selectors,
            "checksum": checksum,
            "last_success": selectors[0] if selectors else None,
            "retry_count": 0,
        }

    def get_element_info(self, selector: str) -> Dict[str, Any]:
        """
        获取元素信息

        Args:
            selector: CSS 选择器

        Returns:
            元素信息字典
        """
        try:
            locator = self.page.locator(selector)
            return {
                "count": locator.count(),
                "visible": locator.is_visible() if locator.count() > 0 else False,
                "enabled": locator.is_enabled() if locator.count() > 0 else False,
                "text": locator.text_content() if locator.count() > 0 else "",
            }
        except Exception as e:
            return {"error": str(e)}

    def wait_for_element(
        self,
        selector: str,
        state: str = "visible",
        timeout: int = 30000
    ) -> Locator:
        """
        等待元素达到指定状态

        Args:
            selector: CSS 选择器
            state: 等待状态 (visible, hidden, attached, detached)
            timeout: 超时时间

        Returns:
            Locator 对象
        """
        locator = self.page.locator(selector)
        locator.wait_for(state=state, timeout=timeout)
        return locator

    def is_element_present(self, selector: str) -> bool:
        """
        检查元素是否存在

        Args:
            selector: CSS 选择器

        Returns:
            是否存在
        """
        try:
            count = self.page.locator(selector).count()
            return count > 0
        except Exception:
            return False


class AsyncSmartLocator:
    """异步智能元素定位器"""

    def __init__(self, page: AsyncPage, ai_adapter=None):
        self.page = page
        self.ai = ai_adapter
        self.element_registry: Dict[str, Dict] = {}

    async def find(
        self,
        selector: str,
        fallback_description: str = None,
        timeout: int = 30000
    ) -> AsyncLocator:
        """异步智能查找元素"""
        # 1. 尝试主选择器
        try:
            locator = self.page.locator(selector)
            await locator.wait_for(timeout=min(timeout, 5000))
            count = await locator.count()
            if count > 0:
                return locator.first
        except Exception:
            pass

        # 2. 尝试备用选择器
        if selector in self.element_registry:
            selectors = self.element_registry[selector].get("selectors", [])
            for backup_selector in selectors:
                if backup_selector != selector:
                    try:
                        locator = self.page.locator(backup_selector)
                        await locator.wait_for(timeout=min(timeout, 3000))
                        count = await locator.count()
                        if count > 0:
                            self.element_registry[selector]["last_success"] = backup_selector
                            return locator.first
                    except Exception:
                        continue

        # 3. 尝试 AI 视觉定位
        if fallback_description and self.ai:
            try:
                return await self._ai_find(fallback_description)
            except Exception:
                pass

        raise ElementNotFoundException(f"无法定位元素: {selector}")

    async def _ai_find(self, description: str) -> AsyncLocator:
        """异步 AI 视觉定位"""
        raise NotImplementedError("AI 视觉定位需要集成视觉模型")

    def register_element(self, name: str, selectors: List[str], checksum: str = None):
        """注册元素"""
        self.element_registry[name] = {
            "selectors": selectors,
            "checksum": checksum,
            "last_success": selectors[0] if selectors else None,
            "retry_count": 0,
        }

    async def is_element_present(self, selector: str) -> bool:
        """异步检查元素是否存在"""
        try:
            count = await self.page.locator(selector).count()
            return count > 0
        except Exception:
            return False


def calculate_checksum(text: str) -> str:
    """
    计算文本的 MD5 校验和

    Args:
        text: 文本内容

    Returns:
        MD5 哈希值
    """
    return hashlib.md5(text.encode("utf-8")).hexdigest()
