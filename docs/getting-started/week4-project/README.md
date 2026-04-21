# Week 4: 实战项目 - 完整自动化测试解决方案

> 🎯 本周目标：完成一个完整的实战项目，将所学知识应用到真实场景中，搭建企业级测试框架

---

## 📚 学习路线图

```
Day 1-2: 项目选型与架构设计
Day 3-4: 核心功能实现
Day 5-6: CI/CD 集成与自动化
Day 7:    项目总结与优化
```

---

## Day 1-2: 项目选型与架构设计

### 2.1 选择一个真实项目

**推荐项目选项：**

1. **电商网站测试**（推荐新手）
   - 功能丰富：登录、搜索、购物车、订单
   - 页面结构清晰
   - 易于理解业务流程

2. **企业后台管理系统**
   - 复杂的表单操作
   - 数据表格验证
   - 权限控制测试

3. **社交类应用**
   - 实时交互测试
   - 多媒体内容验证
   - 复杂用户流程

### 2.2 项目架构设计

```
my-test-project/                        # 项目根目录
├── 📁 config/                          # 配置管理
│   ├── __init__.py
│   ├── settings.py                     # 全局配置
│   ├── test_env.yaml                   # 测试环境配置
│   └── browser.yaml                    # 浏览器配置
│
├── 📁 pages/                           # 页面对象
│   ├── __init__.py
│   ├── base_page.py                    # 基础页面对象
│   ├── login_page.py                   # 登录页
│   ├── home_page.py                    # 首页
│   ├── product_page.py                 # 商品页
│   ├── cart_page.py                    # 购物车
│   ├── checkout_page.py                # 结算页
│   └── components/                     # 公共组件
│       ├── __init__.py
│       ├── header.py                   # 页头
│       ├── footer.py                   # 页脚
│       └── sidebar.py                  # 侧边栏
│
├── 📁 tests/                           # 测试用例
│   ├── __init__.py
│   ├── conftest.py                     # pytest配置
│   ├── test_login.py                   # 登录测试
│   ├── test_product.py                 # 商品测试
│   ├── test_cart.py                    # 购物车测试
│   ├── test_checkout.py                # 结算测试
│   ├── test_e2e.py                     # 端到端测试
│   └── test_api.py                     # API测试
│
├── 📁 utils/                           # 工具函数
│   ├── __init__.py
│   ├── data_generator.py               # 数据生成
│   ├── api_client.py                   # API客户端
│   └── helpers.py                      # 辅助函数
│
├── 📁 fixtures/                        # 测试数据
│   ├── users.json                      # 用户数据
│   ├── products.json                   # 商品数据
│   └── test_data.yaml                  # 通用数据
│
├── 📁 reports/                         # 测试报告
│   ├── allure-results/                 # Allure结果
│   └── ai-insights/                    # AI洞察报告
│
├── 📁 scripts/                         # 脚本
│   ├── run_tests.sh                    # 运行测试
│   ├── run_smoke.sh                    # 冒烟测试
│   └── generate_report.sh              # 生成报告
│
├── 📁 docs/                            # 项目文档
│   └── README.md                       # 项目说明
│
├── 📄 .env                             # 环境变量
├── 📄 pytest.ini                       # pytest配置
├── 📄 requirements.txt                 # 依赖
└── 📄 README.md                        # 项目文档
```

### 2.3 核心配置文件

```yaml
# config/test_env.yaml
dev:
  base_url: "https://dev.example-shop.com"
  api_url: "https://api-dev.example-shop.com"
  db_host: "dev-db.example.com"
  timeout: 30000

staging:
  base_url: "https://staging.example-shop.com"
  api_url: "https://api-staging.example-shop.com"
  db_host: "staging-db.example.com"
  timeout: 20000

production:
  base_url: "https://example-shop.com"
  api_url: "https://api.example-shop.com"
  timeout: 10000
```

---

## Day 3-4: 核心功能实现

### 4.1 实现核心页面对象

```python
# pages/product_page.py
from pages.base_page import BasePage
from playwright.sync_api import expect


class ProductPage(BasePage):
    """商品详情页"""
    
    # 选择器定义
    PRODUCT_NAME = "h1.product-name"
    PRODUCT_PRICE = ".product-price .current-price"
    PRODUCT_IMAGE = ".product-main-image img"
    ADD_TO_CART_BTN = "#add-to-cart"
    QUANTITY_INPUT = "#quantity"
    SIZE_OPTIONS = ".size-option"
    COLOR_OPTIONS = ".color-option"
    STOCK_STATUS = ".stock-status"
    REVIEWS_TAB = "#reviews-tab"
    RELATED_PRODUCTS = ".related-product"
    
    def get_product_name(self) -> str:
        """获取商品名称"""
        return self.get_text(self.PRODUCT_NAME)
    
    def get_product_price(self) -> float:
        """获取商品价格"""
        price_text = self.get_text(self.PRODUCT_PRICE)
        # 解析价格文本，如 "¥1,299.00" -> 1299.00
        return float(price_text.replace('¥', '').replace(',', ''))
    
    def select_size(self, size: str):
        """选择尺码"""
        size_selector = f"{self.SIZE_OPTIONS}[data-size='{size}']"
        self.click(size_selector)
        return self
    
    def select_color(self, color: str):
        """选择颜色"""
        color_selector = f"{self.COLOR_OPTIONS}[data-color='{color}']"
        self.click(color_selector)
        return self
    
    def set_quantity(self, quantity: int):
        """设置数量"""
        self.clear(self.QUANTITY_INPUT)
        self.fill(self.QUANTITY_INPUT, str(quantity))
        return self
    
    def add_to_cart(self):
        """加入购物车"""
        self.click(self.ADD_TO_CART_BTN)
        # 等待成功提示
        self.wait_for_element_visible(".toast-success", timeout=5000)
        return self
    
    def is_in_stock(self) -> bool:
        """检查是否有库存"""
        status = self.get_text(self.STOCK_STATUS)
        return "有货" in status or "In Stock" in status
    
    def go_to_reviews(self):
        """切换到评价标签"""
        self.click(self.REVIEWS_TAB)
        self.wait_for_element_visible(".review-item")
        return self
    
    def get_related_products(self) -> list:
        """获取相关商品列表"""
        return self.smart_locator.find_all(self.RELATED_PRODUCTS)
```

### 4.2 实现测试用例

```python
# tests/test_product.py
import pytest
import allure
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@allure.epic("商品模块")
@allure.feature("商品详情")
class TestProduct:
    """商品相关测试"""
    
    @pytest.fixture
    def product_page(self, page):
        """商品页 fixture"""
        product_page = ProductPage(page)
        product_page.navigate_to("https://example-shop.com/products/1")
        return product_page
    
    @allure.story("商品信息展示")
    @allure.title("验证商品基本信息")
    def test_product_info_display(self, product_page):
        """测试商品信息正确显示"""
        with allure.step("验证商品名称"):
            name = product_page.get_product_name()
            assert len(name) > 0
            allure.attach(name, "商品名称")
        
        with allure.step("验证商品价格"):
            price = product_page.get_product_price()
            assert price > 0
            allure.attach(f"¥{price}", "商品价格")
        
        with allure.step("验证商品图片"):
            assert product_page.is_visible(product_page.PRODUCT_IMAGE)
    
    @allure.story("加入购物车")
    @allure.title("验证加入购物车功能")
    def test_add_to_cart(self, product_page, page):
        """测试添加商品到购物车"""
        with allure.step("选择规格"):
            if product_page.is_visible(product_page.SIZE_OPTIONS):
                product_page.select_size("M")
            if product_page.is_visible(product_page.COLOR_OPTIONS):
                product_page.select_color("black")
        
        with allure.step("设置数量"):
            product_page.set_quantity(2)
        
        with allure.step("加入购物车"):
            product_name = product_page.get_product_name()
            product_price = product_page.get_product_price()
            product_page.add_to_cart()
        
        with allure.step("验证购物车"):
            cart = CartPage(page)
            cart.navigate()
            assert cart.has_product(product_name)
            assert cart.get_product_quantity(product_name) == 2
```

### 4.3 端到端测试

```python
# tests/test_e2e.py
import pytest
import allure
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage


@allure.epic("端到端测试")
@allure.feature("完整购物流程")
class TestE2EShopping:
    """端到端购物测试"""
    
    @pytest.fixture
    def logged_in_user(self, page, env_config):
        """登录用户 fixture"""
        login = LoginPage(page)
        login.navigate()
        login.login("test@example.com", "TestPass123!")
        yield page
    
    @allure.title("完整购物到支付流程")
    def test_complete_purchase_flow(self, logged_in_user):
        """测试完整购物流程"""
        page = logged_in_user
        
        with allure.step("1. 浏览首页"):
            home = HomePage(page)
            home.navigate()
            home.wait_for_page_load()
            allure.attach(page.url, "首页URL")
        
        with allure.step("2. 选择商品"):
            product = home.click_recommended_product(index=0)
            product_name = product.get_product_name()
            product_price = product.get_product_price()
            allure.attach(product_name, "选中商品")
            allure.attach(f"¥{product_price}", "商品价格")
        
        with allure.step("3. 添加到购物车"):
            product.add_to_cart()
        
        with allure.step("4. 结算"):
            cart = CartPage(page)
            cart.navigate()
            checkout = cart.proceed_to_checkout()
        
        with allure.step("5. 填写收货信息"):
            checkout.fill_shipping_info(
                name="张三",
                phone="13800138000",
                address="北京市朝阳区xxx街道",
                city="北京",
                postcode="100000"
            )
        
        with allure.step("6. 选择支付方式"):
            checkout.select_payment_method("alipay")
        
        with allure.step("7. 提交订单"):
            order = checkout.place_order()
            order_number = order.get_order_number()
            allure.attach(order_number, "订单号")
            assert order.is_order_successful()
```

---

## Day 5-6: CI/CD 集成与自动化

### 5.1 GitHub Actions 配置

```yaml
# .github/workflows/test.yml
name: Automated Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]
  schedule:
    # 每天晚上 2 点运行
    - cron: '0 2 * * *'

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout code
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        playwright install chromium
    
    - name: Run smoke tests
      run: |
        pytest tests/ -m smoke -v --alluredir=reports/allure-results
      env:
        TEST_ENV: staging
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
    
    - name: Run regression tests
      if: github.ref == 'refs/heads/main'
      run: |
        pytest tests/ -m regression -v --alluredir=reports/allure-results
    
    - name: Generate Allure Report
      uses: simple-elf/allure-report-action@master
      with:
        allure_results: reports/allure-results
        allure_history: allure-history
    
    - name: Upload Report
      uses: actions/upload-artifact@v3
      with:
        name: test-report
        path: reports/
```

### 5.2 Jenkins 配置

```groovy
// Jenkinsfile
pipeline {
    agent any
    
    environment {
        TEST_ENV = 'staging'
        PYTHON_VERSION = '3.11'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup') {
            steps {
                sh '''
                    python -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                    playwright install chromium
                '''
            }
        }
        
        stage('Smoke Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    pytest tests/ -m smoke -v --alluredir=reports/allure-results
                '''
            }
        }
        
        stage('Full Tests') {
            when {
                branch 'main'
            }
            steps {
                sh '''
                    source venv/bin/activate
                    pytest tests/ -v --alluredir=reports/allure-results
                '''
            }
        }
        
        stage('Generate Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: 'reports/allure-results']]
                ])
            }
        }
    }
    
    post {
        always {
            // 发送测试结果邮件
            emailext(
                subject: "Test Results: ${env.JOB_NAME} - ${env.BUILD_NUMBER}",
                body: "Tests completed. Check Allure report.",
                to: "${env.CHANGE_AUTHOR_EMAIL}"
            )
        }
    }
}
```

### 5.3 Docker 支持

```dockerfile
# Dockerfile
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制测试代码
COPY . .

# 运行测试
CMD ["pytest", "tests/", "-v"]
```

```yaml
# docker-compose.yml
version: '3'
services:
  tests:
    build: .
    environment:
      - TEST_ENV=staging
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./reports:/app/reports
    command: pytest tests/ -v --alluredir=reports/allure-results
```

---

## Day 7: 项目总结与优化

### 7.1 性能优化建议

```python
# 1. 并行执行测试
# pytest.ini
[pytest]
addopts = -n auto --dist=loadgroup

# 2. 失败重试
# pip install pytest-rerunfailures
# pytest.ini
addopts = --reruns 2 --reruns-delay 1

# 3. 选择性执行
# 只运行修改文件相关的测试
# pytest --testmon

# 4. 截图优化（只在失败时截图）
# conftest.py
def pytest_runtest_makereport(item, call):
    if call.when == "call" and call.excinfo is not None:
        # 失败时才截图
        pass
```

### 7.2 项目检查清单

**代码质量：**
- [ ] 所有页面对象都有完整的文档字符串
- [ ] 测试用例有清晰的 Arrange-Act-Assert 结构
- [ ] 使用了类型注解
- [ ] 代码通过 flake8/pylint 检查

**测试覆盖：**
- [ ] 核心业务流程都有端到端测试
- [ ] 至少 80% 的页面有自动化测试
- [ ] 包含正例和反例测试
- [ ] 有性能基准测试

**报告与监控：**
- [ ] Allure 报告能正常生成
- [ ] 测试失败时自动截图和记录日志
- [ ] CI/CD 集成完成
- [ ] 有测试成功率监控

### 7.3 项目交付物

```
📦 项目交付物清单：
├── 源代码
│   ├── pages/              ✓ 页面对象
│   ├── tests/              ✓ 测试用例
│   └── utils/              ✓ 工具函数
├── 文档
│   ├── README.md           ✓ 项目说明
│   ├── API.md              ✓ 接口文档
│   └── TEST_PLAN.md        ✓ 测试计划
├── 配置
│   ├── pytest.ini          ✓ pytest配置
│   ├── .github/workflows/  ✓ CI配置
│   └── Dockerfile          ✓ Docker配置
└── 报告
    ├── test-report.html    ✓ 测试报告
    └── coverage-report/    ✓ 覆盖率报告
```

---

## 📝 Week 4 毕业项目要求

完成以下项目才能毕业：

1. **选择一个真实网站**，完成以下测试：
   - [ ] 用户认证（登录/注册/退出）
   - [ ] 核心业务（搜索/浏览/购买）
   - [ ] 至少 3 个端到端流程测试

2. **页面对象设计**：
   - [ ] 至少 5 个页面对象类
   - [ ] 至少 2 个可复用组件
   - [ ] 使用 SmartLocator 智能定位

3. **测试套件**：
   - [ ] 至少 20 个测试用例
   - [ ] 包含传统测试和 AI 测试
   - [ ] 有 smoke、regression 标记

4. **CI/CD 集成**：
   - [ ] GitHub Actions 或 Jenkins 配置
   - [ ] 自动触发测试运行
   - [ ] 测试报告自动归档

5. **文档完善**：
   - [ ] README 文档
   - [ ] 测试计划文档
   - [ ] 项目演示视频（可选）

---

## 🎉 课程总结

**4周学习路径回顾：**

```
Week 1: 基础巩固
  ├─ BasePage 核心方法
  ├─ 元素定位策略
  ├─ 断言与验证
  └─ Allure 报告

Week 2: 进阶提升
  ├─ 页面对象模式 (POM)
  ├─ SmartLocator 智能定位
  ├─ Self-Healing 自我修复
  └─ 完整测试框架搭建

Week 3: AI 能力
  ├─ AI 环境配置
  ├─ 自然语言测试
  ├─ 混合模式实践
  └─ AI 测试最佳实践

Week 4: 实战项目
  ├─ 项目架构设计
  ├─ 核心功能实现
  ├─ CI/CD 集成
  └─ 企业级测试方案
```

**你现在已经掌握了：**
✅ 传统自动化测试技能
✅ 页面对象模式设计
✅ 智能元素定位与自愈
✅ AI 驱动测试能力
✅ 企业级测试框架搭建
✅ CI/CD 持续集成

---

## 🚀 下一步建议

1. **深入学习**
   - 学习 Playwright 高级特性（网络拦截、移动端测试）
   - 学习性能测试（Locust、JMeter）
   - 学习安全测试（OWASP、渗透测试）

2. **参与开源**
   - 为 Playwright 贡献代码
   - 参与测试框架开源项目
   - 分享自己的测试工具

3. **职业发展**
   - 考取相关认证（ISTQB）
   - 建立个人技术博客
   - 参加技术社区分享

---

**🎊 恭喜你完成全部课程！** 

你已经从一个自动化测试小白成长为具备企业级测试能力的工程师。继续保持学习的热情，在自动化测试的道路上越走越远！

欢迎加入我们的社区，与更多测试工程师交流学习！
