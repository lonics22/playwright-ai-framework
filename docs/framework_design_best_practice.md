# Python + Playwright + Allure + browser-use 自动化测试框架设计
## 最佳实践融合版

**更新时间**: 2026-04-20  
**版本**: v1.0 - 战略设计 + 技术实现完整版  
**适用场景**: 生产级自动化测试体系（兼顾稳定性与AI增强）

---

## 📋 目录

1. [背景与目标](#1-背景与目标)
2. [技术栈定位](#2-技术栈定位)
3. [核心设计原则](#3-核心设计原则)
4. [整体架构设计](#4-整体架构设计)
5. [目录结构详解](#5-目录结构详解)
6. [分层设计实现](#6-分层设计实现)
7. [AI增强策略](#7-ai增强策略)
8. [核心模块实现](#8-核心模块实现)
9. [Allure报告集成](#9-allure报告集成)
10. [配置与环境管理](#10-配置与环境管理)
11. [安全与合规](#11-安全与合规)
12. [CI/CD集成](#12-cicd集成)
13. [分阶段实施路线](#13-分阶段实施路线)
14. [风险与应对](#14-风险与应对)

---

## 1. 背景与目标

### 1.1 核心目标

建设一个"**可回归、可扩展、可观测、可AI增强**"的自动化测试体系：

1. ✅ 以 `pytest + Playwright` 作为稳定回归主干，保障可重复性与执行速度
2. ✅ 以 `Allure` 作为统一报告出口，沉淀完整证据链
3. ✅ 通过 `browser-use` 增强AI属性，支持探索式测试、弱自愈、智能辅助
4. ✅ 支持本地与CI一致执行，支持分层分级（smoke/regression/ai-explore）
5. ✅ 双模式支持：传统脚本测试 + AI自然语言测试

### 1.2 价值主张

| 能力维度 | 传统框架 | 本框架 |
|---------|---------|--------|
| **稳定性** | 依赖精确定位器 | 传统定位 + AI自愈备选 |
| **可维护性** | 页面变更需手动修复 | AI辅助定位器更新建议 |
| **覆盖度** | 仅覆盖已知场景 | AI探索未知路径 |
| **调试效率** | 截图 + 日志 | 截图 + Trace + AI步骤历史 |
| **开发速度** | 需编写全部脚本 | 可用自然语言描述任务 |

---

## 2. 技术栈定位

```
┌─────────────────────────────────────────────────────┐
│                 测试执行层                           │
│  pytest (组织) + Playwright (引擎) + Allure (报告)   │
└─────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────┐
│                 AI增强层 (可选)                      │
│        browser-use + LangChain + 多LLM支持           │
└─────────────────────────────────────────────────────┘
```

### 核心依赖

- **Python**: 3.11+ (推荐3.12，性能更优)
- **pytest**: 测试组织、fixture管理、并行执行、标记筛选
- **Playwright (Python)**: 核心UI自动化引擎（稳定、快速、上下文隔离）
- **Allure + allure-pytest**: 统一测试报告与附件管理
- **browser-use**: AI Agent能力层（任务驱动、工具调用、浏览器自动操作）
- **LangChain**: AI编排框架（支持多LLM切换）

---

## 3. 核心设计原则

### 原则1: 稳定优先
```
确定性回归测试 与 AI探索测试 严格分层，不相互污染
- 回归测试：传统Playwright，可重复、可预测
- 探索测试：AI Agent驱动，发现未知问题
- 混合测试：关键路径传统，易变路径AI
```

### 原则2: 证据优先
```
每次失败必须有足够上下文：
✓ 失败截图 (PNG)
✓ 页面DOM快照 (HTML)
✓ Playwright Trace (zip)
✓ 视频录制 (失败必留)
✓ AI步骤历史 (browser-use action log)
✓ 网络请求摘要 (HAR)
```

### 原则3: 可控AI
```
AI能力默认"辅助模式"，逐步开放"执行模式"

三种运行模式：
├─ assist (默认)：AI只给建议，不直接改写回归逻辑
├─ semi-auto：AI可执行受控动作（白名单域名、白名单动作）
└─ agent：纯Agent场景，用于探索与问题复现
```

### 原则4: 安全合规
```
✓ 密钥与敏感数据分离 (secret_provider)
✓ PII数据脱敏过滤 (pii_filter)
✓ 域名白名单限制 (allowed_domains)
✓ 可关闭遥测 (ANONYMIZED_TELEMETRY=false)
✓ 最小权限API密钥
```

### 原则5: 可演进
```
先实现骨架和最小闭环，再迭代智能化能力
Phase 1 → 稳定回归 → Phase 2 → AI增强 → Phase 3 → 体系化
```

---

## 4. 整体架构设计

```
┌──────────────────────────────────────────────────────────────┐
│                      测试用例层 (tests/)                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐              │
│  │ e2e/smoke  │  │ regression │  │ ai_explore │              │
│  └────────────┘  └────────────┘  └────────────┘              │
└──────────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────────┐
│                   页面与流程层 (pages/ + flows/)              │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐              │
│  │ PageObject │  │   AIPage   │  │ FlowObject │              │
│  └────────────┘  └────────────┘  └────────────┘              │
└──────────────────────────────────────────────────────────────┘
                        ↓
┌──────────────────────────────────────────────────────────────┐
│                     核心能力层 (core/)                        │
│  ┌───────────────┐  ┌───────────────┐  ┌──────────────┐     │
│  │ Playwright    │  │ AI/browser-use│  │  Reporting   │     │
│  │ 引擎管理      │  │ Agent服务     │  │  Allure增强  │     │
│  └───────────────┘  └───────────────┘  └──────────────┘     │
│  ┌───────────────┐  ┌───────────────┐                       │
│  │  Security     │  │  Smart Locator│                       │
│  │  安全管理     │  │  智能定位      │                       │
│  └───────────────┘  └───────────────┘                       │
└──────────────────────────────────────────────────────────────┘
```

---

## 5. 目录结构详解

```
automation-framework/
├─ 📄 pyproject.toml              # 项目依赖与工具配置
├─ 📄 pytest.ini                  # pytest配置
├─ 📄 .env.example                # 环境变量模板
├─ 📄 .gitignore
├─ 📄 README.md
│
├─ 📁 docs/                       # 文档中心
│  ├─ framework_design.md         # 本设计文档
│  ├─ test_strategy.md            # 测试策略
│  ├─ ai_usage_guide.md           # AI使用指南
│  └─ troubleshooting.md          # 故障排查
│
├─ 📁 config/                     # 配置管理
│  ├─ settings.yaml               # 全局配置
│  ├─ env.dev.yaml                # 开发环境
│  ├─ env.test.yaml               # 测试环境
│  ├─ env.prod.yaml               # 生产环境
│  └─ browser_config.yaml         # 浏览器配置
│
├─ 📁 core/                       # 框架核心
│  ├─ playwright/                 # Playwright封装
│  │  ├─ browser_manager.py       # 浏览器生命周期管理
│  │  ├─ context_factory.py       # 上下文工厂
│  │  ├─ page_guard.py            # 页面保护（超时、异常）
│  │  └─ wait_helpers.py          # 等待策略
│  │
│  ├─ ai/                         # AI增强模块
│  │  ├─ browser_use_client.py    # browser-use客户端
│  │  ├─ agent_service.py         # Agent服务层
│  │  ├─ agent_factory.py         # Agent工厂（多LLM）
│  │  ├─ prompt_templates.py      # 提示词模板
│  │  ├─ tool_registry.py         # 自定义工具注册
│  │  └─ fallback_policy.py       # AI失败回退策略
│  │
│  ├─ elements/                   # 智能元素定位
│  │  ├─ smart_locator.py         # 智能定位器
│  │  ├─ self_healing.py          # 自我修复定位
│  │  └─ element_watcher.py       # 元素变更监听
│  │
│  ├─ reporting/                  # 报告增强
│  │  ├─ allure_helper.py         # Allure工具函数
│  │  ├─ artifact_manager.py      # 附件管理器
│  │  ├─ result_enricher.py       # 结果增强器
│  │  └─ ai_report_plugin.py      # AI测试洞察报告
│  │
│  └─ security/                   # 安全与合规
│     ├─ secret_provider.py       # 密钥管理
│     └─ pii_filter.py            # 敏感信息过滤
│
├─ 📁 pages/                      # 页面对象模型
│  ├─ base_page.py                # 基础页面对象
│  ├─ ai_page.py                  # AI增强页面基类
│  ├─ login_page.py
│  ├─ dashboard_page.py
│  └─ components/                 # 可复用组件
│     ├─ header.py
│     └─ modal.py
│
├─ 📁 flows/                      # 业务流程封装
│  ├─ auth_flow.py                # 认证流程
│  ├─ order_flow.py               # 订单流程
│  └─ payment_flow.py             # 支付流程
│
├─ 📁 tests/                      # 测试用例
│  ├─ conftest.py                 # pytest全局配置
│  │
│  ├─ e2e/                        # 端到端测试
│  │  ├─ smoke/                   # 冒烟测试（核心链路）
│  │  │  ├─ test_login_smoke.py
│  │  │  └─ test_checkout_smoke.py
│  │  │
│  │  └─ regression/              # 回归测试（全量覆盖）
│  │     ├─ test_user_management.py
│  │     └─ test_order_lifecycle.py
│  │
│  ├─ ai_driven/                  # AI驱动测试
│  │  ├─ test_natural_language.py # 自然语言任务
│  │  ├─ test_self_healing.py     # 自我修复场景
│  │  └─ test_exploration.py      # 探索式测试
│  │
│  ├─ hybrid/                     # 混合测试
│  │  └─ test_e2e_with_ai.py      # 传统+AI组合
│  │
│  └─ contract/                   # 契约测试（可选）
│
├─ 📁 data/                       # 测试数据
│  ├─ accounts/                   # 测试账号
│  │  ├─ dev_accounts.yaml
│  │  └─ test_accounts.yaml
│  │
│  └─ testdata/                   # 业务测试数据
│     ├─ products.json
│     └─ orders.json
│
├─ 📁 fixtures/                   # pytest fixtures
│  ├─ browser_fixtures.py         # 浏览器相关
│  ├─ data_fixtures.py            # 数据相关
│  ├─ ai_fixtures.py              # AI相关
│  └─ allure_fixtures.py          # 报告相关
│
├─ 📁 hooks/                      # pytest钩子
│  ├─ pytest_hooks.py             # 自定义钩子
│  └─ pytest_plugins.py           # 自定义插件
│
├─ 📁 utils/                      # 工具函数
│  ├─ screenshot_helper.py
│  ├─ data_generator.py
│  └─ api_client.py
│
├─ 📁 scripts/                    # 执行脚本
│  ├─ run_smoke.sh
│  ├─ run_regression.sh
│  ├─ run_ai_explore.sh
│  ├─ gen_allure_env.py
│  └─ ci_entry.sh
│
├─ 📁 tools/                      # 开发工具
│  ├─ lint.sh
│  └─ format.sh
│
└─ 📁 reports/                    # 测试报告
   ├─ allure-results/
   ├─ allure-report/
   └─ ai-insights/
```

---

## 6. 分层设计实现

### 6.1 测试层（tests）

#### 6.1.1 smoke测试（冒烟）
```
目标：核心链路快速验证，5分钟内完成
范围：登录、下单、支付、查看订单
频率：每次PR、每次构建
门禁：失败阻塞合并
```

#### 6.1.2 regression测试（回归）
```
目标：全量业务覆盖
范围：所有功能模块
频率：Nightly、发布前
门禁：失败阻塞发布
```

#### 6.1.3 ai_explore测试（AI探索）
```
目标：发现未知问题、补足脚本盲区
范围：边界场景、随机路径
频率：Nightly（低优先级）
门禁：失败告警，不阻塞（初期）
```

### 6.2 页面与流程层

#### 6.2.1 传统PageObject
```python
# pages/login_page.py
from playwright.sync_api import Page

class LoginPage:
    """传统页面对象 - 确定性操作"""
    
    def __init__(self, page: Page):
        self.page = page
        self.email_input = page.locator("#email")
        self.password_input = page.locator("#password")
        self.submit_btn = page.locator("button[type='submit']")
    
    def login(self, email: str, password: str):
        """稳定的登录流程"""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_btn.click()
        self.page.wait_for_url("**/dashboard")
```

#### 6.2.2 AI增强PageObject
```python
# pages/ai_page.py
from playwright.sync_api import Page
from core.ai.browser_use_client import BrowserUseClient
from typing import Optional

class AIPage:
    """AI增强的基础页面对象 - 双模式支持"""
    
    def __init__(self, page: Page, ai_client: Optional[BrowserUseClient] = None):
        self.page = page
        self.ai = ai_client
        self._smart_mode = ai_client is not None
    
    # ========== 传统模式方法 ==========
    def click(self, selector: str):
        """传统点击操作"""
        self.page.click(selector)
    
    def fill(self, selector: str, value: str):
        """传统输入操作"""
        self.page.fill(selector, value)
    
    # ========== AI模式方法 ==========
    async def ai_click(self, element_description: str):
        """
        AI驱动的点击 - 通过自然语言描述定位元素
        
        Args:
            element_description: 元素的自然语言描述
            例如: "红色的提交按钮", "显示'下一步'的链接"
        """
        if not self._smart_mode:
            raise RuntimeError("AI client not initialized")
        
        task = f"在页面上找到 '{element_description}' 并点击它"
        return await self.ai.execute_task(task)
    
    async def ai_fill_form(self, form_data: dict):
        """
        AI驱动的表单填写
        
        Args:
            form_data: 表单字段与值的字典
            例如: {"用户名": "test", "邮箱": "test@example.com"}
        """
        fields = ", ".join([f"{k}={v}" for k, v in form_data.items()])
        task = f"填写表单，字段值: {fields}"
        return await self.ai.execute_task(task)
    
    async def ai_verify(self, expectation: str) -> bool:
        """
        AI驱动的验证 - 自然语言断言
        
        Args:
            expectation: 预期状态的自然语言描述
            例如: "页面显示成功提示", "购物车有3个商品"
        """
        task = f"验证页面是否符合预期: {expectation}"
        result = await self.ai.execute_task(task)
        return result.get("success", False)
```

#### 6.2.3 业务流程封装
```python
# flows/auth_flow.py
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

class AuthFlow:
    """认证流程封装 - 减少测试脚本重复"""
    
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)
        self.dashboard_page = DashboardPage(page)
    
    def standard_login(self, email: str, password: str):
        """标准登录流程"""
        self.page.goto("/login")
        self.login_page.login(email, password)
        self.dashboard_page.wait_for_loaded()
        return self.dashboard_page
    
    def admin_login(self):
        """管理员登录（使用预设账号）"""
        from data.accounts import ADMIN_ACCOUNT
        return self.standard_login(
            ADMIN_ACCOUNT["email"],
            ADMIN_ACCOUNT["password"]
        )
```

---

## 7. AI增强策略

### 7.1 AI定位：增强层而非替代层

```
┌─────────────────────────────────────────────┐
│          稳定回归主干（Playwright）          │
│  ├─ 确定性场景（登录、支付、核心业务）       │
│  ├─ 高频执行（smoke、regression）            │
│  └─ 门禁阻塞（失败必须修复）                │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│            AI增强层（browser-use）           │
│  ├─ 探索式测试（发现未知问题）              │
│  ├─ 弱自愈辅助（定位失败时给建议）          │
│  ├─ 复杂易变场景（频繁改版的功能）          │
│  └─ 智能工具（OTP读取、邮件校验）           │
└─────────────────────────────────────────────┘
```

### 7.2 三种运行模式

#### 模式1: assist（推荐默认）
```python
AI_MODE=assist

特点：
- AI只给建议，不直接执行
- 定位失败时返回候选定位器
- 报告中附加AI分析结果
- 安全性最高，适合生产环境
```

#### 模式2: semi-auto（受控执行）
```python
AI_MODE=semi-auto
AI_ALLOWED_DOMAINS=example.com,api.example.com
AI_ALLOWED_ACTIONS=click,fill,select

特点：
- AI可执行白名单内的动作
- 域名限制避免误操作
- 适合混合测试场景
```

#### 模式3: agent（纯探索）
```python
AI_MODE=agent
AI_MAX_STEPS=30

特点：
- AI完全自主探索
- 用于问题复现、边界探索
- 仅用于ai_explore测试集
- 需要严格监控
```

### 7.3 AI控制点设计

```python
# core/ai/agent_service.py
from browser_use import Agent, Browser
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

class AgentService:
    """AI Agent服务层 - 统一管理AI调用"""
    
    def __init__(self, config: dict):
        self.mode = config.get("ai_mode", "assist")
        self.max_steps = config.get("ai_max_steps", 30)
        self.allowed_domains = config.get("ai_allowed_domains", [])
        self.llm = self._create_llm(config.get("llm_provider", "openai"))
        self.browser = None
    
    async def execute_task(
        self,
        task: str,
        context: dict = None,
        use_vision: bool = True
    ):
        """
        执行AI任务（带控制点）
        
        Args:
            task: 自然语言任务描述
            context: 额外上下文信息
            use_vision: 是否启用视觉能力（敏感场景可关闭）
        """
        # 控制点1: 检查模式
        if self.mode == "assist":
            return await self._assist_mode(task, context)
        
        # 控制点2: 域名限制
        if self.allowed_domains:
            self._validate_allowed_domains()
        
        # 控制点3: 步骤限制
        agent = Agent(
            task=task,
            llm=self.llm,
            browser=self.browser,
            use_vision=use_vision,
            max_steps=self.max_steps,  # 关键控制点
        )
        
        try:
            result = await agent.run()
            return self._format_result(result)
        except Exception as e:
            return self._handle_failure(e, task)
    
    def _create_llm(self, provider: str):
        """支持多LLM后端"""
        llm_map = {
            "openai": ChatOpenAI(model="gpt-4o", temperature=0.1),
            "anthropic": ChatAnthropic(model="claude-3-5-sonnet-20241022"),
            "local": ChatOllama(model="llama3.2"),
        }
        return llm_map.get(provider)
    
    async def _assist_mode(self, task: str, context: dict):
        """辅助模式：AI只给建议，不执行"""
        # AI分析任务并返回建议步骤
        suggestions = await self._analyze_task(task)
        return {
            "mode": "assist",
            "suggestions": suggestions,
            "auto_execute": False
        }
```

---

## 8. 核心模块实现

### 8.1 智能定位器（SmartLocator）

```python
# core/elements/smart_locator.py
from typing import List, Optional
from playwright.sync_api import Page, Locator
import hashlib
import json

class SmartLocator:
    """
    智能元素定位器
    
    策略：
    1. 优先使用传统选择器（快速、稳定）
    2. 失败时尝试备用选择器列表
    3. 启用AI时，使用AI视觉定位
    4. 记录成功定位历史，优化后续查找
    """
    
    def __init__(self, page: Page, ai_service=None):
        self.page = page
        self.ai = ai_service
        self.element_registry = {}  # 元素历史定位缓存
        self.success_history = {}   # 成功定位历史
    
    def find(
        self,
        selector: str,
        fallback_selectors: List[str] = None,
        ai_description: str = None
    ) -> Locator:
        """
        智能查找元素
        
        Args:
            selector: 主选择器
            fallback_selectors: 备用选择器列表
            ai_description: AI定位用的自然语言描述
        
        Returns:
            Playwright Locator对象
        
        Raises:
            ElementNotFoundException: 所有策略失败时抛出
        """
        # 策略1: 尝试主选择器
        try:
            locator = self.page.locator(selector)
            if locator.count() > 0:
                self._update_success_history(selector)
                return locator.first
        except Exception as e:
            pass
        
        # 策略2: 尝试备用选择器
        if fallback_selectors:
            for fb_selector in fallback_selectors:
                try:
                    locator = self.page.locator(fb_selector)
                    if locator.count() > 0:
                        self._update_success_history(fb_selector)
                        return locator.first
                except:
                    continue
        
        # 策略3: AI视觉定位（如果启用）
        if ai_description and self.ai:
            return self._ai_find(ai_description)
        
        raise ElementNotFoundException(
            f"无法定位元素: {selector}, "
            f"备用策略: {fallback_selectors}, "
            f"AI描述: {ai_description}"
        )
    
    async def _ai_find(self, description: str) -> Locator:
        """
        使用AI通过视觉描述定位元素
        
        流程:
        1. 截图当前页面
        2. AI分析图像，返回元素坐标或新选择器
        3. 构造Playwright Locator
        """
        screenshot = self.page.screenshot()
        
        result = await self.ai.execute_task(
            f"在页面上定位元素: {description}",
            context={"screenshot": screenshot}
        )
        
        # 根据AI返回的坐标或选择器构造Locator
        if "selector" in result:
            return self.page.locator(result["selector"])
        elif "coordinates" in result:
            x, y = result["coordinates"]
            # 使用坐标点击（Playwright不直接支持坐标定位，需转换）
            return self.page.locator(f"xpath=//*[position()=('{x}','{y}')]")
    
    def register_element(
        self,
        name: str,
        selectors: List[str],
        description: str = None
    ):
        """
        注册元素多维度特征，用于自我修复
        
        Args:
            name: 元素名称（唯一标识）
            selectors: 多个候选选择器
            description: AI定位用的描述
        """
        self.element_registry[name] = {
            "selectors": selectors,
            "description": description,
            "checksum": None,  # 元素内容哈希（未来用于检测变化）
            "last_success": None,  # 最后成功的选择器
        }
    
    def _update_success_history(self, selector: str):
        """更新成功定位历史（用于优化查找顺序）"""
        if selector not in self.success_history:
            self.success_history[selector] = 0
        self.success_history[selector] += 1
```

### 8.2 自我修复定位

```python
# core/elements/self_healing.py
from playwright.sync_api import Page, Locator
from core.ai.agent_service import AgentService

class SelfHealingLocator:
    """
    自我修复定位器
    
    当元素定位失败时，AI自动寻找替代方案
    并记录修复建议供人工确认
    """
    
    def __init__(self, page: Page, ai_service: AgentService):
        self.page = page
        self.ai = ai_service
        self.healing_log = []  # 修复历史日志
    
    async def find_with_healing(
        self,
        failed_selector: str,
        element_purpose: str
    ) -> Locator:
        """
        自我修复查找
        
        Args:
            failed_selector: 失败的原始选择器
            element_purpose: 元素用途描述（用于AI理解上下文）
        
        Returns:
            新的Locator对象
        """
        # 步骤1: 截图当前页面
        screenshot = self.page.screenshot()
        
        # 步骤2: AI分析寻找相似元素
        healing_result = await self.ai.execute_task(
            task=f"""
            原始选择器 '{failed_selector}' 已失效。
            元素用途: {element_purpose}
            
            请分析页面并找到最可能的替代元素，返回:
            1. 新的CSS选择器
            2. 置信度评分 (0-1)
            3. 修复理由
            """,
            context={"screenshot": screenshot}
        )
        
        # 步骤3: 记录修复日志
        self.healing_log.append({
            "original_selector": failed_selector,
            "new_selector": healing_result.get("selector"),
            "confidence": healing_result.get("confidence"),
            "reason": healing_result.get("reason"),
            "timestamp": datetime.now().isoformat()
        })
        
        # 步骤4: 返回新定位器
        new_selector = healing_result.get("selector")
        if new_selector:
            return self.page.locator(new_selector)
        else:
            raise ElementNotFoundException(
                f"AI无法找到 '{failed_selector}' 的替代方案"
            )
    
    def export_healing_report(self) -> dict:
        """导出修复报告供人工审查"""
        return {
            "total_healings": len(self.healing_log),
            "healings": self.healing_log,
            "suggestions": self._generate_suggestions()
        }
    
    def _generate_suggestions(self) -> List[str]:
        """基于修复历史生成改进建议"""
        suggestions = []
        
        # 分析高频失效的选择器
        failed_counts = {}
        for log in self.healing_log:
            selector = log["original_selector"]
            failed_counts[selector] = failed_counts.get(selector, 0) + 1
        
        for selector, count in failed_counts.items():
            if count >= 3:
                suggestions.append(
                    f"选择器 '{selector}' 失效{count}次，建议更新为更稳定的定位策略"
                )
        
        return suggestions
```

### 8.3 browser-use集成

```python
# core/ai/browser_use_client.py
from browser_use import Agent, Browser, BrowserConfig
from langchain_openai import ChatOpenAI
from core.security.secret_provider import get_secret
import asyncio

class BrowserUseClient:
    """
    browser-use 客户端封装
    
    负责:
    1. AI Agent初始化与配置
    2. 任务执行与结果处理
    3. 安全控制（域名限制、步骤限制）
    4. 错误处理与重试
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.llm = self._init_llm()
        self.browser = None
        self.agent = None
    
    def _init_llm(self):
        """初始化LLM（从环境变量读取API Key）"""
        provider = self.config.get("llm_provider", "openai")
        
        if provider == "openai":
            return ChatOpenAI(
                model=self.config.get("openai_model", "gpt-4o"),
                temperature=0.1,
                api_key=get_secret("OPENAI_API_KEY")
            )
        elif provider == "anthropic":
            return ChatAnthropic(
                model=self.config.get("anthropic_model", "claude-3-5-sonnet-20241022"),
                api_key=get_secret("ANTHROPIC_API_KEY")
            )
        elif provider == "local":
            return ChatOllama(
                model=self.config.get("local_model", "llama3.2"),
                base_url=self.config.get("ollama_base_url", "http://localhost:11434")
            )
    
    async def execute_task(
        self,
        task: str,
        max_steps: int = None,
        use_vision: bool = True,
        allowed_domains: List[str] = None
    ):
        """
        执行AI任务
        
        Args:
            task: 自然语言任务描述
            max_steps: 最大步骤数（默认从config读取）
            use_vision: 是否启用视觉能力
            allowed_domains: 允许访问的域名列表
        """
        max_steps = max_steps or self.config.get("ai_max_steps", 30)
        allowed_domains = allowed_domains or self.config.get("ai_allowed_domains", [])
        
        # 初始化Browser（如果尚未初始化）
        if not self.browser:
            browser_config = BrowserConfig(
                headless=self.config.get("headless", False),
                disable_security=False,  # 保持安全限制
            )
            self.browser = Browser(config=browser_config)
        
        # 创建Agent
        agent = Agent(
            task=task,
            llm=self.llm,
            browser=self.browser,
            use_vision=use_vision,
            max_steps=max_steps,
        )
        
        # 执行任务
        try:
            result = await agent.run()
            return self._format_result(result)
        except Exception as e:
            return self._handle_error(e, task)
    
    def _format_result(self, result) -> dict:
        """格式化AI执行结果"""
        return {
            "success": result.is_done(),
            "final_result": result.final_result(),
            "history": result.history(),
            "steps_taken": len(result.history()),
            "errors": result.errors() if hasattr(result, 'errors') else []
        }
    
    def _handle_error(self, error: Exception, task: str) -> dict:
        """处理AI执行错误"""
        return {
            "success": False,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "task": task,
            "suggestion": self._get_error_suggestion(error)
        }
    
    def _get_error_suggestion(self, error: Exception) -> str:
        """根据错误类型给出建议"""
        error_suggestions = {
            "TimeoutError": "尝试增加max_steps或简化任务描述",
            "ElementNotFoundError": "检查页面是否已加载，或使用更详细的元素描述",
            "NetworkError": "检查allowed_domains配置或网络连接",
        }
        return error_suggestions.get(type(error).__name__, "请检查日志获取更多信息")
    
    async def close(self):
        """关闭浏览器"""
        if self.browser:
            await self.browser.close()
```

---

## 9. Allure报告集成

### 9.1 报告增强策略

每个失败用例必须包含以下附件：

```
✓ 失败截图 (PNG)
✓ 页面源码快照 (HTML)
✓ Playwright Trace (zip) - 可回放完整操作
✓ 视频录制 (MP4) - 失败必留，成功可选
✓ AI步骤历史 (JSON) - browser-use action log
✓ 网络请求摘要 (HAR)
✓ 控制台日志 (TXT)
```

### 9.2 Allure Helper实现

```python
# core/reporting/allure_helper.py
import allure
from allure_commons.types import AttachmentType
import json
from pathlib import Path

class AllureHelper:
    """Allure报告增强工具"""
    
    @staticmethod
    def attach_screenshot(page, name: str = "截图"):
        """附加截图"""
        screenshot = page.screenshot()
        allure.attach(
            screenshot,
            name=name,
            attachment_type=AttachmentType.PNG
        )
    
    @staticmethod
    def attach_page_source(page, name: str = "页面源码"):
        """附加页面HTML"""
        html = page.content()
        allure.attach(
            html,
            name=name,
            attachment_type=AttachmentType.HTML
        )
    
    @staticmethod
    def attach_trace(trace_path: Path):
        """附加Playwright Trace"""
        with open(trace_path, "rb") as f:
            allure.attach(
                f.read(),
                name="Playwright Trace",
                attachment_type=AttachmentType.ZIP,
                extension="zip"
            )
    
    @staticmethod
    def attach_video(video_path: Path):
        """附加视频录制"""
        with open(video_path, "rb") as f:
            allure.attach(
                f.read(),
                name="执行视频",
                attachment_type=AttachmentType.MP4,
                extension="mp4"
            )
    
    @staticmethod
    def attach_ai_execution(task: str, result: dict):
        """附加AI执行详情"""
        ai_report = {
            "task": task,
            "success": result.get("success"),
            "steps_taken": result.get("steps_taken"),
            "history": result.get("history", []),
            "errors": result.get("errors", []),
        }
        
        allure.attach(
            json.dumps(ai_report, indent=2, ensure_ascii=False),
            name="AI执行详情",
            attachment_type=AttachmentType.JSON
        )
    
    @staticmethod
    def attach_network_log(page):
        """附加网络请求日志（HAR）"""
        # Playwright可以导出HAR文件
        # 这里简化为附加关键请求信息
        pass
    
    @staticmethod
    def attach_console_log(page):
        """附加控制台日志"""
        console_messages = []
        
        def handle_console(msg):
            console_messages.append({
                "type": msg.type,
                "text": msg.text,
                "location": msg.location
            })
        
        page.on("console", handle_console)
        
        # 测试结束后附加
        if console_messages:
            allure.attach(
                json.dumps(console_messages, indent=2),
                name="控制台日志",
                attachment_type=AttachmentType.JSON
            )
```

### 9.3 标签体系设计

```python
# 在测试用例中使用
import allure

@allure.epic("电商平台")
@allure.feature("订单管理")
@allure.story("下单流程")
@allure.severity(allure.severity_level.BLOCKER)
@allure.tag("smoke", "P0")
@allure.owner("QA Team")
@allure.link("https://jira.example.com/PROJ-123", name="JIRA")
def test_checkout_flow():
    pass
```

---

## 10. 配置与环境管理

### 10.1 环境变量设计

```bash
# .env.example

# ========== Playwright / Runtime ==========
BASE_URL=https://example.test
HEADLESS=false
BROWSER=chromium
SLOW_MO=50
TIMEOUT_MS=15000
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080

# ========== Allure ==========
ALLURE_RESULTS_DIR=reports/allure-results
ALLURE_REPORT_DIR=reports/allure-report

# ========== Browser-Use AI ==========
# LLM Provider: openai / anthropic / local
LLM_PROVIDER=openai

# OpenAI
OPENAI_API_KEY=sk-xxx
OPENAI_MODEL=gpt-4o

# Anthropic
ANTHROPIC_API_KEY=sk-ant-xxx
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022

# Local Ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# AI 控制
AI_MODE=assist                      # assist / semi-auto / agent
AI_MAX_STEPS=30
AI_ALLOWED_DOMAINS=example.test,api.example.test
AI_USE_VISION=true
ANONYMIZED_TELEMETRY=false

# ========== 安全 ==========
ENABLE_PII_FILTER=true
SECRET_PROVIDER=env                 # env / vault / aws-secrets

# ========== 测试数据 ==========
TEST_ACCOUNT_EMAIL=test@example.com
TEST_ACCOUNT_PASSWORD=xxx
```

### 10.2 多环境配置

```yaml
# config/env.dev.yaml
environment: development
base_url: https://dev.example.com
api_base: https://api.dev.example.com
timeout: 30000

database:
  host: dev-db.example.com
  port: 5432

features:
  ai_enabled: true
  video_recording: on-failure
```

```yaml
# config/env.prod.yaml
environment: production
base_url: https://example.com
api_base: https://api.example.com
timeout: 10000

database:
  host: prod-db.example.com
  port: 5432

features:
  ai_enabled: false           # 生产环境默认关闭AI探索
  video_recording: always
```

### 10.3 配置加载器

```python
# config/settings.py
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

class Settings:
    """全局配置管理器"""
    
    def __init__(self):
        # 加载.env文件
        load_dotenv()
        
        # 加载环境配置
        env = os.getenv("TEST_ENV", "dev")
        config_file = Path(__file__).parent / f"env.{env}.yaml"
        
        with open(config_file) as f:
            self.config = yaml.safe_load(f)
        
        # 合并环境变量（优先级更高）
        self._merge_env_vars()
    
    def _merge_env_vars(self):
        """环境变量覆盖配置文件"""
        if os.getenv("BASE_URL"):
            self.config["base_url"] = os.getenv("BASE_URL")
        
        if os.getenv("AI_MODE"):
            self.config.setdefault("ai", {})["mode"] = os.getenv("AI_MODE")
    
    def get(self, key: str, default=None):
        """获取配置值（支持点号路径）"""
        keys = key.split(".")
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default

# 全局实例
settings = Settings()
```

---

## 11. 安全与合规

### 11.1 密钥管理

```python
# core/security/secret_provider.py
import os
from abc import ABC, abstractmethod

class SecretProvider(ABC):
    """密钥提供者抽象基类"""
    
    @abstractmethod
    def get_secret(self, key: str) -> str:
        pass

class EnvSecretProvider(SecretProvider):
    """从环境变量读取密钥"""
    
    def get_secret(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Secret {key} not found in environment")
        return value

class VaultSecretProvider(SecretProvider):
    """从HashiCorp Vault读取密钥"""
    
    def __init__(self, vault_url: str, token: str):
        self.vault_url = vault_url
        self.token = token
    
    def get_secret(self, key: str) -> str:
        # 实现Vault API调用
        pass

# 工厂函数
def get_secret_provider() -> SecretProvider:
    """根据配置返回密钥提供者"""
    provider_type = os.getenv("SECRET_PROVIDER", "env")
    
    if provider_type == "env":
        return EnvSecretProvider()
    elif provider_type == "vault":
        return VaultSecretProvider(
            vault_url=os.getenv("VAULT_URL"),
            token=os.getenv("VAULT_TOKEN")
        )
    else:
        raise ValueError(f"Unknown secret provider: {provider_type}")

# 便捷函数
def get_secret(key: str) -> str:
    """获取密钥的便捷函数"""
    return get_secret_provider().get_secret(key)
```

### 11.2 PII过滤

```python
# core/security/pii_filter.py
import re
from typing import Dict, Any

class PIIFilter:
    """敏感信息过滤器"""
    
    # 正则模式
    PATTERNS = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        "credit_card": r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
    }
    
    @classmethod
    def filter_dict(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """递归过滤字典中的PII"""
        filtered = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                filtered[key] = cls.filter_string(value)
            elif isinstance(value, dict):
                filtered[key] = cls.filter_dict(value)
            elif isinstance(value, list):
                filtered[key] = [
                    cls.filter_string(item) if isinstance(item, str) else item
                    for item in value
                ]
            else:
                filtered[key] = value
        
        return filtered
    
    @classmethod
    def filter_string(cls, text: str) -> str:
        """过滤字符串中的PII"""
        filtered = text
        
        for pii_type, pattern in cls.PATTERNS.items():
            filtered = re.sub(pattern, f"[{pii_type.upper()}_REDACTED]", filtered)
        
        return filtered
```

---

## 12. CI/CD集成

### 12.1 分层门禁策略

```
┌───────────────────────────────────────────────────────┐
│                   PR阶段（快速反馈）                   │
│  ├─ smoke测试 (5分钟内)                               │
│  ├─ lint检查                                          │
│  └─ 失败策略：阻塞合并                                │
└───────────────────────────────────────────────────────┘
                        ↓
┌───────────────────────────────────────────────────────┐
│                 Nightly阶段（深度验证）                │
│  ├─ regression测试 (30-60分钟)                        │
│  ├─ ai_explore测试 (可选，不阻塞)                     │
│  └─ 失败策略：告警通知，生成报告                      │
└───────────────────────────────────────────────────────┘
                        ↓
┌───────────────────────────────────────────────────────┐
│                 Release阶段（质量保障）                │
│  ├─ 全量regression测试                               │
│  ├─ 跨浏览器测试（Chromium/Firefox/WebKit）           │
│  └─ 失败策略：阻塞发布                                │
└───────────────────────────────────────────────────────┘
```

### 12.2 GitHub Actions示例

```yaml
# .github/workflows/pr-tests.yml
name: PR Tests

on:
  pull_request:
    branches: [main, develop]

jobs:
  smoke-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
      
      - name: Run smoke tests
        env:
          BASE_URL: ${{ secrets.TEST_BASE_URL }}
          HEADLESS: true
        run: |
          pytest tests/e2e/smoke/ \
            -v \
            -m smoke \
            --alluredir=reports/allure-results
      
      - name: Upload Allure results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-results
          path: reports/allure-results
      
      - name: Generate Allure report
        if: always()
        run: |
          allure generate reports/allure-results \
            -o reports/allure-report \
            --clean
      
      - name: Upload Allure report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: allure-report
          path: reports/allure-report
```

```yaml
# .github/workflows/nightly-tests.yml
name: Nightly Regression

on:
  schedule:
    - cron: '0 2 * * *'  # 每天凌晨2点（UTC）
  workflow_dispatch:      # 手动触发

jobs:
  regression-tests:
    runs-on: ubuntu-latest
    timeout-minutes: 60
    
    strategy:
      matrix:
        browser: [chromium, firefox, webkit]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install ${{ matrix.browser }}
      
      - name: Run regression tests
        env:
          BASE_URL: ${{ secrets.TEST_BASE_URL }}
          BROWSER: ${{ matrix.browser }}
          HEADLESS: true
        run: |
          pytest tests/e2e/regression/ \
            -v \
            -m regression \
            -n auto \
            --dist=loadgroup \
            --alluredir=reports/allure-results
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-${{ matrix.browser }}
          path: reports/
  
  ai-exploration:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    if: github.event_name == 'schedule'  # 仅在定时任务时运行
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          playwright install chromium
      
      - name: Run AI exploration
        env:
          BASE_URL: ${{ secrets.TEST_BASE_URL }}
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          AI_MODE: agent
          HEADLESS: true
        run: |
          pytest tests/ai_driven/ \
            -v \
            -m ai \
            --alluredir=reports/allure-results
        continue-on-error: true  # AI测试失败不阻塞
      
      - name: Upload AI insights
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: ai-insights
          path: reports/ai-insights/
```

### 12.3 执行脚本

```bash
# scripts/run_smoke.sh
#!/bin/bash
set -e

echo "🚀 运行冒烟测试..."

pytest tests/e2e/smoke/ \
  -v \
  -m smoke \
  --tb=short \
  --alluredir=reports/allure-results

echo "✅ 冒烟测试完成"

# 生成报告
allure generate reports/allure-results \
  -o reports/allure-report \
  --clean

echo "📊 Allure报告已生成: reports/allure-report/index.html"
```

```bash
# scripts/run_ai_explore.sh
#!/bin/bash
set -e

echo "🤖 运行AI探索测试..."

# 检查API Key
if [ -z "$OPENAI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "❌ 错误: 未设置LLM API Key"
  exit 1
fi

pytest tests/ai_driven/ \
  -v \
  -m ai \
  --ai-mode=agent \
  --alluredir=reports/allure-results

echo "✅ AI探索测试完成（失败不阻塞）"

# 导出AI洞察报告
python scripts/gen_ai_insights.py
```

---

## 13. 分阶段实施路线

### Phase 1: 基础框架（2-3周）

**目标**: 跑通Playwright + pytest + Allure最小闭环

- [x] 项目结构搭建
- [x] pytest配置与fixture设计
- [x] Playwright基础封装（browser_manager, context_factory）
- [x] PageObject基类实现
- [x] Allure报告集成（截图、trace、视频）
- [x] 示例测试用例（登录、下单）
- [x] 本地执行脚本
- [x] CI集成（smoke测试）

**验收标准**:
```
✓ smoke测试可在本地和CI稳定执行
✓ 失败用例有完整证据链（截图+trace+视频）
✓ Allure报告可正常生成和查看
```

### Phase 2: AI增强（3-4周）

**目标**: 接入browser-use，建立AI辅助能力

- [ ] browser-use客户端封装
- [ ] AgentService实现（模式控制、域名限制）
- [ ] AIPage双模式页面对象
- [ ] SmartLocator智能定位器
- [ ] AI探索测试目录与示例
- [ ] AI执行结果附加到Allure
- [ ] assist模式试点（在1-2个场景）

**验收标准**:
```
✓ AI assist模式可给出定位失败的修复建议
✓ AI探索测试可发现至少1个未覆盖场景
✓ AI执行历史完整记录到Allure
```

### Phase 3: 体系化（4-6周）

**目标**: 建立完整测试体系与质量度量

- [ ] SelfHealingLocator自我修复
- [ ] 自定义AI工具（OTP读取、邮件验证）
- [ ] flaky测试检测与重跑策略
- [ ] 测试稳定性看板
- [ ] 风险评分与优先级策略
- [ ] 多LLM支持（OpenAI + Anthropic + Local）
- [ ] 完整的CI分层门禁
- [ ] 测试质量度量（覆盖率、稳定性）

**验收标准**:
```
✓ 回归测试稳定性 > 95%
✓ AI探索可自动生成候选回归用例
✓ 完整的质量看板（覆盖率、flaky率、执行时长）
```

---

## 14. 风险与应对

### 风险1: AI不确定性高

**表现**: AI执行结果不稳定，同一任务多次执行结果不同

**应对**:
- ✅ AI结果不直接作为强门禁（初期仅告警）
- ✅ 设置max_steps限制，避免无限探索
- ✅ 关键路径仍用传统脚本保障
- ✅ 建立AI执行成功率监控

### 风险2: 运行成本上升

**表现**: AI调用LLM API产生费用，并发执行成本高

**应对**:
- ✅ 控制AI场景数量（初期 < 10%测试用例）
- ✅ 限制并发数（AI测试串行执行）
- ✅ 优先使用本地Ollama（成本为0）
- ✅ 设置月度预算告警

### 风险3: 调试困难

**表现**: AI失败时难以复现，缺少足够上下文

**应对**:
- ✅ 统一收集trace/video/AI history
- ✅ 每个AI步骤附加截图
- ✅ 记录完整的提示词与响应
- ✅ 失败自动生成复现脚本

### 风险4: 数据安全风险

**表现**: AI可能误操作敏感数据，或泄露到LLM日志

**应对**:
- ✅ 敏感数据脱敏（PII Filter）
- ✅ 域名白名单限制
- ✅ 最小权限API密钥
- ✅ 关闭LLM遥测（ANONYMIZED_TELEMETRY=false）
- ✅ 使用本地Ollama处理敏感场景

### 风险5: 团队学习曲线

**表现**: 团队对AI测试理解不足，滥用或误用

**应对**:
- ✅ 提供详细的AI使用指南
- ✅ 代码审查强制检查AI控制点
- ✅ 定期复盘AI使用效果
- ✅ 建立AI使用最佳实践库

---

## 15. pytest.ini配置

```ini
[pytest]
# 测试路径
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# 标记定义
markers =
    smoke: 冒烟测试（核心链路，快速验证）
    regression: 回归测试（全量覆盖）
    ai: AI驱动测试（需要LLM配置）
    hybrid: 混合测试（传统+AI）
    slow: 慢速测试（执行时间>5分钟）
    flaky: 已知不稳定测试
    
    # 按功能模块
    auth: 认证相关测试
    order: 订单相关测试
    payment: 支付相关测试
    
    # 按优先级
    p0: 最高优先级（阻塞发布）
    p1: 高优先级
    p2: 中优先级
    p3: 低优先级

# 默认参数
addopts =
    -v
    --tb=short
    --strict-markers
    --alluredir=reports/allure-results
    --clean-alluredir

# 异步测试配置
asyncio_mode = auto
asyncio_default_fixture_loop_scope = function

# 并发执行配置
# 使用: pytest -n auto --dist=loadgroup
# loadgroup: 相同标记的测试在同一worker执行

# 日志配置
log_cli = true
log_cli_level = INFO
log_cli_format = %(asctime)s [%(levelname)8s] %(message)s
log_cli_date_format = %Y-%m-%d %H:%M:%S

# 超时配置
timeout = 300
timeout_method = thread
```

---

## 16. 依赖管理

```toml
# pyproject.toml
[project]
name = "automation-framework"
version = "1.0.0"
description = "Modern test automation framework with AI enhancement"
requires-python = ">=3.11"

dependencies = [
    # 核心依赖
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-xdist>=3.5.0",
    "pytest-timeout>=2.2.0",
    "playwright>=1.41.0",
    "allure-pytest>=2.13.0",
    
    # 配置管理
    "pyyaml>=6.0.1",
    "python-dotenv>=1.0.0",
    
    # Browser-Use 及 AI 相关
    "browser-use>=0.1.0",
    "langchain>=0.1.0",
    "langchain-openai>=0.0.5",
    "langchain-anthropic>=0.1.0",
    "langchain-community>=0.0.13",
    
    # 数据处理
    "faker>=22.0.0",
    "requests>=2.31.0",
    
    # 工具
    "rich>=13.0.0",  # 美化控制台输出
]

[project.optional-dependencies]
dev = [
    "black>=24.0.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0",
    "pre-commit>=3.6.0",
]

local-ai = [
    "langchain-ollama>=0.0.1",
]

[tool.pytest.ini_options]
# pytest配置也可以写在这里

[tool.black]
line-length = 100
target-version = ['py311']

[tool.ruff]
line-length = 100
select = ["E", "F", "I", "N", "W"]
ignore = ["E501"]

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

---

## 17. 快速开始

### 17.1 环境准备

```bash
# 1. 克隆仓库
git clone https://github.com/your-org/automation-framework.git
cd automation-framework

# 2. 创建虚拟环境（推荐）
python3.12 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. 安装依赖
pip install -e .
playwright install chromium

# 4. 配置环境变量
cp .env.example .env
# 编辑.env，填入必要的配置（BASE_URL等）

# 5. 验证安装
pytest --version
playwright --version
```

### 17.2 运行第一个测试

```bash
# 运行冒烟测试
./scripts/run_smoke.sh

# 查看Allure报告
allure open reports/allure-report
```

### 17.3 启用AI功能

```bash
# 1. 配置LLM API Key（.env文件）
OPENAI_API_KEY=sk-xxx
AI_MODE=assist

# 2. 运行AI测试
pytest tests/ai_driven/test_natural_language.py -v -m ai

# 3. 查看AI执行详情（Allure报告中）
```

---

## 18. 总结

本框架设计融合了传统自动化测试的稳定性与AI增强的灵活性：

### 核心价值

1. **稳定优先**: 传统回归保障质量基线，AI探索发现盲区
2. **证据充分**: 完整的失败证据链，支持快速定位问题
3. **可控AI**: 三种模式渐进式应用，安全可控
4. **易于维护**: PageObject + Flow分层，降低脚本重复
5. **持续演进**: 分阶段实施，从骨架到智能化

### 关键差异化

| 传统框架 | 本框架 |
|---------|--------|
| 单一脚本模式 | 双模式（传统+AI） |
| 定位器失效需手动修复 | AI辅助自我修复建议 |
| 仅覆盖已知场景 | AI探索未知路径 |
| 失败证据单一 | 完整证据链（trace+video+AI历史） |

### 下一步行动

1. ✅ 完成Phase 1基础框架搭建
2. ✅ 在1-2个场景试点AI assist模式
3. ✅ 收集反馈，调整AI控制策略
4. ✅ 逐步扩展AI覆盖范围
5. ✅ 建立质量度量看板

---

**文档维护者**: QA Team  
**最后更新**: 2026-04-20  
**反馈渠道**: qa-team@example.com
