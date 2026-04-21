# Week 1: 基础巩固 - 掌握传统测试的核心技能

> 🎯 本周目标：熟练掌握传统自动化测试的基本操作，能够独立编写 5-10 个测试用例

---

## 📚 学习路线图

```
Day 1-2: 理解 BasePage 的核心方法
Day 3-4: 元素定位策略与实践
Day 5-6: 断言与验证技巧
Day 7:    综合练习与 Allure 报告
```

---

## Day 1-2: 掌握 BasePage 核心方法

### 2.1 页面导航与基础操作

```python
from pages.base_page import BasePage

class TestBasicOperations:
    """基础操作练习"""
    
    def test_navigate_and_interact(self, page):
        base = BasePage(page)
        
        # 1. 导航到页面
        base.navigate_to("https://www.example.com")
        
        # 2. 等待页面加载
        base.wait_for_page_load()
        
        # 3. 点击元素
        base.click("#submit-button")
        
        # 4. 填写表单
        base.fill("#username", "testuser")
        base.fill("#password", "testpass123")
        
        # 5. 截图记录
        base.take_screenshot("after_login")
```

### 2.2 常用方法速查表

| 方法 | 用途 | 示例 |
|------|------|------|
| `navigate_to(url)` | 打开网页 | `base.navigate_to("https://baidu.com")` |
| `click(selector)` | 点击元素 | `base.click("#btn")` |
| `fill(selector, value)` | 填写输入框 | `base.fill("#name", "张三")` |
| `clear(selector)` | 清空输入框 | `base.clear("#search")` |
| `get_text(selector)` | 获取文本 | `text = base.get_text(".title")` |
| `get_attribute(selector, attr)` | 获取属性 | `href = base.get_attribute("a", "href")` |
| `is_visible(selector)` | 检查可见性 | `if base.is_visible("#modal"):` |
| `is_enabled(selector)` | 检查可用性 | `if base.is_enabled("#btn"):` |
| `select_option(selector, value)` | 选择下拉框 | `base.select_option("#city", "北京")` |
| `upload_file(selector, path)` | 上传文件 | `base.upload_file("#file", "test.pdf")` |
| `take_screenshot(name)` | 截图 | `base.take_screenshot("result")` |

### 2.3 练习任务

**练习 1**: 访问京东首页，搜索"手机"，验证搜索结果页标题包含"手机"

```python
import allure
from pages.base_page import BasePage

@allure.feature("Week1练习")
class TestWeek1Practice:
    
    @allure.title("练习1: 京东搜索")
    def test_jd_search(self, page):
        base = BasePage(page)
        
        # 访问京东
        base.navigate_to("https://www.jd.com")
        base.wait_for_page_load()
        
        # 搜索手机
        base.fill("#key", "手机")
        base.click(".button")
        
        # 等待搜索结果
        base.wait_for_element_visible(".gl-item")
        
        # 验证标题
        assert "手机" in base.get_page_title()
        base.take_screenshot("jd_search_result")
```

**练习 2**: 访问淘宝，检查首页是否有搜索框和登录按钮

```python
    @allure.title("练习2: 淘宝首页元素检查")
    def test_taobao_elements(self, page):
        base = BasePage(page)
        base.navigate_to("https://www.taobao.com")
        
        # 检查多个元素是否存在
        assert base.is_visible("#q")  # 搜索框
        assert base.is_visible(".site-nav-sign")  # 登录按钮
        assert base.get_text(".site-nav-sign") == "亲，请登录"
```

---

## Day 3-4: 元素定位策略

### 4.1 CSS 选择器详解

```
基础选择器:
  #id          → 按ID选择    → #username
  .class       → 按类选择    → .btn-primary
  tag          → 按标签      → input, button
  [attr]       → 按属性      → [type="submit"]

组合选择器:
  A B          → 后代        → .form input
  A > B        → 直接子元素   → .nav > li
  A + B        → 相邻兄弟     → h1 + p
  A ~ B        → 通用兄弟     → h1 ~ p

伪类选择器:
  :first-child    → 第一个子元素
  :last-child     → 最后一个子元素
  :nth-child(n)   → 第n个子元素
  :hover          → 鼠标悬停状态
  :focus          → 聚焦状态
```

### 4.2 XPath vs CSS 选择器

| 场景 | CSS | XPath | 推荐 |
|------|-----|-------|------|
| 按ID | `#id` | `//*[@id="id"]` | CSS |
| 按Class | `.class` | `//*[@class="class"]` | CSS |
| 按文本 | 不支持 | `//*[text()="文本"]` | XPath |
| 父元素 | 不支持 | `//child/..` | XPath |
| 第N个 | `:nth-child(n)` | `//[n]` | CSS |
| 复杂关系 | 有限 | 强大 | XPath |

### 4.3 Playwright 智能定位

```python
# 按文本定位（Playwright 特有）
page.click("text=登录")
page.click("text=提交订单")

# 按角色定位
page.click("role=button[name='提交']")
page.fill("role=textbox[name='用户名']", "test")

# 按标签定位
page.click("label=同意协议")

# 占位符定位
page.fill("placeholder=请输入手机号", "13800138000")

# 标题定位
page.click("title=查看详情")
```

### 4.4 练习任务

**练习 3**: 使用多种定位方式访问 https://ant.design/components/overview-cn/

```python
    @allure.title("练习3: 多种定位方式")
    def test_ant_design(self, page):
        base = BasePage(page)
        base.navigate_to("https://ant.design/components/overview-cn/")
        base.wait_for_page_load()
        
        # 1. 按文本定位 - 点击"组件总览"
        page.click("text=组件总览")
        
        # 2. 按CSS定位 - 搜索组件
        base.fill("#search-components", "button")
        
        # 3. 按属性定位 - 点击第一个结果
        base.click("[data-keyword='button']")
        
        # 4. 截图验证
        base.take_screenshot("antd_button_doc")
```

---

## Day 5-6: 断言与验证技巧

### 6.1 常用断言方法

```python
# 基础断言
assert "expected" in actual_text
assert element_count == 5
assert is_visible == True

# Playwright 自带断言（推荐）
from playwright.sync_api import expect

# 验证元素可见
expect(page.locator(".success")).to_be_visible()

# 验证文本内容
expect(page.locator(".message")).to_have_text("操作成功")

# 验证包含文本
expect(page.locator("body")).to_contain_text("欢迎")

# 验证URL
expect(page).to_have_url("https://example.com/dashboard")

# 验证标题
expect(page).to_have_title("首页")
```

### 6.2 异步等待策略

```python
# 等待元素出现
base.wait_for_element("#modal", timeout=5000)

# 等待元素可见
base.wait_for_element_visible(".loading-complete")

# 等待元素隐藏
base.wait_for_element_hidden(".spinner")

# 等待网络空闲
page.wait_for_load_state("networkidle")

# 等待特定请求
page.wait_for_response("**/api/data")
```

### 6.3 软断言（多个断言都执行）

```python
import pytest

@pytest.mark.parametrize("selector,expected", [
    ("#title", "商品名称"),
    ("#price", "¥"),
    ("#stock", "有货"),
])
def test_product_info(page, selector, expected):
    """验证商品信息 - 多个断言"""
    base = BasePage(page)
    actual = base.get_text(selector)
    assert expected in actual, f"{selector} 应该包含 {expected}, 实际为 {actual}"
```

### 6.4 练习任务

**练习 4**: 编写一个完整的登录流程测试，包含多重验证

```python
    @allure.title("练习4: 完整登录流程验证")
    def test_complete_login_flow(self, page):
        base = BasePage(page)
        
        # 1. 访问登录页
        base.navigate_to("https://example.com/login")
        base.take_screenshot("login_page")
        
        # 2. 验证登录表单元素存在
        assert base.is_visible("#username")
        assert base.is_visible("#password")
        assert base.is_visible("#login-btn")
        
        # 3. 填写登录信息
        base.fill("#username", "test@example.com")
        base.fill("#password", "TestPass123!")
        base.take_screenshot("login_filled")
        
        # 4. 点击登录
        base.click("#login-btn")
        
        # 5. 等待跳转
        base.wait_for_page_load()
        
        # 6. 多重验证
        assert "dashboard" in base.get_page_url(), "URL应包含dashboard"
        assert base.is_visible(".user-profile"), "应显示用户头像"
        assert base.get_text(".welcome-msg") == "欢迎回来", "欢迎消息正确"
        base.take_screenshot("login_success")
```

---

## Day 7: Allure 报告与综合练习

### 7.1 Allure 装饰器详解

```python
import allure

@allure.epic("电商平台")           # 史诗级别（最大）
@allure.feature("用户模块")        # 功能模块
@allure.story("登录功能")          # 用户故事
@allure.suite("回归测试")          # 测试套件
@allure.severity(allure.severity_level.CRITICAL)  # 严重程度
class TestLogin:
    
    @allure.title("正常登录测试")
    @allure.description("使用正确的用户名密码登录系统")
    @allure.tag("smoke", "regression")
    def test_normal_login(self, page):
        with allure.step("步骤1: 打开登录页"):
            # 操作...
            allure.attach("说明", "访问登录页面")
        
        with allure.step("步骤2: 填写凭证"):
            # 操作...
            allure.attach("用户名", "test@example.com")
        
        with allure.step("步骤3: 验证登录成功"):
            # 断言...
            allure.attach("实际结果", "登录成功")
```

### 7.2 Allure 附件类型

```python
# 附加文本
allure.attach("日志内容", "运行日志", allure.attachment_type.TEXT)

# 附加JSON
allure.attach(json.dumps(data), "接口返回", allure.attachment_type.JSON)

# 附加HTML
allure.attach(html_content, "页面源码", allure.attachment_type.HTML)

# 附加图片（截图）
screenshot = page.screenshot()
allure.attach(screenshot, "失败截图", allure.attachment_type.PNG)

# 附加CSV
allure.attach(csv_data, "测试数据", allure.attachment_type.CSV)
```

### 7.3 综合练习项目

**练习 5**: 完成一个完整的购物流程测试

```python
@allure.epic("电商平台")
@allure.feature("购物流程")
class TestShoppingFlow:
    """Week1 综合练习：完整购物流程"""
    
    @allure.story("浏览商品")
    def test_browse_products(self, page):
        """步骤1: 浏览商品列表"""
        base = BasePage(page)
        
        with allure.step("访问商品列表页"):
            base.navigate_to("https://example-shop.com/products")
            base.wait_for_page_load()
        
        with allure.step("验证商品加载"):
            products = page.locator(".product-card").count()
            assert products > 0, "应该有商品显示"
            allure.attach(f"找到 {products} 个商品", "商品统计")
        
        with allure.step("筛选商品"):
            base.click("[data-filter='electronics']")
            base.wait_for_element_visible(".filtered")
            base.take_screenshot("filtered_products")
    
    @allure.story("商品详情")
    def test_product_detail(self, page):
        """步骤2: 查看商品详情"""
        base = BasePage(page)
        base.navigate_to("https://example-shop.com/products/1")
        
        with allure.step("验证详情页元素"):
            assert base.is_visible(".product-title")
            assert base.is_visible(".product-price")
            assert base.is_visible(".add-to-cart")
            
            price = base.get_text(".product-price")
            assert "¥" in price
            allure.attach(f"商品价格: {price}", "价格信息")
    
    @allure.story("加入购物车")
    def test_add_to_cart(self, page):
        """步骤3: 加入购物车"""
        base = BasePage(page)
        base.navigate_to("https://example-shop.com/products/1")
        
        with allure.step("选择规格"):
            base.click("[data-size='M']")
            base.click("[data-color='red']")
        
        with allure.step("加入购物车"):
            base.click(".add-to-cart")
            base.wait_for_element_visible(".toast-success")
        
        with allure.step("验证成功提示"):
            message = base.get_text(".toast-success")
            assert "已加入购物车" in message
            base.take_screenshot("add_to_cart_success")
```

---

## 📝 Week1 作业清单

完成以下任务才算 Week1 毕业：

- [ ] 独立完成练习 1-5
- [ ] 编写 3 个自己的测试用例（选择任意网站）
- [ ] 生成 Allure 报告并查看
- [ ] 理解 BasePage 的 80% 方法
- [ ] 掌握至少 5 种元素定位方式

---

## 💡 常见问题

**Q: 元素定位总是失败怎么办？**
- 使用 `page.pause()` 暂停调试
- 检查元素是否在 iframe 中
- 等待元素加载完成再操作
- 使用 Playwright 的 Inspector 工具

**Q: 测试运行太慢怎么办？**
- 使用 `headless=True` 无头模式
- 减少 `wait_for_load_state` 等待时间
- 并行运行测试 `pytest -n auto`

**Q: 如何处理弹窗(alert)？**
```python
# 监听并处理弹窗
page.on("dialog", lambda dialog: dialog.accept())
```

---

## 🔗 扩展阅读

- [Playwright 官方文档](https://playwright.dev/python/)
- [CSS 选择器教程](https://www.w3school.com.cn/cssref/css_selectors.asp)
- [Allure 报告指南](https://docs.qameta.io/allure/)

---

**恭喜完成 Week 1！** 你已经掌握了自动化测试的基础技能。继续 Week 2 学习更高级的内容！
