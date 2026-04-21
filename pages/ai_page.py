"""AI 增强页面基类"""
from typing import Optional, Dict, Any
from playwright.sync_api import Page
from core.driver.browser_use_adapter import AIAgentAdapter
from pages.base_page import BasePage
from core.reporting.allure_helper import AllureHelper


class AIPage(BasePage):
    """AI 增强的基础页面对象 - 支持传统和 AI 两种模式"""

    def __init__(self, page: Page, ai_adapter: AIAgentAdapter = None):
        super().__init__(page)
        self.ai = ai_adapter
        self._smart_mode = ai_adapter is not None

    # ========== 传统模式方法（继承自 BasePage）==========
    # click, fill, get_text 等方法已在 BasePage 中定义

    # ========== AI 模式方法 ==========
    async def ai_click(self, element_description: str):
        """
        AI 驱动的点击 - 通过自然语言描述定位元素

        Args:
            element_description: 元素描述（如"右上角的登录按钮"）
        """
        if not self._smart_mode:
            raise RuntimeError("AI adapter not initialized")

        task = f"在页面上找到 '{element_description}' 并点击它"
        with AllureHelper.step_context(f"AI 点击: {element_description}"):
            result = await self.ai.execute_task(task)
            AllureHelper.attach_ai_execution(task, result)
        return result

    async def ai_fill_form(self, form_data: Dict[str, str]):
        """
        AI 驱动的表单填写

        Args:
            form_data: 表单数据字典 {字段名: 值}
        """
        if not self._smart_mode:
            raise RuntimeError("AI adapter not initialized")

        fields = ", ".join([f"{k}={v}" for k, v in form_data.items()])
        task = f"填写表单，字段值: {fields}"

        with AllureHelper.step_context(f"AI 填写表单: {fields}"):
            result = await self.ai.execute_task(task)
            AllureHelper.attach_ai_execution(task, result)
            AllureHelper.attach_form_data(form_data, "表单数据")

        return result

    async def ai_verify(self, expectation: str) -> bool:
        """
        AI 驱动的验证 - 自然语言断言

        Args:
            expectation: 期望条件（如"页面显示订单成功消息"）

        Returns:
            验证是否通过
        """
        if not self._smart_mode:
            raise RuntimeError("AI adapter not initialized")

        task = f"验证页面是否符合预期: {expectation}"

        with AllureHelper.step_context(f"AI 验证: {expectation}"):
            result = await self.ai.execute_task(task)
            AllureHelper.attach_ai_execution(task, result)

        return getattr(result, "success", False)

    async def ai_find_element(self, element_description: str) -> Dict[str, Any]:
        """
        AI 驱动的元素查找

        Args:
            element_description: 元素描述

        Returns:
            元素信息字典
        """
        if not self._smart_mode:
            raise RuntimeError("AI adapter not initialized")

        task = f"在页面上找到元素: {element_description}，返回元素的选择器"

        with AllureHelper.step_context(f"AI 查找元素: {element_description}"):
            result = await self.ai.execute_task(task)

        return result

    async def ai_navigate(self, target: str):
        """
        AI 驱动的导航

        Args:
            target: 导航目标（如"个人中心页面"）
        """
        if not self._smart_mode:
            raise RuntimeError("AI adapter not initialized")

        task = f"导航到: {target}"

        with AllureHelper.step_context(f"AI 导航: {target}"):
            result = await self.ai.execute_task(task)
            AllureHelper.attach_ai_execution(task, result)

        return result

    async def ai_search(self, keyword: str):
        """
        AI 驱动的搜索

        Args:
            keyword: 搜索关键词
        """
        if not self._smart_mode:
            raise RuntimeError("AI adapter not initialized")

        task = f"在搜索框输入 '{keyword}' 并搜索"

        with AllureHelper.step_context(f"AI 搜索: {keyword}"):
            result = await self.ai.execute_task(task)
            AllureHelper.attach_ai_execution(task, result)

        return result

    async def ai_complete_task(self, task_description: str, context: Dict[str, Any] = None):
        """
        使用 AI 完成复杂任务

        Args:
            task_description: 任务描述
            context: 额外上下文

        Returns:
            执行结果
        """
        if not self._smart_mode:
            raise RuntimeError("AI adapter not initialized")

        with AllureHelper.step_context(f"AI 执行任务: {task_description[:50]}..."):
            result = await self.ai.execute_task(task_description, context)
            AllureHelper.attach_ai_execution(task_description, result)

        return result

    async def ai_complete_steps(self, steps: list):
        """
        使用 AI 完成多个步骤

        Args:
            steps: 步骤列表

        Returns:
            执行结果
        """
        if not self._smart_mode:
            raise RuntimeError("AI adapter not initialized")

        task = "完成以下任务步骤:\n" + "\n".join(
            f"{i+1}. {step}" for i, step in enumerate(steps)
        )

        with AllureHelper.step_context(f"AI 执行 {len(steps)} 个步骤"):
            result = await self.ai.execute_task(task)
            AllureHelper.attach_ai_execution(task, result)

        return result

    def is_ai_enabled(self) -> bool:
        """
        检查是否启用了 AI 模式

        Returns:
            是否启用 AI
        """
        return self._smart_mode

    def get_ai_adapter(self) -> Optional[AIAgentAdapter]:
        """
        获取 AI 适配器

        Returns:
            AIAgentAdapter 实例或 None
        """
        return self.ai
