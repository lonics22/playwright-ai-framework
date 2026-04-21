"""提示词模板"""
from typing import Dict, Any


class PromptTemplates:
    """AI 测试提示词模板"""

    # 基础任务模板
    BASE_TASK_TEMPLATE = """
你是一个 Web 自动化测试专家。请帮助完成以下任务：

任务：{task}

注意事项：
1. 在每一步操作后，验证操作是否成功
2. 如果遇到错误，尝试替代方案
3. 保持专注在任务目标上
4. 操作完成后报告结果

{context}
"""

    # 表单填写模板
    FORM_FILLING_TEMPLATE = """
请完成表单填写任务。

表单字段：
{form_fields}

填写要求：
{constraints}

注意事项：
1. 确保每个字段都正确填写
2. 注意字段的数据格式要求
3. 检查是否有必填项
4. 提交前验证表单完整性
"""

    # 元素定位模板
    ELEMENT_LOCATION_TEMPLATE = """
请在页面上找到以下元素：

元素描述：{element_description}

可能的定位方式：
- CSS 选择器
- XPath
- 文本内容
- 视觉特征

请尝试多种方式定位该元素，如果找到请返回元素信息。
"""

    # 验证模板
    VERIFICATION_TEMPLATE = """
请验证以下内容：

验证目标：{expectation}

验证步骤：
1. 检查当前页面状态
2. 查找相关元素
3. 验证数据准确性
4. 确认业务逻辑正确性

请返回验证结果：成功/失败，以及详细信息。
"""

    # 错误分析模板
    ERROR_ANALYSIS_TEMPLATE = """
请分析以下测试失败原因：

错误信息：
{error_message}

页面状态：
{page_state}

请分析：
1. 失败的根本原因
2. 可能的解决方案
3. 是否需要调整测试策略
4. 是否是环境问题还是功能问题
"""

    # 自我修复模板
    SELF_HEALING_TEMPLATE = """
元素定位失败，请尝试自我修复：

原始选择器：{original_selector}

元素描述：{element_description}

页面截图可用，请分析：
1. 元素是否存在于页面上
2. 元素是否有变化（位置、样式、文本等）
3. 尝试找到相似或替代元素
4. 返回最佳的替代定位策略
"""

    # 购物流程模板
    SHOPPING_JOURNEY_TEMPLATE = """
请完成一次完整的购物流程：

步骤：
1. 搜索商品："{search_keyword}"
2. 选择第一个商品加入购物车
3. 进入购物车结算
4. 填写配送信息
5. 完成支付流程
6. 验证订单确认

注意事项：
- 如果商品无库存，选择其他商品
- 记录重要的订单信息
- 验证每个步骤的成功状态
"""

    @classmethod
    def format_base_task(cls, task: str, context: Dict[str, Any] = None) -> str:
        """格式化基础任务"""
        context_str = ""
        if context:
            context_str = "\n额外上下文：\n" + "\n".join(
                f"- {k}: {v}" for k, v in context.items()
            )
        return cls.BASE_TASK_TEMPLATE.format(task=task, context=context_str)

    @classmethod
    def format_form_filling(
        cls,
        form_data: Dict[str, str],
        constraints: list = None
    ) -> str:
        """格式化表单填写任务"""
        form_fields = "\n".join(f"- {k}: {v}" for k, v in form_data.items())
        constraints_str = "\n".join(f"- {c}" for c in (constraints or []))
        return cls.FORM_FILLING_TEMPLATE.format(
            form_fields=form_fields,
            constraints=constraints_str
        )

    @classmethod
    def format_element_location(cls, element_description: str) -> str:
        """格式化元素定位任务"""
        return cls.ELEMENT_LOCATION_TEMPLATE.format(
            element_description=element_description
        )

    @classmethod
    def format_verification(cls, expectation: str) -> str:
        """格式化验证任务"""
        return cls.VERIFICATION_TEMPLATE.format(expectation=expectation)

    @classmethod
    def format_error_analysis(cls, error_message: str, page_state: str = "") -> str:
        """格式化错误分析任务"""
        return cls.ERROR_ANALYSIS_TEMPLATE.format(
            error_message=error_message,
            page_state=page_state
        )

    @classmethod
    def format_self_healing(
        cls,
        original_selector: str,
        element_description: str
    ) -> str:
        """格式化自我修复任务"""
        return cls.SELF_HEALING_TEMPLATE.format(
            original_selector=original_selector,
            element_description=element_description
        )

    @classmethod
    def format_shopping_journey(cls, search_keyword: str) -> str:
        """格式化购物流程任务"""
        return cls.SHOPPING_JOURNEY_TEMPLATE.format(search_keyword=search_keyword)


class TaskBuilder:
    """任务构建器"""

    def __init__(self):
        self.steps = []
        self.context = {}

    def add_step(self, step: str):
        """添加步骤"""
        self.steps.append(step)
        return self

    def add_context(self, key: str, value: Any):
        """添加上下文"""
        self.context[key] = value
        return self

    def build(self) -> str:
        """构建完整任务描述"""
        task = "完成以下任务：\n"
        for i, step in enumerate(self.steps, 1):
            task += f"{i}. {step}\n"

        if self.context:
            task += "\n上下文信息：\n"
            for k, v in self.context.items():
                task += f"- {k}: {v}\n"

        return task
