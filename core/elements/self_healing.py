"""自我修复定位策略"""
from typing import Optional, List, Dict, Any
from playwright.sync_api import Page, Locator
from playwright.async_api import Page as AsyncPage, Locator as AsyncLocator
import json


class SelfHealingLocator:
    """
    自我修复定位器
    当元素定位失败时，AI 自动寻找替代方案
    """

    def __init__(self, page: Page, ai_adapter=None):
        self.page = page
        self.ai = ai_adapter
        self.healing_history: List[Dict] = []

    def find_with_healing(
        self,
        failed_selector: str,
        element_description: str = None
    ) -> Optional[Locator]:
        """
        使用自我修复机制查找元素

        Args:
            failed_selector: 失败的选择器
            element_description: 元素描述（用于 AI 分析）

        Returns:
            Locator 或 None
        """
        # 1. 尝试常见的修复策略
        healed_locator = self._try_common_strategies(failed_selector)
        if healed_locator:
            self._record_healing(failed_selector, healed_locator, "common_strategy")
            return healed_locator

        # 2. 使用 AI 分析（如果可用）
        if self.ai and element_description:
            healed_locator = self._ai_healing(failed_selector, element_description)
            if healed_locator:
                self._record_healing(failed_selector, healed_locator, "ai_healing")
                return healed_locator

        return None

    def _try_common_strategies(self, selector: str) -> Optional[Locator]:
        """
        尝试常见的修复策略

        Args:
            selector: 原始选择器

        Returns:
            修复后的 Locator 或 None
        """
        strategies = [
            self._strategy_add_contains,
            self._strategy_partial_match,
            self._strategy_parent_child_swap,
            self._strategy_different_attribute,
        ]

        for strategy in strategies:
            try:
                new_selector = strategy(selector)
                if new_selector:
                    locator = self.page.locator(new_selector)
                    if locator.count() > 0:
                        return locator.first
            except Exception:
                continue

        return None

    def _strategy_add_contains(self, selector: str) -> Optional[str]:
        """策略1: 添加 contains 匹配"""
        if "[" in selector and "=" in selector:
            # 提取属性和值
            import re
            match = re.search(r'\[([^=]+)="([^"]+)"\]', selector)
            if match:
                attr, value = match.groups()
                base_selector = selector[:selector.find("[")]
                return f"{base_selector}:has([{attr}*='{value}'])"
        return None

    def _strategy_partial_match(self, selector: str) -> Optional[str]:
        """策略2: 使用部分匹配"""
        if "=" in selector and "[" in selector:
            return selector.replace('="', '*="')
        return None

    def _strategy_parent_child_swap(self, selector: str) -> Optional[str]:
        """策略3: 调整父子关系"""
        if ">" in selector:
            parts = selector.split(">")
            if len(parts) == 2:
                return f"{parts[0].strip()}:has(>{parts[1].strip()})"
        return None

    def _strategy_different_attribute(self, selector: str) -> Optional[str]:
        """策略4: 尝试不同属性"""
        attribute_mapping = {
            "data-testid": "data-test-id",
            "data-test-id": "data-testid",
            "id": "name",
            "name": "id",
        }

        for old_attr, new_attr in attribute_mapping.items():
            if old_attr in selector:
                import re
                match = re.search(rf'{old_attr}="([^"]+)"', selector)
                if match:
                    value = match.group(1)
                    return selector.replace(f'{old_attr}="{value}"', f'{new_attr}="{value}"')
        return None

    def _ai_healing(
        self,
        failed_selector: str,
        element_description: str
    ) -> Optional[Locator]:
        """
        使用 AI 进行修复

        Args:
            failed_selector: 失败的选择器
            element_description: 元素描述

        Returns:
            修复后的 Locator 或 None
        """
        # TODO: 实现 AI 辅助修复
        # 1. 截图当前页面
        # 2. AI 分析寻找相似元素
        # 3. 返回新定位器
        return None

    def _record_healing(
        self,
        original_selector: str,
        healed_locator: Locator,
        healing_method: str
    ):
        """
        记录修复历史

        Args:
            original_selector: 原始选择器
            healed_locator: 修复后的定位器
            healing_method: 修复方法
        """
        self.healing_history.append({
            "original_selector": original_selector,
            "healed_selector": healed_locator,  # 注意：这里需要获取选择器字符串
            "method": healing_method,
            "timestamp": time.time(),
        })

    def get_healing_history(self) -> List[Dict]:
        """
        获取修复历史

        Returns:
            修复历史列表
        """
        return self.healing_history.copy()

    def generate_healing_report(self) -> str:
        """
        生成修复报告

        Returns:
            报告字符串
        """
        if not self.healing_history:
            return "No healing events recorded."

        report = ["=== Self-Healing Report ===", ""]

        method_counts = {}
        for record in self.healing_history:
            method = record["method"]
            method_counts[method] = method_counts.get(method, 0) + 1

        report.append("Healing Methods Used:")
        for method, count in method_counts.items():
            report.append(f"  - {method}: {count}")

        report.append("")
        report.append("Detailed Events:")
        for i, record in enumerate(self.healing_history, 1):
            report.append(f"{i}. {record['original_selector']} -> {record['method']}")

        return "\n".join(report)


class AsyncSelfHealingLocator:
    """异步自我修复定位器"""

    def __init__(self, page: AsyncPage, ai_adapter=None):
        self.page = page
        self.ai = ai_adapter
        self.healing_history: List[Dict] = []

    async def find_with_healing(
        self,
        failed_selector: str,
        element_description: str = None
    ) -> Optional[AsyncLocator]:
        """异步使用自我修复机制查找元素"""
        # 1. 尝试常见的修复策略
        healed_locator = await self._try_common_strategies(failed_selector)
        if healed_locator:
            self._record_healing(failed_selector, healed_locator, "common_strategy")
            return healed_locator

        # 2. 使用 AI 分析（如果可用）
        if self.ai and element_description:
            healed_locator = await self._ai_healing(failed_selector, element_description)
            if healed_locator:
                self._record_healing(failed_selector, healed_locator, "ai_healing")
                return healed_locator

        return None

    async def _try_common_strategies(self, selector: str) -> Optional[AsyncLocator]:
        """异步尝试常见的修复策略"""
        strategies = [
            self._strategy_add_contains,
            self._strategy_partial_match,
            self._strategy_parent_child_swap,
            self._strategy_different_attribute,
        ]

        for strategy in strategies:
            try:
                new_selector = strategy(selector)
                if new_selector:
                    locator = self.page.locator(new_selector)
                    count = await locator.count()
                    if count > 0:
                        return locator.first
            except Exception:
                continue

        return None

    def _strategy_add_contains(self, selector: str) -> Optional[str]:
        """策略1: 添加 contains 匹配"""
        if "[" in selector and "=" in selector:
            import re
            match = re.search(r'\[([^=]+)="([^"]+)"\]', selector)
            if match:
                attr, value = match.groups()
                base_selector = selector[:selector.find("[")]
                return f"{base_selector}:has([{attr}*='{value}'])"
        return None

    def _strategy_partial_match(self, selector: str) -> Optional[str]:
        """策略2: 使用部分匹配"""
        if "=" in selector and "[" in selector:
            return selector.replace('="', '*="')
        return None

    def _strategy_parent_child_swap(self, selector: str) -> Optional[str]:
        """策略3: 调整父子关系"""
        if ">" in selector:
            parts = selector.split(">")
            if len(parts) == 2:
                return f"{parts[0].strip()}:has(>{parts[1].strip()})"
        return None

    def _strategy_different_attribute(self, selector: str) -> Optional[str]:
        """策略4: 尝试不同属性"""
        attribute_mapping = {
            "data-testid": "data-test-id",
            "data-test-id": "data-testid",
            "id": "name",
            "name": "id",
        }

        for old_attr, new_attr in attribute_mapping.items():
            if old_attr in selector:
                import re
                match = re.search(rf'{old_attr}="([^"]+)"', selector)
                if match:
                    value = match.group(1)
                    return selector.replace(f'{old_attr}="{value}"', f'{new_attr}="{value}"')
        return None

    async def _ai_healing(
        self,
        failed_selector: str,
        element_description: str
    ) -> Optional[AsyncLocator]:
        """异步使用 AI 进行修复"""
        return None

    def _record_healing(
        self,
        original_selector: str,
        healed_locator: AsyncLocator,
        healing_method: str
    ):
        """记录修复历史"""
        self.healing_history.append({
            "original_selector": original_selector,
            "healed_selector": healed_locator,
            "method": healing_method,
            "timestamp": time.time(),
        })

    def get_healing_history(self) -> List[Dict]:
        """获取修复历史"""
        return self.healing_history.copy()


import time
