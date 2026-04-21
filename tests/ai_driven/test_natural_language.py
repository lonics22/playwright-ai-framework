"""AI 驱动测试示例 - 自然语言任务执行"""
import pytest
import allure


@pytest.mark.ai
@allure.feature("AI 驱动测试")
@allure.story("自然语言任务执行")
class TestNaturalLanguage:
    """自然语言描述的测试用例"""

    @allure.title("完成完整购物流程")
    async def test_shopping_journey(self, async_ai_agent, async_page):
        """使用自然语言描述复杂的端到端场景"""
        # 先使用传统方式打开页面
        await async_page.goto("https://example-shop.com")

        # AI 方式：执行复杂任务
        result = await async_ai_agent.execute_task("""
            完成一次完整的购物流程：
            1. 在搜索框输入 "wireless headphones"
            2. 选择第一个商品加入购物车
            3. 进入购物车结算
            4. 使用测试信用卡信息完成支付
            5. 验证订单确认页面显示成功消息
        """)

        # Allure 报告附加 AI 执行详情
        allure.attach(
            str(result),
            name="AI 执行日志",
            attachment_type=allure.attachment_type.TEXT
        )

        assert getattr(result, "success", False), "AI 任务执行失败"

    @allure.title("自适应表单填写")
    async def test_self_healing_form(self, async_ai_agent):
        """当页面结构变化时，AI 自动适应"""

        result = await async_ai_agent.execute_task(
            task="填写用户注册表单",
            context={
                "form_data": {
                    "username": "testuser123",
                    "email": "test@example.com",
                    "password": "TestPass123!"
                },
                "constraints": ["必须同意服务条款"]
            }
        )

        allure.attach(
            str(result),
            name="AI 执行结果",
            attachment_type=allure.attachment_type.TEXT
        )

        assert getattr(result, "success", False)

    @allure.title("智能搜索和筛选")
    async def test_intelligent_search(self, async_ai_agent, async_page):
        """AI 智能搜索和筛选商品"""
        await async_page.goto("https://example-shop.com")

        result = await async_ai_agent.execute_task("""
            完成以下任务：
            1. 找到搜索框并搜索 "laptop"
            2. 应用筛选条件：价格范围 500-1000 美元，品牌选择 Dell 或 HP
            3. 按评分排序
            4. 选择评分最高的商品查看详情
            5. 验证商品页面显示正确的价格范围
        """)

        allure.attach(
            str(result),
            name="AI 执行结果",
            attachment_type=allure.attachment_type.TEXT
        )

        assert getattr(result, "success", False)

    @allure.title("多步骤复杂流程")
    async def test_complex_multi_step_flow(self, async_ai_agent, async_page):
        """AI 执行多步骤复杂流程"""
        await async_page.goto("https://example-app.com")

        steps = [
            "找到并点击'我的账户'链接",
            "在账户设置中找到'安全'选项卡",
            "启用双重验证",
            "选择通过短信接收验证码",
            "输入测试手机号 +1234567890",
            "验证显示成功设置消息"
        ]

        result = await async_ai_agent.execute_steps(steps)

        allure.attach(
            str(result),
            name="AI 执行结果",
            attachment_type=allure.attachment_type.TEXT
        )

        assert getattr(result, "success", False)

    @allure.title("使用不同 LLM 提供商 - Anthropic")
    @pytest.mark.ai(llm="anthropic")
    async def test_with_anthropic(self, async_ai_agent, async_page):
        """使用 Anthropic Claude 执行 AI 测试"""
        await async_page.goto("https://example.com")

        result = await async_ai_agent.execute_task(
            "找到页面上的联系表单并填写测试信息"
        )

        assert getattr(result, "success", False)

    @allure.title("使用本地 LLM - Ollama")
    @pytest.mark.ai(llm="local")
    @pytest.mark.skip(reason="需要本地 Ollama 服务")
    async def test_with_local_llm(self, async_ai_agent, async_page):
        """使用本地 Ollama LLM 执行 AI 测试"""
        await async_page.goto("https://example.com")

        result = await async_ai_agent.execute_task(
            "找到导航菜单并点击'关于我们'页面"
        )

        assert getattr(result, "success", False)
