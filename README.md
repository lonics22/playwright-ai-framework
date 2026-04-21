# Playwright AI 自动化测试框架

🎭 AI 增强的自动化测试框架 - 基于 Python + Playwright + Allure + browser-use

## 🌟 核心特性

- **双模式执行**：传统脚本测试 + AI Agent 自然语言测试
- **智能元素定位**：AI 辅助元素识别与自我修复定位策略
- **多 LLM 支持**：OpenAI GPT-4o、Anthropic Claude 3.5、本地 Ollama
- **专业报告**：Allure 专业级测试报告与 AI 洞察报告
- **多浏览器支持**：Chromium/Firefox/WebKit 一键切换
- **并发执行**：pytest-xdist 支持多进程并行

## 📁 项目结构

```
playwright-ai-framework/
├── config/                    # 配置管理
│   ├── settings.py            # 全局配置
│   ├── env_config.yaml        # 环境配置（多环境支持）
│   └── browser_config.yaml    # 浏览器配置
│
├── core/                      # 框架核心
│   ├── driver/               # 浏览器驱动封装
│   │   ├── playwright_driver.py
│   │   └── browser_use_adapter.py
│   ├── ai/                   # AI Agent 模块
│   │   ├── agent_factory.py
│   │   ├── prompt_templates.py
│   │   └── custom_tools.py
│   ├── elements/             # 元素定位增强
│   │   ├── smart_locator.py
│   │   ├── element_watcher.py
│   │   └── self_healing.py
│   └── reporting/            # 报告增强
│       ├── allure_helper.py
│       └── ai_report_plugin.py
│
├── pages/                     # 页面对象模型
│   ├── base_page.py          # 基础页面对象
│   ├── ai_page.py            # AI 增强页面基类
│   └── components/           # 可复用组件
│       ├── header.py
│       └── footer.py
│
├── tests/                     # 测试用例
│   ├── conftest.py           # pytest fixtures
│   ├── traditional/          # 传统自动化测试
│   ├── ai_driven/            # AI 驱动测试
│   └── hybrid/               # 混合测试
│
├── utils/                     # 工具函数
│   ├── screenshot_helper.py
│   ├── data_generator.py
│   └── api_client.py
│
├── fixtures/                  # 测试数据
│   ├── test_data.yaml
│   └── ai_scenarios/
│
├── scripts/                   # 辅助脚本
│   ├── run_tests.sh
│   ├── run_ai_tests.sh
│   └── generate_report.sh
│
├── docs/                      # 设计文档
├── pytest.ini                # pytest 配置
├── requirements.txt          # 依赖管理
└── .env.example              # 环境变量示例
```

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Git

### 安装

```bash
# 克隆仓库
git clone https://github.com/your-username/playwright-ai-framework.git
cd playwright-ai-framework

# 创建虚拟环境
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
playwright install chromium

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入必要的 API 密钥
```

### 运行测试

```bash
# 运行传统测试
./scripts/run_tests.sh

# 运行 AI 驱动测试（需要配置 LLM API Key）
./scripts/run_ai_tests.sh

# 运行混合测试
pytest tests/hybrid/ -v -m hybrid

# 生成 Allure 报告
./scripts/generate_report.sh --serve
```

## 🤖 AI 模式说明

框架支持三种 AI 运行模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `assist` | AI 只给建议，不直接执行 | 生产环境默认 |
| `semi-auto` | AI 可执行白名单内的动作 | 混合测试场景 |
| `agent` | AI 完全自主探索 | 探索式测试 |

配置 AI 模式：

```bash
export AI_MODE=assist
export OPENAI_API_KEY=sk-xxx
export ANTHROPIC_API_KEY=sk-ant-xxx
```

## 💻 使用示例

### 传统测试模式

```python
# tests/traditional/test_login.py
import allure
from pages.base_page import BasePage

@allure.feature("用户认证")
class TestLogin:
    @allure.title("成功登录")
    def test_successful_login(self, page):
        base_page = BasePage(page)
        base_page.navigate_to("https://example.com/login")
        base_page.fill("#username", "test@example.com")
        base_page.fill("#password", "password123")
        base_page.click("button[type='submit']")
        assert "dashboard" in base_page.get_page_url()
```

### AI 驱动测试模式

```python
# tests/ai_driven/test_natural_language.py
import pytest
import allure

@pytest.mark.ai
@allure.feature("AI 驱动测试")
class TestNaturalLanguage:
    @allure.title("完成购物流程")
    async def test_shopping_journey(self, async_ai_agent, async_page):
        await async_page.goto("https://example-shop.com")

        result = await async_ai_agent.execute_task("""
            完成一次完整的购物流程：
            1. 在搜索框输入 "wireless headphones"
            2. 选择第一个商品加入购物车
            3. 进入购物车结算
            4. 完成支付流程
            5. 验证订单确认页面
        """)

        assert result.success
```

### 混合测试模式

```python
# tests/hybrid/test_e2e_with_ai.py
import pytest
import allure

@pytest.mark.hybrid
@allure.feature("混合模式测试")
class TestE2EWithAI:
    @allure.title("登录后 AI 完成复杂操作")
    async def test_login_then_ai_task(self, async_page, async_ai_agent):
        # 传统方式：稳定的登录流程
        base_page = BasePage(async_page)
        base_page.navigate_to("https://example-shop.com/login")
        base_page.login("user@test.com", "password123")

        # AI 方式：处理复杂、易变的业务流程
        result = await async_ai_agent.execute_task("""
            在个人中心完成以下操作：
            1. 找到订单历史标签并点击
            2. 找到最近一笔未评价的订单
            3. 为该订单添加五星好评
            4. 提交评价并确认成功
        """)

        assert result.success
```

### 使用 AI 增强页面对象

```python
# 使用 AIPage 双模式页面对象
from pages.ai_page import AIPage

async def test_with_ai_page(self, smart_page):
    # 传统模式操作
    smart_page.navigate_to("https://example.com")
    smart_page.click("#login-link")

    # AI 模式操作
    await smart_page.ai_fill_form({
        "username": "testuser",
        "email": "test@example.com",
        "password": "TestPass123!"
    })

    # AI 验证
    is_success = await smart_page.ai_verify("页面显示注册成功消息")
    assert is_success
```

## 🔧 核心模块

### Browser-Use 适配器

支持多 LLM 提供商的 AI Agent 适配器：

```python
from core.driver.browser_use_adapter import AIAgentAdapter

# 创建适配器
adapter = AIAgentAdapter(llm_provider="openai", headless=False)

# 执行自然语言任务
result = await adapter.execute_task("找到搜索框并搜索 'laptop'")

# 完成后关闭
await adapter.close()
```

### 智能元素定位器

结合传统定位与 AI 视觉定位：

```python
from core.elements.smart_locator import SmartLocator

smart_locator = SmartLocator(page, ai_adapter)

# 智能查找元素
element = smart_locator.find(
    selector="#submit-button",
    fallback_description="蓝色提交按钮"
)
```

### 自我修复定位

当元素定位失败时自动寻找替代方案：

```python
from core.elements.self_healing import SelfHealingLocator

healer = SelfHealingLocator(page, ai_adapter)

# 使用自我修复查找元素
element = healer.find_with_healing(
    failed_selector="#old-button-id",
    element_description="提交按钮"
)
```

### 数据生成工具

生成测试数据：

```python
from utils.data_generator import generate_user, generate_order

# 生成用户数据
user = generate_user()
print(user)  # {'username': '...', 'email': '...', ...}

# 生成订单数据
order = generate_order()
print(order)  # {'order_id': '...', 'items': [...], ...}
```

## ⚙️ 配置说明

### 环境配置 (config/env_config.yaml)

```yaml
default:
  base_url: "https://staging.example.com"
  timeout: 30000

production:
  base_url: "https://example.com"
  timeout: 10000

ai:
  default_provider: "openai"
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

### 浏览器配置 (config/browser_config.yaml)

```yaml
chromium:
  headless: false
  slow_mo: 50
  viewport:
    width: 1920
    height: 1080
```

## 📊 报告生成

### Allure 报告

```bash
# 生成并打开报告
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
```

### AI 洞察报告

框架会自动生成 AI 测试洞察报告：

- JSON 报告: `reports/ai-insights/ai-insights-report.json`
- HTML 报告: `reports/ai-insights/ai-insights-report.html`

## 📝 运行命令参考

```bash
# 运行所有传统测试
pytest tests/traditional/ -v --alluredir=reports/allure-results

# 运行 AI 驱动测试
pytest tests/ai_driven/ -v -m ai --llm=openai

# 运行混合测试
pytest tests/hybrid/ -v -m hybrid

# 并发执行
pytest tests/traditional/ -n auto --dist=loadgroup

# 指定标记运行
pytest -v -m "smoke and not slow"

# 失败时自动重试
pytest --reruns 2 --reruns-delay 1
```

## 📖 设计文档

- [框架设计文档 (MD)](docs/framework-design.md)
- [最佳实践文档 (MD)](docs/framework_design_best_practice.md)
- [框架概览 (HTML)](docs/framework-overview.html) - 浏览器打开查看
- [最佳实践 (HTML)](docs/framework-best-practice.html) - 浏览器打开查看

## 🔨 技术栈

- **测试框架**：pytest + Playwright
- **AI 能力**：browser-use + LangChain
- **LLM 支持**：OpenAI GPT-4o / Claude 3.5 Sonnet / Ollama 本地模型
- **报告**：Allure Report + AI 洞察报告
- **配置**：YAML + python-dotenv

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**文档维护者**: QA Team  
**最后更新**: 2026-04-21
