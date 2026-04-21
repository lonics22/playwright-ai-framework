"""混合模式测试示例 - 传统 POM + AI 能力"""
import pytest
import allure


@pytest.mark.hybrid
@allure.feature("混合模式测试")
class TestE2EWithAI:
    """结合传统 POM 与 AI 能力的测试"""

    @allure.title("登录后 AI 完成复杂操作")
    async def test_login_then_ai_task(self, async_page, async_ai_agent):
        """传统方式登录，AI 方式处理复杂业务"""
        from pages.base_page import BasePage

        # 传统方式：稳定的登录流程
        base_page = BasePage(async_page)

        with allure.step("传统方式：用户登录"):
            base_page.navigate_to("https://example-shop.com/login")
            base_page.fill("#email", "user@test.com")
            base_page.fill("#password", "password123")
            base_page.click("button[type='submit']")
            base_page.wait_for_page_load()

        # 截图记录登录后的状态
        base_page.take_screenshot("登录后状态")

        # AI 方式：处理复杂、易变的业务流程
        with allure.step("AI 方式：完成评价流程"):
            result = await async_ai_agent.execute_task("""
                在个人中心完成以下操作：
                1. 找到订单历史标签并点击
                2. 找到最近一笔未评价的订单
                3. 为该订单添加五星好评，评论写 "Great product!"
                4. 上传一张测试图片作为评价配图
                5. 提交评价并确认成功
            """)

            allure.attach(
                str(result),
                name="AI 执行结果",
                attachment_type=allure.attachment_type.TEXT
            )

        assert getattr(result, "success", False)

    @allure.title("AI 辅助验证 + 传统操作")
    async def test_traditional_ops_with_ai_verification(self, async_smart_page, async_page):
        """传统操作 + AI 验证"""
        smart_page = async_smart_page

        with allure.step("传统方式：添加商品到购物车"):
            await async_page.goto("https://example-shop.com/products")
            await async_page.click(".product-card:first-child .add-to-cart")
            await async_page.wait_for_load_state("networkidle")

        with allure.step("AI 方式：验证购物车内容"):
            # 使用 AI 验证购物车中是否有正确的商品
            is_correct = await smart_page.ai_verify(
                "购物车中显示刚刚添加的商品，商品数量为1，并且显示正确的商品图片和名称"
            )

        assert is_correct

    @allure.title("混合模式：表单填写和提交")
    async def test_mixed_form_submission(self, async_smart_page, async_page):
        """混合模式表单提交"""
        smart_page = async_smart_page

        with allure.step("传统方式：导航到表单页面"):
            await async_page.goto("https://example.com/checkout")

        with allure.step("AI 方式：智能填写复杂表单"):
            # AI 处理复杂表单，自动识别字段
            result = await smart_page.ai_fill_form({
                "full_name": "张三",
                "phone": "13800138000",
                "address": "北京市朝阳区建国路88号",
                "city": "北京",
                "postal_code": "100000",
                "payment_method": "信用卡"
            })

            allure.attach(
                str(result),
                name="AI 表单填写结果",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("传统方式：提交表单"):
            await async_page.click("button[type='submit']")
            await async_page.wait_for_load_state("networkidle")

        with allure.step("AI 方式：验证提交结果"):
            is_success = await smart_page.ai_verify(
                "页面显示订单提交成功，订单号已生成，并显示预计配送时间"
            )

        assert is_success

    @allure.title("智能错误处理和恢复")
    async def test_intelligent_error_recovery(self, async_smart_page, async_page):
        """测试智能错误处理和恢复"""
        smart_page = async_smart_page

        with allure.step("尝试访问可能出错的页面"):
            await async_page.goto("https://example.com/unstable-page")

        with allure.step("AI 方式：自动处理可能的错误"):
            result = await smart_page.ai_complete_task("""
                当前页面可能有以下情况，请处理：
                1. 如果出现加载错误，刷新页面重试
                2. 如果出现登录过期提示，点击重新登录
                3. 如果出现维护页面，记录错误信息
                4. 如果页面正常加载，验证关键元素存在
            """)

            allure.attach(
                str(result),
                name="AI 错误处理结果",
                attachment_type=allure.attachment_type.TEXT
            )

        # 验证 AI 成功处理了场景
        assert getattr(result, "success", False)

    @allure.title("多页面混合流程")
    async def test_multi_page_hybrid_flow(self, async_smart_page, async_page):
        """多页面混合流程测试"""
        smart_page = async_smart_page

        with allure.step("步骤1: 传统方式访问首页"):
            await async_page.goto("https://example-shop.com")
            await async_page.wait_for_load_state("networkidle")

        with allure.step("步骤2: AI 方式搜索和筛选"):
            result = await smart_page.ai_complete_task("""
                在首页完成以下操作：
                1. 找到搜索框搜索 "wireless mouse"
                2. 筛选价格低于 50 美元的商品
                3. 选择第一个符合条件的商品
            """)

        with allure.step("步骤3: 传统方式添加到购物车"):
            await async_page.click("button.add-to-cart")
            await async_page.wait_for_selector(".cart-notification")

        with allure.step("步骤4: AI 方式继续购物并结算"):
            result = await smart_page.ai_complete_task("""
                继续完成购物流程：
                1. 点击继续购物
                2. 添加另一个商品到购物车
                3. 进入购物车
                4. 点击结算按钮
            """)

        assert getattr(result, "success", False)
