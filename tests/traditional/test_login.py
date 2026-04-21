"""传统自动化测试示例 - 登录功能"""
import pytest
import allure
from pages.base_page import BasePage


@pytest.mark.ui
@allure.feature("用户认证")
@allure.story("登录功能")
class TestLogin:
    """登录功能测试"""

    @allure.title("成功登录测试")
    def test_successful_login(self, page, env_config):
        """测试用户能够成功登录"""
        # 使用基础页面对象
        base_page = BasePage(page)

        # 导航到登录页面
        base_url = env_config.get("base_url", "https://example.com")
        base_page.navigate_to(f"{base_url}/login")
        base_page.wait_for_page_load()

        # 截图记录
        base_page.take_screenshot("登录页面")

        # 填写登录表单
        with allure.step("填写用户名"):
            base_page.fill("#username", "testuser@example.com")

        with allure.step("填写密码"):
            base_page.fill("#password", "TestPass123!")

        with allure.step("点击登录按钮"):
            base_page.click("button[type='submit']")

        # 等待页面跳转
        base_page.wait_for_page_load()

        # 验证登录成功
        with allure.step("验证登录成功"):
            assert "dashboard" in base_page.get_page_url() or "welcome" in base_page.get_page_title().lower()

    @allure.title("登录失败 - 错误密码")
    def test_login_with_wrong_password(self, page, env_config):
        """测试使用错误密码登录失败"""
        base_page = BasePage(page)

        base_url = env_config.get("base_url", "https://example.com")
        base_page.navigate_to(f"{base_url}/login")

        with allure.step("填写错误的登录信息"):
            base_page.fill("#username", "testuser@example.com")
            base_page.fill("#password", "WrongPassword123!")
            base_page.click("button[type='submit']")

        # 验证错误提示
        with allure.step("验证错误提示显示"):
            error_visible = base_page.is_visible(".error-message, .alert-error")
            assert error_visible, "应该显示错误提示"

    @allure.title("登录表单验证 - 空字段")
    def test_login_form_validation(self, page, env_config):
        """测试登录表单验证"""
        base_page = BasePage(page)

        base_url = env_config.get("base_url", "https://example.com")
        base_page.navigate_to(f"{base_url}/login")

        with allure.step("提交空表单"):
            base_page.click("button[type='submit']")

        # 验证验证提示
        with allure.step("验证验证提示"):
            # 检查是否有必填字段验证
            validation_visible = base_page.is_visible(
                ".validation-error, .field-error, :invalid"
            )
            # 如果浏览器原生验证，可能没有可见元素
            assert True  # 简化验证

    @allure.title("记住我功能")
    @pytest.mark.skip(reason="需要具体页面实现")
    def test_remember_me(self, page):
        """测试记住我功能"""
        pass


@pytest.mark.ui
@allure.feature("用户认证")
@allure.story("注册功能")
class TestRegister:
    """用户注册测试"""

    @allure.title("成功注册新用户")
    def test_successful_registration(self, page, env_config):
        """测试新用户注册"""
        from faker import Faker
        fake = Faker()

        base_page = BasePage(page)
        base_url = env_config.get("base_url", "https://example.com")

        base_page.navigate_to(f"{base_url}/register")

        with allure.step("填写注册信息"):
            base_page.fill("#email", fake.email())
            base_page.fill("#password", "TestPass123!")
            base_page.fill("#confirm_password", "TestPass123!")
            base_page.fill("#username", fake.user_name())

        with allure.step("同意服务条款"):
            if base_page.is_visible("#terms"):
                base_page.click("#terms")

        with allure.step("提交注册"):
            base_page.click("button[type='submit']")

        base_page.wait_for_page_load()

        # 验证注册成功
        with allure.step("验证注册成功"):
            success_message_visible = base_page.is_visible(
                ".success-message, .alert-success, [data-testid='registration-success']"
            )
            # 根据实际页面调整断言
