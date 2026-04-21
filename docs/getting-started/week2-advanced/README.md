# Week 2: 进阶提升 - 页面对象模式与智能定位

> 🎯 本周目标：掌握页面对象模式 (POM)，学会使用 SmartLocator 智能定位和元素自愈机制

---

## 📚 学习路线图

```
Day 1-2: 理解并实践页面对象模式 (POM)
Day 3-4: SmartLocator 智能元素定位
Day 5-6: 自我修复 (Self-Healing) 机制
Day 7:    综合项目 - 搭建完整的测试框架
```

---

## Day 1-2: 页面对象模式 (Page Object Model)

### 2.1 为什么要用 POM？

**不使用 POM 的问题：**
```python
# ❌ 不好的做法 - 测试代码和定位逻辑混在一起
def test_login(page):
    page.goto("https://example.com/login")
    page.fill("#username", "test")
    page.fill("#password", "pass")
    page.click("button[type='submit']")
    # 如果页面改版，需要修改所有用到这些选择器的测试
```

**使用 POM 的好处：**
```python
# ✅ 好的做法 - 测试代码和业务逻辑分离
class LoginPage(BasePage):
    # 选择器集中管理
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    SUBMIT_BUTTON = "button[type='submit']"
    
    def login(self, username, password):
        self.fill(self.USERNAME_INPUT, username)
        self.fill(self.PASSWORD_INPUT, password)
        self.click(self.SUBMIT_BUTTON)

# 测试代码简洁清晰
def test_login(page):
    login_page = LoginPage(page)
    login_page.navigate_to("https://example.com/login")
    login_page.login("test", "pass")
    # 页面改版只需要改 LoginPage 类
```

### 2.2 创建完整的页面对象

```python
# pages/login_page.py
from pages.base_page import BasePage
from pages.components.header import Header
from pages.components.footer import Footer


class LoginPage(BasePage):
    """登录页面"""
    
    # ========== 页面 URL ==========
    URL = "/login"
    
    # ========== 选择器定义 ==========
    # 表单元素
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    SUBMIT_BUTTON = "button[type='submit']"
    REMEMBER_ME = "input[name='remember']"
    
    # 链接元素
    FORGOT_PASSWORD_LINK = "a[href='/forgot-password']"
    REGISTER_LINK = "a[href='/register']"
    
    # 提示元素
    ERROR_MESSAGE = ".error-message"
    SUCCESS_MESSAGE = ".success-message"
    
    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)
        self.footer = Footer(page)
    
    # ========== 页面导航 ==========
    def navigate(self):
        """导航到登录页"""
        self.navigate_to(f"{self.env_config['base_url']}{self.URL}")
        return self
    
    # ========== 表单操作 ==========
    def fill_username(self, username):
        """填写用户名"""
        self.fill(self.USERNAME_INPUT, username)
        return self
    
    def fill_password(self, password):
        """填写密码"""
        self.fill(self.PASSWORD_INPUT, password)
        return self
    
    def check_remember_me(self):
        """勾选记住我"""
        if not self.is_checked(self.REMEMBER_ME):
            self.click(self.REMEMBER_ME)
        return self
    
    def click_submit(self):
        """点击登录按钮"""
        self.click(self.SUBMIT_BUTTON)
        return self
    
    # ========== 组合操作 ==========
    def login(self, username, password, remember=False):
        """完整登录流程"""
        self.fill_username(username)
        self.fill_password(password)
        if remember:
            self.check_remember_me()
        self.click_submit()
        return self
    
    def login_as_valid_user(self):
        """使用有效用户登录（快捷方式）"""
        return self.login("valid@example.com", "ValidPass123!")
    
    def login_as_admin(self):
        """使用管理员登录"""
        return self.login("admin@example.com", "AdminPass123!")
    
    # ========== 链接跳转 ==========
    def go_to_forgot_password(self):
        """跳转到忘记密码页"""
        self.click(self.FORGOT_PASSWORD_LINK)
        return ForgotPasswordPage(self.page)
    
    def go_to_register(self):
        """跳转到注册页"""
        self.click(self.REGISTER_LINK)
        return RegisterPage(self.page)
    
    # ========== 状态验证 ==========
    def is_error_displayed(self):
        """是否显示错误信息"""
        return self.is_visible(self.ERROR_MESSAGE)
    
    def get_error_message(self):
        """获取错误信息文本"""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_success_displayed(self):
        """是否显示成功信息"""
        return self.is_visible(self.SUCCESS_MESSAGE)
    
    def wait_for_login_complete(self):
        """等待登录完成"""
        self.wait_for_element_visible(".user-profile, .dashboard")
        return self
```

### 2.3 组件化设计

```python
# pages/components/header.py
class Header:
    """页面头部组件 - 可复用于多个页面"""
    
    SELECTORS = {
        "logo": ".header-logo",
        "nav_menu": ".nav-menu",
        "search_box": ".search-input",
        "search_btn": ".search-btn",
        "cart_icon": ".cart-icon",
        "cart_count": ".cart-count",
        "user_menu": ".user-menu",
        "login_link": ".login-link",
        "logout_link": ".logout-link",
    }
    
    def __init__(self, page):
        self.page = page
        self.locator = SmartLocator(page)
    
    def search(self, keyword):
        """搜索商品"""
        self.locator.find(self.SELECTORS["search_box"]).fill(keyword)
        self.locator.find(self.SELECTORS["search_btn"]).click()
        return SearchResultPage(self.page)
    
    def go_to_cart(self):
        """进入购物车"""
        self.locator.find(self.SELECTORS["cart_icon"]).click()
        return CartPage(self.page)
    
    def get_cart_count(self):
        """获取购物车商品数量"""
        count_text = self.locator.find(self.SELECTORS["cart_count"]).text_content()
        return int(count_text) if count_text else 0
    
    def click_login(self):
        """点击登录"""
        self.locator.find(self.SELECTORS["login_link"]).click()
        return LoginPage(self.page)
    
    def click_logout(self):
        """点击退出"""
        self.locator.find(self.SELECTORS["logout_link"]).click()
        return self
```

### 2.4 测试中使用 POM

```python
# tests/test_login_with_pom.py
import allure
from pages.login_page import LoginPage

@allure.feature("登录功能")
@allure.story("使用POM的登录测试")
class TestLoginWithPOM:
    """使用页面对象模式的登录测试"""
    
    @allure.title("正常登录流程")
    def test_successful_login(self, page, env_config):
        """测试正常登录"""
        # 1. 创建页面对象
        login_page = LoginPage(page)
        
        # 2. 导航到登录页
        login_page.navigate()
        
        # 3. 执行登录（链式调用）
        login_page.fill_username("test@example.com") \
                  .fill_password("TestPass123!") \
                  .click_submit()
        
        # 4. 等待登录完成
        login_page.wait_for_login_complete()
        
        # 5. 验证跳转成功
        assert "dashboard" in page.url
    
    @allure.title("使用快捷方式登录")
    def test_login_with_shortcut(self, page):
        """使用预设用户快捷登录"""
        login_page = LoginPage(page)
        login_page.navigate().login_as_valid_user()
        
        # 验证登录成功
        assert not login_page.is_error_displayed()
    
    @allure.title("登录失败验证")
    def test_login_failure(self, page):
        """测试错误密码登录失败"""
        login_page = LoginPage(page)
        login_page.navigate().login("wrong@example.com", "wrongpass")
        
        # 验证错误提示
        assert login_page.is_error_displayed()
        assert "用户名或密码错误" in login_page.get_error_message()
```

---

## Day 3-4: SmartLocator 智能定位

### 4.1 为什么需要 SmartLocator？

传统定位的问题：
```python
# 问题1: 元素不存在时直接报错
element = page.locator("#submit-button")
element.click()  # 如果元素不存在，直接抛出异常

# 问题2: 没有备用方案
# 如果 #submit-button 变了，测试直接失败

# 问题3: 无法智能重试
# 元素还在加载中，但代码已经执行了
```

SmartLocator 解决方案：
```python
from core.elements.smart_locator import SmartLocator

smart = SmartLocator(page)

# 智能查找：先尝试主选择器，失败尝试备用选择器
element = smart.find(
    selector="#submit-button",
    fallback_description="蓝色的提交按钮"
)

# 自动等待：元素出现前会一直等待
element = smart.wait_for_element(".dynamic-content", timeout=10000)
```

### 4.2 SmartLocator 核心功能

```python
class TestSmartLocator:
    """SmartLocator 使用示例"""
    
    def test_basic_usage(self, page):
        """基础用法"""
        smart = SmartLocator(page)
        
        # 1. 智能查找元素
        # 先尝试主选择器，失败时报错前的友好提示
        element = smart.find("#username", fallback_description="用户名输入框")
        
        # 2. 等待元素出现
        element = smart.wait_for_element("#modal", state="visible", timeout=5000)
        
        # 3. 查找多个元素
        items = smart.find_all(".product-item")
        assert len(items) > 0
        
        # 4. 检查元素是否存在（不抛出异常）
        if smart.is_element_present("#optional-banner"):
            smart.find("#optional-banner").click()
    
    def test_element_registry(self, page):
        """元素注册功能 - 多维度特征存储"""
        smart = SmartLocator(page)
        
        # 注册元素的多维度特征
        smart.register_element(
            name="submit_button",
            selectors=[
                "#submit-btn",           # ID
                "button[type='submit']", # 属性
                ".btn-primary",          # 类名
                "text=提交"              # 文本
            ]
        )
        
        # 后续查找时，如果第一个选择器失败，会自动尝试后面的
        element = smart.find("submit_button")
    
    def test_async_usage(self, async_page):
        """异步用法"""
        from core.elements.smart_locator import AsyncSmartLocator
        
        smart = AsyncSmartLocator(async_page)
        
        # 异步查找
        element = await smart.find("#async-loaded-content")
        count = await smart.is_element_present("#notification")
```

### 4.3 练习：使用 SmartLocator 重构测试

**练习 1**: 将之前的登录测试改为使用 SmartLocator

```python
# pages/login_page_v2.py - 使用 SmartLocator 的版本
from core.elements.smart_locator import SmartLocator
from pages.base_page import BasePage


class LoginPageV2(BasePage):
    """使用 SmartLocator 的登录页"""
    
    def __init__(self, page):
        super().__init__(page)
        self.smart = SmartLocator(page)
        
        # 注册元素特征
        self.smart.register_element("username", [
            "input[name='username']",
            "input[placeholder='请输入用户名']",
            "#username"
        ])
        self.smart.register_element("password", [
            "input[name='password']",
            "input[type='password']",
            "#password"
        ])
        self.smart.register_element("submit", [
            "button[type='submit']",
            ".btn-login",
            "text=登录"
        ])
    
    def login(self, username, password):
        """使用 SmartLocator 的登录方法"""
        # 即使页面改版，只要有一个选择器有效就能找到元素
        self.smart.find("username").fill(username)
        self.smart.find("password").fill(password)
        self.smart.find("submit").click()
        return self
    
    def wait_for_error_message(self):
        """等待错误信息出现"""
        return self.smart.wait_for_element(
            ".error-message",
            state="visible",
            timeout=3000
        )
```

---

## Day 5-6: 自我修复 (Self-Healing) 机制

### 5.1 什么是 Self-Healing？

当页面结构变化时，传统的测试会直接失败。Self-Healing 会尝试自动修复定位策略。

```python
# 场景：开发改了按钮的 ID
# 原来: <button id="submit-btn">提交</button>
# 现在: <button id="submit-button-v2">提交</button>

# 传统测试会失败
page.click("#submit-btn")  # ❌ 失败！ID变了

# Self-Healing 会自动尝试修复
healer = SelfHealingLocator(page)
element = healer.find_with_healing(
    failed_selector="#submit-btn",
    element_description="蓝色的提交按钮"
)
# ✅ 成功！通过描述找到新位置的按钮
```

### 5.2 Self-Healing 策略详解

```python
from core.elements.self_healing import SelfHealingLocator


class TestSelfHealing:
    """自我修复测试示例"""
    
    def test_with_self_healing(self, page):
        """使用自我修复的定位"""
        healer = SelfHealingLocator(page)
        
        try:
            # 尝试原始定位
            element = page.locator("#old-button-id")
            element.click()
        except Exception as e:
            print(f"原始定位失败: {e}")
            
            # 使用自我修复
            healed = healer.find_with_healing(
                failed_selector="#old-button-id",
                element_description="页面右下角的蓝色提交按钮，上面有"确认"两个字"
            )
            
            if healed:
                print(f"✅ 修复成功！使用新定位器: {healed}")
                healed.click()
            else:
                print("❌ 修复失败，需要人工检查")
                raise
    
    def test_healing_strategies(self, page):
        """了解修复策略"""
        healer = SelfHealingLocator(page)
        
        # 策略1: 添加 contains 匹配
        # "[id='submit']" → "[id*='submit']"
        
        # 策略2: 使用部分匹配
        # "data-test='btn-submit'" → "data-test*='submit'"
        
        # 策略3: 调整父子关系
        # ".form > .btn" → ".form:has(>.btn)"
        
        # 策略4: 尝试不同属性
        # "data-testid" → "data-test-id"
        
        # 策略5: AI 视觉定位（如果配置了 AI）
        # 截图 + AI 分析找到相似元素
        
    def test_healing_report(self, page):
        """查看修复报告"""
        healer = SelfHealingLocator(page)
        
        # 执行一些可能失败的定位
        for selector in ["#btn1", "#btn2", "#btn3"]:
            try:
                healer.find_with_healing(selector, f"按钮{selector}")
            except:
                pass
        
        # 生成修复报告
        report = healer.generate_healing_report()
        print(report)
        # 输出示例：
        # === Self-Healing Report ===
        # Healing Methods Used:
        #   - common_strategy: 2
        #   - ai_healing: 1
        # Detailed Events:
        # 1. #btn1 -> common_strategy
        # 2. #btn2 -> ai_healing
```

### 5.3 练习：模拟页面变化并观察自愈效果

```python
import allure

@allure.feature("自我修复机制")
class TestSelfHealingPractice:
    """自愈机制练习"""
    
    @allure.title("练习1: 元素ID变化后的自愈")
    def test_element_id_changed(self, page):
        """模拟元素ID变化，观察自愈效果"""
        # 假设页面改版前是 #submit-btn，改版后是 #submit-button
        
        healer = SelfHealingLocator(page)
        
        # 尝试使用旧的选择器
        old_selector = "#submit-btn"  # 已不存在
        
        element = healer.find_with_healing(
            failed_selector=old_selector,
            element_description="表单下方的蓝色提交按钮"
        )
        
        assert element is not None, "应该能找到替代元素"
        
        # 验证修复历史被记录
        history = healer.get_healing_history()
        assert len(history) > 0
        assert history[0]["method"] in ["common_strategy", "ai_healing"]
    
    @allure.title("练习2: 多级修复策略")
    def test_multiple_healing_attempts(self, page):
        """测试多种修复策略的尝试顺序"""
        healer = SelfHealingLocator(page)
        
        # 按优先级尝试：
        # 1. common_strategy（快速修复）
        # 2. ai_healing（智能修复）
        
        with allure.step("触发定位失败"):
            # 使用一个肯定失败的选择器
            element = healer.find_with_healing(
                failed_selector="#definitely-not-exist",
                element_description="页面主要内容区域"
            )
        
        # 查看使用了哪些策略
        with allure.step("查看修复策略"):
            for record in healer.get_healing_history():
                allure.attach(
                    f"原选择器: {record['original_selector']}\n方法: {record['method']}",
                    name="修复记录"
                )
```

---

## Day 7: 综合项目 - 搭建完整测试框架

### 7.1 项目结构

```
project/
├── pages/
│   ├── __init__.py
│   ├── base_page.py           # 基础页面对象
│   ├── login_page.py          # 登录页
│   ├── home_page.py           # 首页
│   ├── product_page.py        # 商品页
│   └── components/
│       ├── __init__.py
│       ├── header.py          # 头部组件
│       └── footer.py          # 底部组件
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # pytest配置
│   ├── test_login.py          # 登录测试
│   ├── test_product.py        # 商品测试
│   └── test_shopping_cart.py  # 购物车测试
└── utils/
    ├── __init__.py
    └── test_data.py           # 测试数据
```

### 7.2 完整页面对象示例

```python
# pages/home_page.py
from pages.base_page import BasePage
from pages.components.header import Header
from pages.product_page import ProductPage


class HomePage(BasePage):
    """首页"""
    
    URL = "/"
    
    # 轮播图
    BANNER_SLIDES = ".banner-slide"
    BANNER_NEXT = ".banner-next"
    
    # 商品分类
    CATEGORY_LIST = ".category-item"
    
    # 推荐商品
    RECOMMENDED_PRODUCTS = ".product-card"
    
    def __init__(self, page):
        super().__init__(page)
        self.header = Header(page)
    
    def navigate(self):
        """导航到首页"""
        self.navigate_to(self.env_config['base_url'])
        return self
    
    def get_banner_count(self):
        """获取轮播图数量"""
        return self.smart.find_all(self.BANNER_SLIDES)
    
    def click_next_banner(self):
        """点击下一张轮播"""
        self.click(self.BANNER_NEXT)
        return self
    
    def click_category(self, category_name):
        """点击商品分类"""
        self.click(f"text={category_name}")
        return ProductListPage(self.page)
    
    def click_recommended_product(self, index=0):
        """点击推荐商品"""
        products = self.smart.find_all(self.RECOMMENDED_PRODUCTS)
        if index < len(products):
            products[index].click()
        return ProductPage(self.page)
    
    def search(self, keyword):
        """搜索商品"""
        return self.header.search(keyword)
```

### 7.3 完整测试套件示例

```python
# tests/test_e2e_shopping.py
import allure
import pytest
from pages.home_page import HomePage
from pages.login_page import LoginPage
from pages.cart_page import CartPage


@allure.epic("电商系统")
@allure.feature("端到端购物流程")
class TestE2EShopping:
    """端到端购物流程测试"""
    
    @pytest.fixture
    def logged_in_user(self, page):
        """登录用户的fixture"""
        login_page = LoginPage(page)
        login_page.navigate().login_as_valid_user()
        yield page
    
    @allure.title("完整购物流程")
    def test_complete_shopping_flow(self, logged_in_user):
        """测试完整的购物到支付流程"""
        page = logged_in_user
        
        with allure.step("1. 浏览首页并选择商品"):
            home = HomePage(page).navigate()
            product_page = home.click_recommended_product(index=0)
            allure.attach(product_page.get_product_name(), "选中商品")
        
        with allure.step("2. 添加商品到购物车"):
            product_name = product_page.get_product_name()
            product_price = product_page.get_product_price()
            product_page.add_to_cart()
            assert product_page.is_add_success()
        
        with allure.step("3. 进入购物车确认"):
            cart = CartPage(page)
            cart.navigate()
            assert cart.has_product(product_name)
            assert cart.get_product_price(product_name) == product_price
        
        with allure.step("4. 结算"):
            checkout = cart.proceed_to_checkout()
            checkout.fill_shipping_address()
            checkout.select_payment_method("alipay")
        
        with allure.step("5. 确认订单"):
            order = checkout.place_order()
            assert order.is_order_successful()
            order_number = order.get_order_number()
            allure.attach(order_number, "订单号")
```

---

## 📝 Week 2 作业清单

- [ ] 为登录页面创建完整的 POM 类（包含至少 10 个方法）
- [ ] 创建 2 个可复用的组件（如 Header、Footer）
- [ ] 使用 SmartLocator 重构 3 个现有测试
- [ ] 编写 1 个测试观察 Self-Healing 效果
- [ ] 搭建一个包含 3 个页面的完整测试套件

---

## 💡 本周重点回顾

1. **POM 的核心思想**：
   - 页面对象封装页面细节
   - 测试代码只调用业务方法
   - 一处修改，全局生效

2. **SmartLocator 的优势**：
   - 多维度元素查找
   - 自动等待机制
   - 失败前的友好提示

3. **Self-Healing 的价值**：
   - 减少测试维护成本
   - 自动适应页面变化
   - 提高测试稳定性

---

**恭喜完成 Week 2！** 你已经掌握了企业级自动化测试的核心技能。继续 Week 3 学习 AI 能力！
