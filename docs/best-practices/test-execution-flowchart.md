# Playwright AI 框架 - 测试执行流程图

本文档详细描述了框架执行测试用例的完整流程，包括正常执行路径和异常处理路径。

---

## 一、整体执行流程概览

```mermaid
flowchart TB
    Start([开始]) --> LoadConfig[加载配置]
    LoadConfig --> |读取| settings.py
    LoadConfig --> |读取| env_config.yaml
    LoadConfig --> |读取| browser_config.yaml
    LoadConfig --> |加载|.env环境变量
    
    LoadConfig --> InitPytest[初始化pytest]
    InitPytest --> DiscoverTests[发现测试用例]
    DiscoverTests --> CheckMarker{检查Marker}
    
    CheckMarker -->|@pytest.mark.ai| AITest[AI驱动测试流程]
    CheckMarker -->|@pytest.mark.hybrid| HybridTest[混合测试流程]
    CheckMarker -->|无特殊Marker| TraditionalTest[传统测试流程]
    
    TraditionalTest --> SetupFixture[执行fixture:setUp]
    AITest --> SetupAIFixture[执行fixture:ai_agent]
    HybridTest --> SetupHybridFixture[执行fixture:smart_page]
    
    SetupFixture --> RunTest[执行测试方法]
    SetupAIFixture --> RunAITest[执行AI测试方法]
    SetupHybridFixture --> RunHybridTest[执行混合测试方法]
    
    RunTest --> CheckResult{检查测试结果}
    RunAITest --> CheckResult
    RunHybridTest --> CheckResult
    
    CheckResult -->|成功| SuccessFlow[成功处理流程]
    CheckResult -->|失败| FailureFlow[失败处理流程]
    CheckResult -->|错误| ErrorFlow[错误处理流程]
    
    SuccessFlow --> CollectEvidence[收集测试证据]
    FailureFlow --> AutoRetry{自动重试?}
    ErrorFlow --> AutoRetry
    
    AutoRetry -->|是| RetryTest[重试测试]
    AutoRetry -->|否| CollectEvidence
    RetryTest --> CheckResult
    
    CollectEvidence --> GenerateReport[生成测试报告]
    GenerateReport --> AllureReport[Allure报告]
    GenerateReport --> AIInsights[AI洞察报告]
    
    AllureReport --> End([结束])
    AIInsights --> End
```

---

## 二、详细流程说明

### 2.1 配置加载阶段

```mermaid
flowchart LR
    A[开始] --> B[config/settings.py]
    B --> C[Settings类初始化]
    C --> D[加载YAML配置]
    C --> E[加载环境变量]
    C --> F[合并配置]
    
    D --> D1[env_config.yaml<br/>环境配置]
    D --> D2[browser_config.yaml<br/>浏览器配置]
    
    E --> E1[OPENAI_API_KEY]
    E --> E2[ANTHROPIC_API_KEY]
    E --> E3[TEST_ENV]
    
    F --> G[返回配置对象]
    G --> H[结束]
```

**调用模块及作用：**

| 模块 | 文件 | 作用 |
|------|------|------|
| Settings | `config/settings.py` | 统一管理框架配置，支持多环境 |
| load_yaml | `config/settings.py:12` | 读取YAML配置文件 |
| get_env_config | `config/settings.py:25` | 获取当前环境的配置 |
| get_browser_config | `config/settings.py:31` | 获取浏览器配置 |

---

### 2.2 Fixture初始化流程

```mermaid
flowchart TB
    subgraph Traditional[传统测试Fixture]
        T1[page fixture] --> T2[sync_playwright]
        T2 --> T3[launch browser]
        T3 --> T4[new context]
        T4 --> T5[new page]
        T5 --> T6[返回page对象]
        T6 --> T7[测试执行]
        T7 --> T8[测试结束]
        T8 --> T9[context.close]
        T9 --> T10[browser.close]
    end
    
    subgraph AI[AI测试Fixture]
        A1[ai_agent fixture] --> A2{检查@ai marker}
        A2 -->|有marker| A3[创建AIAgentAdapter]
        A2 -->|无marker| A4[返回None]
        A3 --> A5[初始化Browser]
        A5 --> A6[创建LLM实例]
        A6 --> A7[返回adapter]
        A7 --> A8[测试执行]
        A8 --> A9[adapter.close]
    end
    
    subgraph Hybrid[混合测试Fixture]
        H1[smart_page fixture] --> H2[获取page]
        H2 --> H3[获取ai_agent]
        H3 --> H4[创建AIPage]
        H4 --> H5[注入page+ai_adapter]
        H5 --> H6[返回smart_page]
    end
```

**调用模块及作用：**

| Fixture | 文件 | 作用 | 生命周期 |
|---------|------|------|----------|
| page | `tests/conftest.py:35` | 提供Playwright页面实例 | function |
| async_page | `tests/conftest.py:88` | 提供异步Playwright页面 | function |
| ai_agent | `tests/conftest.py:56` | 提供AI Agent适配器 | function |
| async_ai_agent | `tests/conftest.py:103` | 提供异步AI适配器 | function |
| smart_page | `tests/conftest.py:78` | 提供AI增强页面对象 | function |
| base_page | `tests/conftest.py:83` | 提供基础页面对象 | function |

---

### 2.3 传统测试执行流程

```mermaid
flowchart TB
    Start([开始]) --> BasePage[创建BasePage]
    BasePage --> SmartLocator[初始化SmartLocator]
    
    subgraph Operations[页面操作]
        Op1[navigate_to] --> Op2[find元素]
        Op2 --> Op3{元素存在?}
        Op3 -->|是| Op4[执行操作<br/>click/fill等]
        Op3 -->|否| Op5[ElementNotFoundException]
        Op4 --> Op6[Allure记录步骤]
    end
    
    SmartLocator --> Operations
    
    subgraph ElementFind[元素查找流程]
        EF1[主选择器] --> EF2{找到?}
        EF2 -->|否| EF3[备用选择器]
        EF2 -->|是| EF9[返回元素]
        EF3 --> EF4{找到?}
        EF4 -->|否| EF5[AI视觉定位]
        EF4 -->|是| EF9
        EF5 --> EF6{AI可用?}
        EF6 -->|是| EF7[AI_find]
        EF6 -->|否| EF8[抛出异常]
        EF7 --> EF9
    end
    
    Op2 --> ElementFind
    
    Op6 --> Assert[断言验证]
    Assert --> Pass{通过?}
    Pass -->|是| Screenshot[自动截图]
    Pass -->|否| AttachError[附加错误信息]
    
    Screenshot --> End([结束])
    AttachError --> End
    
    Op5 --> SelfHealing{自我修复?}
    SelfHealing -->|是| Heal[尝试修复定位]
    SelfHealing -->|否| Rethrow[重新抛出异常]
    Heal --> EF2
    Rethrow --> End
```

**核心类说明：**

| 类/方法 | 文件 | 作用 |
|---------|------|------|
| BasePage | `pages/base_page.py` | 基础页面对象，封装常用操作 |
| SmartLocator.find | `core/elements/smart_locator.py:25` | 智能元素查找 |
| SelfHealingLocator | `core/elements/self_healing.py` | 自我修复定位 |
| AllureHelper | `core/reporting/allure_helper.py` | Allure报告辅助 |

---

### 2.4 AI测试执行流程

```mermaid
flowchart TB
    Start([开始]) --> CheckMarker{检查@ai marker}
    CheckMarker -->|有| CreateAdapter[创建AIAgentAdapter]
    CheckMarker -->|无| SkipAI[跳过AI初始化]
    
    CreateAdapter --> SelectLLM{选择LLM提供商}
    SelectLLM -->|openai| OpenAI[ChatOpenAI]
    SelectLLM -->|anthropic| Anthropic[ChatAnthropic]
    SelectLLM -->|local| Ollama[ChatOllama]
    
    OpenAI --> CheckKey{检查API Key}
    Anthropic --> CheckKey
    Ollama --> CheckConnection{检查连接}
    
    CheckKey -->|缺失| Error1[抛出ValueError]
    CheckKey -->|存在| InitBrowser[初始化Browser]
    CheckConnection -->|失败| Error2[连接错误]
    CheckConnection -->|成功| InitBrowser
    
    InitBrowser --> CreateAgent[创建Agent]
    CreateAgent --> ExecuteTask[execute_task]
    
    subgraph TaskExecution[任务执行流程]
        TE1[接收自然语言任务] --> TE2[构建完整提示词]
        TE2 --> TE3[调用LLM]
        TE3 --> TE4{执行成功?}
        TE4 -->|是| TE5[返回结果]
        TE4 -->|否| TE6[错误处理]
        TE6 --> TE7[重试?]
        TE7 -->|是| TE3
        TE7 -->|否| TE8[记录失败]
    end
    
    ExecuteTask --> TaskExecution
    TE5 --> RecordResult[记录执行结果]
    TE8 --> RecordResult
    
    RecordResult --> AttachAllure[附加到Allure报告]
    AttachAllure --> AIReport[记录到AI洞察报告]
    
    AIReport --> Verify{验证结果}
    Verify -->|成功| Success([成功])
    Verify -->|失败| Failure([失败])
    
    Error1 --> EndError([异常结束])
    Error2 --> EndError
    SkipAI --> NormalTest[执行传统测试]
    NormalTest --> EndNormal([结束])
```

**调用模块及作用：**

| 模块 | 文件 | 作用 |
|------|------|------|
| AIAgentAdapter | `core/driver/browser_use_adapter.py` | AI Agent适配器主类 |
| _create_llm | `core/driver/browser_use_adapter.py:38` | 创建LLM实例 |
| execute_task | `core/driver/browser_use_adapter.py:68` | 执行自然语言任务 |
| AgentFactory | `core/ai/agent_factory.py` | LLM工厂模式 |
| PromptTemplates | `core/ai/prompt_templates.py` | 提示词模板 |

---

### 2.5 混合测试执行流程

```mermaid
flowchart TB
    Start([开始]) --> CreateAIPage[创建AIPage]
    CreateAIPage --> CheckAIMode{检查AI模式}
    
    CheckAIMode -->|启用| HybridFlow[混合模式执行]
    CheckAIMode -->|禁用| TraditionalOnly[仅传统模式]
    
    subgraph HybridMode[混合模式]
        HM1[传统操作] --> HM2{操作类型}
        HM2 -->|简单操作| HM3[传统方法<br/>click/fill]
        HM2 -->|复杂操作| HM4[AI方法<br/>ai_click/ai_fill]
        HM2 -->|验证| HM5[AI验证<br/>ai_verify]
        
        HM3 --> HM6[记录步骤]
        HM4 --> HM7[AI执行] --> HM8[记录AI日志]
        HM5 --> HM9[AI分析] --> HM10[返回验证结果]
        
        HM6 --> CheckResult{检查结果}
        HM8 --> CheckResult
        HM10 --> CheckResult
    end
    
    HybridFlow --> HybridMode
    
    CheckResult -->|成功| Continue[继续下一步]
    CheckResult -->|失败| HandleFailure[失败处理]
    
    HandleFailure --> CanHeal{可修复?}
    CanHeal -->|是| SelfHeal[自我修复]
    CanHeal -->|否| ReportFailure[报告失败]
    
    SelfHeal --> Retry[重试]
    Retry --> CheckResult
    
    Continue --> MoreSteps{更多步骤?}
    MoreSteps -->|是| HM1
    MoreSteps -->|否| Complete([完成])
    
    ReportFailure --> Complete
    TraditionalOnly --> TSteps[传统步骤] --> Complete
```

**混合模式优势：**
- 稳定流程用传统方式（快速可靠）
- 易变流程用AI方式（自适应）
- 复杂验证用AI方式（智能判断）

---

### 2.6 失败处理与自我修复流程

```mermaid
flowchart TB
    Start([元素定位失败]) --> CaptureState[捕获当前状态]
    
    subgraph FailureCapture[失败信息捕获]
        FC1[截图] --> FC2[获取页面源码]
        FC2 --> FC3[记录错误信息]
        FC3 --> FC4[获取当前URL]
    end
    
    CaptureState --> FailureCapture
    FailureCapture --> AttachAllure[附加到Allure报告]
    
    AttachAllure --> TryHeal{尝试修复?}
    TryHeal -->|是| SelfHealing[自我修复流程]
    TryHeal -->|否| ThrowException[抛出异常]
    
    subgraph SelfHealingFlow[自我修复详细流程]
        SH1[记录失败选择器] --> SH2[尝试常见策略]
        
        SH2 --> SH3[策略1: 添加contains]
        SH3 -->|失败| SH4[策略2: 部分匹配]
        SH4 -->|失败| SH5[策略3: 父子关系调整]
        SH5 -->|失败| SH6[策略4: 不同属性]
        SH6 -->|失败| SH7[AI辅助修复]
        
        SH3 -->|成功| SH8[返回新定位器]
        SH4 -->|成功| SH8
        SH5 -->|成功| SH8
        SH6 -->|成功| SH8
        SH7 -->|成功| SH8
        SH7 -->|失败| SH9[记录修复失败]
    end
    
    SelfHealing --> SelfHealingFlow
    
    SH8 --> VerifyNew[验证新定位器]
    VerifyNew -->|成功| UpdateRegistry[更新元素注册表]
    VerifyNew -->|失败| SH9
    
    UpdateRegistry --> ReturnElement[返回元素]
    ReturnElement --> ContinueTest[继续测试]
    
    SH9 --> CheckRetry{可重试?}
    CheckRetry -->|是| TraditionalRetry[传统重试]
    CheckRetry -->|否| FinalError[最终失败]
    
    TraditionalRetry --> TryHeal
    FinalError --> ThrowException
    ThrowException --> End([结束])
    ContinueTest --> End
```

**自我修复策略：**

| 策略 | 方法 | 说明 |
|------|------|------|
| 添加contains | `_strategy_add_contains` | 使用CSS :has和*=匹配 |
| 部分匹配 | `_strategy_partial_match` | 使用属性*=代替= |
| 父子关系调整 | `_strategy_parent_child_swap` | 调整>和:has(>) |
| 不同属性 | `_strategy_different_attribute` | 尝试data-testid等替代 |
| AI辅助 | `_ai_healing` | 截图AI分析寻找元素 |

---

### 2.7 报告生成流程

```mermaid
flowchart TB
    Start([测试会话结束]) --> CollectResults[收集测试结果]
    
    CollectResults --> GenerateAllure[生成Allure报告]
    CollectResults --> GenerateAI[生成AI洞察报告]
    
    subgraph AllureReport[Allure报告生成]
        AR1[读取allure-results] --> AR2[解析测试结果]
        AR2 --> AR3[生成HTML]
        AR3 --> AR4[生成图表]
        AR4 --> AR5[allure-report/index.html]
    end
    
    subgraph AIReport[AI洞察报告生成]
        IR1[收集AI执行记录] --> IR2[统计成功率]
        IR2 --> IR3[按LLM分组统计]
        IR3 --> IR4[计算平均耗时]
        IR4 --> IR5[生成JSON报告]
        IR5 --> IR6[生成HTML报告]
        IR6 --> IR7[生成可视化图表]
    end
    
    GenerateAllure --> AllureReport
    GenerateAI --> AIReport
    
    AR5 --> MergeReport[合并报告]
    IR7 --> MergeReport
    
    MergeReport --> AddLinks[添加报告链接]
    AddLinks --> Notify[通知完成]
    Notify --> End([结束])
```

**报告内容：**

| 报告类型 | 文件 | 内容 |
|----------|------|------|
| Allure HTML | `reports/allure-report/index.html` | 测试用例详情、趋势图、环境信息 |
| Allure Results | `reports/allure-results/*.json` | 原始测试结果数据 |
| AI Insights JSON | `reports/ai-insights/ai-insights-report.json` | AI执行统计数据 |
| AI Insights HTML | `reports/ai-insights/ai-insights-report.html` | AI执行可视化报告 |

---

## 三、异常处理流程

### 3.1 常见异常及处理

```mermaid
flowchart TB
    subgraph Exceptions[异常类型]
        E1[ElementNotFoundException<br/>元素未找到] 
        E2[TimeoutError<br/>超时]
        E3[AssertionError<br/>断言失败]
        E4[APIError<br/>AI API错误]
        E5[NetworkError<br/>网络错误]
        E6[BrowserCrash<br/>浏览器崩溃]
    end
    
    subgraph Handlers[处理策略]
        H1[自我修复定位]
        H2[自动重试]
        H3[截图记录]
        H4[切换LLM]
        H5[网络重连]
        H6[重启浏览器]
    end
    
    E1 -->|触发| H1
    E1 -->|失败| H2
    E2 --> H2
    E3 --> H3
    E4 --> H4
    E4 --> H2
    E5 --> H5
    E5 --> H2
    E6 --> H6
    E6 --> H2
```

### 3.2 pytest hook异常处理

```mermaid
flowchart LR
    A[pytest_runtest_makereport] --> B{when?}
    B -->|call| C{excinfo?}
    C -->|有异常| D[获取page对象]
    D --> E[截图]
    D --> F[获取页面源码]
    D --> G[获取浏览器日志]
    
    E --> H[附加到Allure]
    F --> H
    G --> H
    
    C -->|无异常| I[检查是否需要截图]
    I -->|需要| E
    I -->|不需要| J[正常结束]
    
    H --> J
```

---

## 四、关键调用链

### 4.1 传统测试调用链

```
test_login.py::TestLogin::test_successful_login
├── conftest.py::page(fixture)
│   └── sync_playwright().start()
│       └── chromium.launch()
│           └── new_context()
│               └── new_page()
│                   └── YIELD page
├── pages/base_page.py::BasePage.__init__(page)
│   └── core/elements/smart_locator.py::SmartLocator.__init__()
├── BasePage.navigate_to(url)
│   └── page.goto(url)
├── BasePage.fill(selector, value)
│   ├── SmartLocator.find(selector)
│   │   ├── page.locator(selector)
│   │   └── locator.wait_for()
│   └── element.fill(value)
├── BasePage.click(selector)
│   └── SmartLocator.find(selector)
│       └── element.click()
└── conftest.py::page(fixture teardown)
    ├── screenshot (if failed)
    ├── context.close()
    └── browser.close()
```

### 4.2 AI测试调用链

```
test_natural_language.py::TestNaturalLanguage::test_shopping
├── conftest.py::async_ai_agent(fixture)
│   └── Check @ai marker
│       └── AIAgentAdapter.__init__(llm_provider="openai")
│           ├── _create_llm("openai")
│           │   └── ChatOpenAI(model="gpt-4o")
│           └── Browser(headless=False)
│               └── YIELD adapter
├── core/driver/browser_use_adapter.py::execute_task(task)
│   ├── PromptTemplates.format_base_task(task)
│   └── Agent(task=task, llm=self.llm, browser=self.browser)
│       └── agent.run()
│           ├── LLM分析任务
│           ├── 执行浏览器操作
│           └── 返回结果
├── core/reporting/allure_helper.py::attach_ai_execution()
│   └── allure.attach(result)
└── conftest.py::async_ai_agent(fixture teardown)
    └── adapter.close()
        └── browser.close()
```

### 4.3 混合测试调用链

```
test_e2e_with_ai.py::TestE2EWithAI::test_login_then_ai
├── conftest.py::async_smart_page(fixture)
│   └── AIPage(page, ai_adapter)
│       ├── BasePage.__init__(page)
│       └── YIELD smart_page
├── AIPage.navigate_to(url) [传统]
│   └── page.goto(url)
├── AIPage.ai_fill_form(form_data) [AI]
│   ├── check _smart_mode
│   ├── PromptTemplates.format_form_filling()
│   └── AIAgentAdapter.execute_task()
│       └── Agent.run()
├── AIPage.ai_verify(expectation) [AI验证]
│   └── execute_task(f"验证: {expectation}")
│       └── 返回success
└── 断言结果
```

---

## 五、数据流向图

```mermaid
flowchart LR
    subgraph Input[输入]
        I1[测试用例.py]
        I2[test_data.yaml]
        I3[ai_scenarios.json]
        I4[.env环境变量]
    end
    
    subgraph Process[处理]
        P1[pytest]
        P2[fixtures]
        P3[页面对象]
        P4[AI Agent]
        P5[Playwright]
    end
    
    subgraph Output[输出]
        O1[allure-results/]
        O2[allure-report/]
        O3[ai-insights/]
        O4[screenshots/]
        O5[控制台日志]
    end
    
    I1 --> P1
    I2 --> P2
    I3 --> P4
    I4 --> P1
    
    P1 --> P2
    P2 --> P3
    P2 --> P4
    P3 --> P5
    P4 --> P5
    
    P5 --> O4
    P4 --> O3
    P3 --> O1
    P1 --> O1
    
    O1 --> O2
```

---

## 六、时序图

### 6.1 完整测试执行时序

```mermaid
sequenceDiagram
    participant T as 测试用例
    participant C as conftest
    participant P as Playwright
    participant B as BasePage/AIPage
    participant S as SmartLocator
    participant A as AIAdapter
    participant L as LLM
    participant R as AllureReport
    
    T->>C: 请求fixture
    C->>P: sync_playwright().start()
    P->>P: launch browser
    P->>P: new context
    P->>C: return page
    C->>T: inject page
    
    T->>B: BasePage(page)
    B->>S: SmartLocator(page)
    S-->>B: return locator
    
    T->>B: navigate_to(url)
    B->>P: page.goto(url)
    
    T->>B: click(selector)
    B->>S: find(selector)
    S->>P: locator(selector)
    P-->>S: element
    S-->>B: element
    B->>P: element.click()
    B->>R: 记录步骤
    
    Note over T,R: AI模式执行
    T->>A: execute_task(task)
    A->>A: _create_llm()
    A->>L: ChatOpenAI()
    L-->>A: llm instance
    A->>L: agent.run(task)
    L->>P: 执行浏览器操作
    P-->>L: 操作结果
    L-->>A: 执行结果
    A->>R: attach_ai_execution()
    
    T->>C: 测试结束
    C->>P: context.close()
    C->>P: browser.close()
    C->>R: 生成报告
```

---

## 七、总结

本框架的执行流程具有以下特点：

1. **分层设计**：配置层 → Fixture层 → 页面层 → 测试层
2. **双模式支持**：传统模式稳定快速，AI模式智能自适应
3. **自我修复**：元素变化时自动修复，提高测试稳定性
4. **丰富报告**：Allure专业报告 + AI洞察报告双重保障
5. **完善的异常处理**：多层级重试和恢复机制

**关键设计决策：**
- 使用pytest fixture管理资源生命周期
- 页面对象模式分离业务逻辑和测试代码
- AI作为增强而非替代，保留传统测试的优势
- 自愈机制降低维护成本
