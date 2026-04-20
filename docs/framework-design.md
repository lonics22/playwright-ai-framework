# Python + Playwright + Allure + Browser-Use 自动化测试框架设计

## 1. 框架概述

本框架是一个基于 Python 的现代化 Web 自动化测试框架，融合了传统自动化测试与 AI 驱动测试能力：

- **Playwright**: 高性能浏览器自动化
- **Allure**: 专业级测试报告与可视化
- **Browser-Use**: AI Agent 驱动的智能测试能力
- **多 LLM 支持**: OpenAI、Anthropic、本地 Ollama 等

## 2. 框架核心特性

| 特性 | 说明 |
|------|------|
| 双模式执行 | 支持传统脚本测试 + AI Agent 自然语言测试 |
| 智能元素定位 | AI 辅助元素识别与自我修复定位策略 |
| 视觉回归测试 | 结合截图与 AI 图像比对 |
| 智能失败重试 | AI 分析失败原因并自适应重试 |
| 多浏览器支持 | Chromium/Firefox/WebKit 一键切换 |
| 并发执行 | pytest-xdist 支持多进程并行 |

## 3. 目录结构

```
automation-framework/
├── 📁 config/                          # 配置管理
│   ├── __init__.py
│   ├── settings.py                     # 全局配置
│   ├── env_config.yaml                 # 环境配置（多环境支持）
│   └── browser_config.yaml             # 浏览器配置
│
├── 📁 core/                            # 框架核心
│   ├── __init__.py
│   ├── driver/                         # 浏览器驱动封装
│   │   ├── __init__.py
│   │   ├── playwright_driver.py        # Playwright 基础封装
│   │   └── browser_use_adapter.py      # Browser-Use 适配器
│   ├── ai/                             # AI Agent 模块
│   │   ├── __init__.py
│   │   ├── agent_factory.py            # Agent 工厂（多 LLM 支持）
│   │   ├── custom_tools.py             # 自定义 AI 工具
│   │   └── prompt_templates.py         # 提示词模板
│   ├── elements/                       # 元素定位增强
│   │   ├── __init__.py
│   │   ├── smart_locator.py            # 智能定位器
│   │   └── element_watcher.py          # 元素变更监听
│   └── reporting/                      # 报告增强
│       ├── __init__.py
│       ├── allure_helper.py            # Allure 工具函数
│       └── ai_report_plugin.py         # AI 测试洞察报告
│
├── 📁 pages/                           # 页面对象模型
│   ├── __init__.py
│   ├── base_page.py                    # 基础页面对象
│   ├── ai_page.py                      # AI 增强页面基类
│   └── components/                     # 可复用组件
│       ├── __init__.py
│       ├── header.py
│       └── footer.py
│
├── 📁 tests/                           # 测试用例
│   ├── __init__.py
│   ├── conftest.py                     # pytest 配置与fixture
│   ├── traditional/                    # 传统自动化测试
│   │   ├── __init__.py
│   │   ├── test_login.py
│   │   └── test_checkout.py
│   ├── ai_driven/                      # AI 驱动测试
│   │   ├── __init__.py
│   │   ├── test_natural_language.py
│   │   └── test_self_healing.py
│   └── hybrid/                         # 混合测试（传统+AI）
│       ├── __init__.py
│       └── test_e2e_with_ai.py
│
├── 📁 utils/                           # 工具函数
│   ├── __init__.py
│   ├── screenshot_helper.py
│   ├── data_generator.py
│   └── api_client.py
│
├── 📁 fixtures/                        # 测试数据
│   ├── test_data.yaml
│   └── ai_scenarios/
│       ├── shopping_task.json
│       └── form_filling_task.json
│
├── 📁 reports/                         # 测试报告输出
│   ├── allure-results/
│   ├── allure-report/
│   └── ai-insights/
│
├── 📁 scripts/                         # 辅助脚本
│   ├── run_tests.sh
│   ├── run_ai_tests.sh
│   └── generate_report.sh
│
├── .env.example                        # 环境变量示例
├── pytest.ini                          # pytest 配置
├── requirements.txt                    # 依赖管理
├── requirements-dev.txt                # 开发依赖
└── README.md
```

## 4. 核心模块设计

### 4.1 Browser-Use 适配器

```python
# core/driver/browser_use_adapter.py
from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI

class AIAgentAdapter:
    """Browser-Use 适配器 - 集成 AI Agent 能力"""

    def __init__(self, llm_provider="openai", headless=False):
        self.browser = Browser(headless=headless)
        self.llm = self._create_llm(llm_provider)

    async def execute_task(self, task: str, context: dict = None):
        """
        使用自然语言执行测试任务

        Args:
            task: 自然语言描述的任务
            context: 额外的上下文信息
        """
        agent = Agent(
            task=task,
            llm=self.llm,
            browser=self.browser,
            use_vision=True,  # 启用视觉能力
        )
        return await agent.run()

    def _create_llm(self, provider: str):
        """支持多 LLM 后端"""
        llm_map = {
            "openai": ChatOpenAI(model="gpt-4o"),
            "anthropic": ChatAnthropic(model="claude-3-5-sonnet"),
            "local": ChatOllama(model="llama3.2"),
        }
        return llm_map.get(provider)
```

### 4.2 双模式页面对象

```python
# pages/ai_page.py
from playwright.sync_api import Page
from core.driver.browser_use_adapter import AIAgentAdapter

class AIPage:
    """AI 增强的基础页面对象 - 支持传统和 AI 两种模式"""

    def __init__(self, page: Page, ai_adapter: AIAgentAdapter = None):
        self.page = page
        self.ai = ai_adapter
        self._smart_mode = ai_adapter is not None

    # ========== 传统模式方法 ==========
    def click(self, selector: str):
        """传统点击操作"""
        self.page.click(selector)

    def fill(self, selector: str, value: str):
        """传统输入操作"""
        self.page.fill(selector, selector)

    # ========== AI 模式方法 ==========
    async def ai_click(self, element_description: str):
        """AI 驱动的点击 - 通过自然语言描述定位元素"""
        if not self._smart_mode:
            raise RuntimeError("AI adapter not initialized")

        task = f"在页面上找到 '{element_description}' 并点击它"
        return await self.ai.execute_task(task)

    async def ai_fill_form(self, form_data: dict):
        """AI 驱动的表单填写"""
        fields = ", ".join([f"{k}={v}" for k, v in form_data.items()])
        task = f"填写表单，字段值: {fields}"
        return await self.ai.execute_task(task)

    async def ai_verify(self, expectation: str):
        """AI 驱动的验证 - 自然语言断言"""
        task = f"验证页面是否符合预期: {expectation}"
        result = await self.ai.execute_task(task)
        return result.success
```

### 4.3 智能元素定位器

```python
# core/elements/smart_locator.py
from typing import List, Optional
from playwright.sync_api import Page, Locator
import hashlib

class SmartLocator:
    """智能元素定位器 - 结合传统定位与 AI 视觉定位"""

    def __init__(self, page: Page, ai_adapter=None):
        self.page = page
        self.ai = ai_adapter
        self.element_registry = {}  # 元素历史定位缓存

    def find(self, selector: str, fallback_description: str = None) -> Locator:
        """
        智能查找元素
        1. 优先使用传统选择器
        2. 失败时尝试备用选择器
        3. 启用 AI 时，使用 AI 视觉定位
        """
        try:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                return locator.first
        except:
            pass

        # 尝试备用策略
        if fallback_description and self.ai:
            return self._ai_find(fallback_description)

        raise ElementNotFoundException(f"无法定位元素: {selector}")

    def _ai_find(self, description: str):
        """使用 AI 通过视觉描述定位元素"""
        # 截图 + AI 分析获取坐标
        # 返回 Playwright Locator
        pass

    def register_element(self, name: str, selectors: List[str]):
        """注册元素多维度特征，用于自我修复"""
        self.element_registry[name] = {
            "selectors": selectors,
            "checksum": None,  # 元素内容哈希
            "last_success": None,  # 最后成功的选择器
        }
```

### 4.4 AI 驱动测试示例

```python
# tests/ai_driven/test_natural_language.py
import pytest
import allure

@pytest.mark.ai
@allure.feature("AI 驱动测试")
@allure.story("自然语言任务执行")
class TestNaturalLanguage:
    """自然语言描述的测试用例"""

    @allure.title("完成完整购物流程")
    async def test_shopping_journey(self, ai_agent, page):
        """使用自然语言描述复杂的端到端场景"""

        # 传统方式：打开页面
        await page.goto("https://example-shop.com")

        # AI 方式：执行复杂任务
        result = await ai_agent.execute_task("""
            完成一次完整的购物流程：
            1. 在搜索框输入 "wireless headphones"
            2. 选择第一个商品加入购物车
            3. 进入购物车结算
            4. 使用测试信用卡信息完成支付
            5. 验证订单确认页面显示成功消息
        """)

        # Allure 报告附加 AI 执行详情
        allure.attach(
            result.execution_log,
            name="AI 执行日志",
            attachment_type=allure.attachment_type.TEXT
        )

        assert result.success

    @allure.title("自适应表单填写")
    async def test_self_healing_form(self, ai_agent):
        """当页面结构变化时，AI 自动适应"""

        result = await ai_agent.execute_task(
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

        assert result.success
```

### 4.5 混合模式测试

```python
# tests/hybrid/test_e2e_with_ai.py
import pytest
import allure
from pages.login_page import LoginPage
from pages.checkout_page import CheckoutPage

@pytest.mark.hybrid
@allure.feature("混合模式测试")
class TestE2EWithAI:
    """结合传统 POM 与 AI 能力的测试"""

    @allure.title("登录后 AI 完成复杂操作")
    async def test_login_then_ai_task(self, page, ai_adapter):
        # 传统方式：稳定的登录流程
        login_page = LoginPage(page)
        login_page.login("user@test.com", "password123")

        # AI 方式：处理复杂、易变的业务流程
        result = await ai_adapter.execute_task("""
            在个人中心完成以下操作：
            1. 找到订单历史标签并点击
            2. 找到最近一笔未评价的订单
            3. 为该订单添加五星好评，评论写 "Great product!"
            4. 上传一张测试图片作为评价配图
            5. 提交评价并确认成功
        """)

        assert result.success
```

## 5. Fixture 设计（conftest.py）

```python
# tests/conftest.py
import pytest
import pytest_asyncio
from playwright.sync_api import sync_playwright
from core.driver.browser_use_adapter import AIAgentAdapter
from core.reporting.allure_helper import AllureHelper

@pytest.fixture(scope="session")
def browser_config():
    """浏览器全局配置"""
    return {
        "headless": False,
        "slow_mo": 50,
        "viewport": {"width": 1920, "height": 1080}
    }

@pytest.fixture(scope="function")
def page(browser_config):
    """每个测试的独立页面实例"""
    with sync_playwright() as p:
        browser = p.chromium.launch(**browser_config)
        context = browser.new_context()
        page = context.new_page()

        # 失败自动截图
        yield page

        # 测试结束后的清理与报告
        browser.close()

@pytest.fixture(scope="function")
def ai_agent(page, request):
    """AI Agent fixture - 按需初始化"""
    marker = request.node.get_closest_marker("ai")
    if marker:
        adapter = AIAgentAdapter(
            llm_provider=marker.kwargs.get("llm", "openai"),
            headless=False
        )
        return adapter
    return None

@pytest.fixture(scope="function")
def smart_page(page, ai_agent):
    """智能页面对象 - 自动选择传统或 AI 模式"""
    from pages.ai_page import AIPage
    return AIPage(page, ai_agent)

# pytest hook - 失败时附加更多信息
def pytest_runtest_makereport(item, call):
    """测试失败时自动附加截图和 AI 分析"""
    if call.when == "call" and call.excinfo is not None:
        # 传统截图
        if hasattr(item.instance, "page"):
            screenshot = item.instance.page.screenshot()
            allure.attach(screenshot, "失败截图", allure.attachment_type.PNG)

        # AI 失败分析（如启用）
        if item.get_closest_marker("ai"):
            analysis = ai_analyze_failure(call.excinfo.value)
            allure.attach(analysis, "AI 失败分析", allure.attachment_type.TEXT)
```

## 6. Allure 报告集成

```python
# core/reporting/allure_helper.py
import allure
from allure_commons.types import AttachmentType
import json

class AllureHelper:
    """Allure 报告增强工具"""

    @staticmethod
    def attach_ai_execution(task: str, result: dict):
        """附加 AI 执行详情到报告"""
        allure.attach(
            json.dumps({
                "task": task,
                "success": result.get("success"),
                "steps": result.get("steps", []),
                "duration": result.get("duration"),
            }, indent=2, ensure_ascii=False),
            name="AI 执行详情",
            attachment_type=AttachmentType.JSON
        )

    @staticmethod
    def attach_screenshot_with_annotation(page, annotation: str):
        """截图并附加标注"""
        # 在截图上绘制 AI 关注的区域
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name=f"截图 - {annotation}",
            attachment_type=AttachmentType.PNG
        )
```

## 7. 配置管理

```yaml
# config/env_config.yaml
default:
  base_url: "https://staging.example.com"
  api_base: "https://api.staging.example.com"
  timeout: 30000

production:
  base_url: "https://example.com"
  api_base: "https://api.example.com"
  timeout: 10000

ai:
  default_provider: "openai"
  vision_enabled: true
  max_iterations: 50
  providers:
    openai:
      model: "gpt-4o"
      temperature: 0.1
    anthropic:
      model: "claude-3-5-sonnet"
    local:
      model: "llama3.2"
      base_url: "http://localhost:11434"
```

## 8. 运行命令设计

```bash
# 运行所有传统测试
pytest tests/traditional/ -v --alluredir=reports/allure-results

# 运行 AI 驱动测试
pytest tests/ai_driven/ -v -m ai --llm=openai

# 运行混合测试
pytest tests/hybrid/ -v -m hybrid

# 并发执行（传统测试）
pytest tests/traditional/ -n auto --dist=loadgroup

# 生成 Allure 报告
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report

# AI 测试并附加执行洞察
pytest tests/ai_driven/ --ai-insights=reports/ai-insights/
```

## 9. pytest.ini 配置

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    ai: 标记 AI 驱动测试（需要 LLM 配置）
    hybrid: 标记混合模式测试
    slow: 标记慢速测试
    smoke: 标记冒烟测试
    regression: 标记回归测试

addopts =
    -v
    --tb=short
    --strict-markers
    --alluredir=reports/allure-results

asyncio_mode = auto
asyncio_default_fixture_loop_scope = function
```

## 10. 依赖文件

```txt
# requirements.txt
# 核心依赖
pytest>=8.0.0
pytest-asyncio>=0.23.0
pytest-xdist>=3.5.0
playwright>=1.41.0
allure-pytest>=2.13.0
PyYAML>=6.0.1
python-dotenv>=1.0.0

# Browser-Use 及 AI 相关
browser-use>=0.1.0
langchain>=0.1.0
langchain-openai>=0.0.5
langchain-anthropic>=0.1.0
langchain-ollama>=0.0.1

# 可选：增强功能
pillow>=10.0.0  # 图像处理
requests>=2.31.0  # API 调用
faker>=22.0.0  # 测试数据生成
```

## 11. 扩展能力

### 11.1 自定义 AI 工具

```python
# core/ai/custom_tools.py
from browser_use import tool

@tool
def verify_element_text(context, selector: str, expected: str) -> bool:
    """自定义工具：验证元素文本"""
    element = context.page.locator(selector)
    actual = element.text_content()
    return actual == expected

@tool
def extract_table_data(context, table_selector: str) -> list:
    """自定义工具：提取表格数据"""
    rows = context.page.locator(f"{table_selector} tr").all()
    return [row.locator("td").all_text_contents() for row in rows]
```

### 11.2 自我修复定位策略

```python
# core/elements/self_healing.py
class SelfHealingLocator:
    """当元素定位失败时，AI 自动寻找替代方案"""

    async def find_with_healing(self, failed_selector: str, page) -> Locator:
        # 1. 截图当前页面
        screenshot = page.screenshot()

        # 2. AI 分析寻找相似元素
        alternative = await self.ai.find_similar_element(
            screenshot=screenshot,
            original_selector=failed_selector
        )

        # 3. 返回新定位器
        return page.locator(alternative)
```

## 12. 实施路线图

| 阶段 | 内容 | 优先级 |
|------|------|--------|
| Phase 1 | 基础框架搭建、Playwright + Allure 集成 | P0 |
| Phase 2 | Browser-Use 集成、AI Agent 适配器 | P0 |
| Phase 3 | 智能定位器、自我修复机制 | P1 |
| Phase 4 | 混合测试模式、AI 报告增强 | P1 |
| Phase 5 | 多 LLM 支持、自定义工具扩展 | P2 |

