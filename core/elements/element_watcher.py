"""元素变更监听"""
import time
from typing import Callable, Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
from playwright.sync_api import Page


class ChangeType(Enum):
    """变更类型"""
    TEXT_CHANGED = "text_changed"
    ATTRIBUTE_CHANGED = "attribute_changed"
    VISIBILITY_CHANGED = "visibility_changed"
    ADDED = "added"
    REMOVED = "removed"
    POSITION_CHANGED = "position_changed"


@dataclass
class ElementChange:
    """元素变更记录"""
    selector: str
    change_type: ChangeType
    old_value: Any
    new_value: Any
    timestamp: float


class ElementWatcher:
    """元素变更监听器"""

    def __init__(self, page: Page):
        self.page = page
        self._watched_elements: Dict[str, Dict] = {}
        self._callbacks: Dict[str, List[Callable]] = {}
        self._is_watching = False
        self._snapshot_interval = 1.0  # 秒

    def watch(
        self,
        selector: str,
        attributes: List[str] = None,
        callback: Callable = None
    ):
        """
        开始监听元素

        Args:
            selector: CSS 选择器
            attributes: 要监听的属性列表
            callback: 变更回调函数
        """
        self._watched_elements[selector] = {
            "attributes": attributes or ["text", "visible"],
            "last_snapshot": None,
        }

        if callback:
            if selector not in self._callbacks:
                self._callbacks[selector] = []
            self._callbacks[selector].append(callback)

        # 获取初始状态
        self._watched_elements[selector]["last_snapshot"] = self._take_snapshot(selector)

    def unwatch(self, selector: str):
        """
        停止监听元素

        Args:
            selector: CSS 选择器
        """
        if selector in self._watched_elements:
            del self._watched_elements[selector]
        if selector in self._callbacks:
            del self._callbacks[selector]

    def _take_snapshot(self, selector: str) -> Dict:
        """
        获取元素当前状态快照

        Args:
            selector: CSS 选择器

        Returns:
            状态快照
        """
        try:
            locator = self.page.locator(selector)
            count = locator.count()

            if count == 0:
                return {"exists": False}

            snapshot = {"exists": True}
            config = self._watched_elements.get(selector, {})
            attributes = config.get("attributes", [])

            if "text" in attributes:
                try:
                    snapshot["text"] = locator.text_content()
                except:
                    snapshot["text"] = ""

            if "visible" in attributes:
                try:
                    snapshot["visible"] = locator.is_visible()
                except:
                    snapshot["visible"] = False

            if "enabled" in attributes:
                try:
                    snapshot["enabled"] = locator.is_enabled()
                except:
                    snapshot["enabled"] = False

            # 获取自定义属性
            for attr in attributes:
                if attr not in ["text", "visible", "enabled"]:
                    try:
                        snapshot[f"attr_{attr}"] = locator.get_attribute(attr)
                    except:
                        snapshot[f"attr_{attr}"] = None

            return snapshot
        except Exception as e:
            return {"exists": False, "error": str(e)}

    def check_changes(self) -> List[ElementChange]:
        """
        检查所有监听元素的变化

        Returns:
            变更列表
        """
        changes = []
        current_time = time.time()

        for selector, config in self._watched_elements.items():
            current_snapshot = self._take_snapshot(selector)
            last_snapshot = config.get("last_snapshot", {})

            # 检查是否存在变化
            if current_snapshot.get("exists") != last_snapshot.get("exists"):
                if current_snapshot.get("exists"):
                    change = ElementChange(
                        selector=selector,
                        change_type=ChangeType.ADDED,
                        old_value=None,
                        new_value=current_snapshot,
                        timestamp=current_time
                    )
                else:
                    change = ElementChange(
                        selector=selector,
                        change_type=ChangeType.REMOVED,
                        old_value=last_snapshot,
                        new_value=None,
                        timestamp=current_time
                    )
                changes.append(change)
            elif current_snapshot.get("exists"):
                # 检查文本变化
                if current_snapshot.get("text") != last_snapshot.get("text"):
                    changes.append(ElementChange(
                        selector=selector,
                        change_type=ChangeType.TEXT_CHANGED,
                        old_value=last_snapshot.get("text"),
                        new_value=current_snapshot.get("text"),
                        timestamp=current_time
                    ))

                # 检查可见性变化
                if current_snapshot.get("visible") != last_snapshot.get("visible"):
                    changes.append(ElementChange(
                        selector=selector,
                        change_type=ChangeType.VISIBILITY_CHANGED,
                        old_value=last_snapshot.get("visible"),
                        new_value=current_snapshot.get("visible"),
                        timestamp=current_time
                    ))

            # 更新快照
            self._watched_elements[selector]["last_snapshot"] = current_snapshot

            # 触发回调
            for change in changes:
                if change.selector in self._callbacks:
                    for callback in self._callbacks[change.selector]:
                        callback(change)

        return changes

    def wait_for_change(
        self,
        selector: str,
        timeout: int = 30000
    ) -> Optional[ElementChange]:
        """
        等待元素变化

        Args:
            selector: CSS 选择器
            timeout: 超时时间（毫秒）

        Returns:
            变更记录或 None
        """
        start_time = time.time()
        timeout_sec = timeout / 1000

        while time.time() - start_time < timeout_sec:
            changes = self.check_changes()
            for change in changes:
                if change.selector == selector:
                    return change
            time.sleep(self._snapshot_interval)

        return None

    def get_watched_elements(self) -> List[str]:
        """
        获取所有监听的元素

        Returns:
            选择器列表
        """
        return list(self._watched_elements.keys())

    def clear(self):
        """清除所有监听"""
        self._watched_elements.clear()
        self._callbacks.clear()
