# Week 3: AI 能力 - 智能化测试实践

> 🎯 本周目标：掌握 AI 驱动测试，学会使用自然语言描述测试，理解 AI 与传统测试的结合

---

## 📚 学习路线图

```
Day 1-2: 配置 AI 环境，理解 AIAgentAdapter
Day 3-4: 自然语言测试编写
Day 5-6: 混合模式测试实践
Day 7:    AI 测试最佳实践与调优
```

---

## Day 1-2: AI 环境配置与核心组件

### 2.1 配置 AI 环境

#### 获取 API 密钥

**OpenAI (推荐新手):**
1. 访问 https://platform.openai.com/
2. 注册/登录账号
3. 点击 API → API Keys
4. 创建新的 API Key
5. 复制密钥（注意：只显示一次！）

**Anthropic Claude:**
1. 访问 https://console.anthropic.com/
2. 注册账号
3. 在 Dashboard 中获取 API Key

**Kimi (Moonshot AI) - 国内大模型:**
1. 访问 https://platform.moonshot.cn/
2. 注册/登录账号
3. 进入控制台 → API Key 管理
4. 创建新的 API Key
5. 复制密钥

**DeepSeek - 国内大模型:**
1. 访问 https://platform.deepseek.com/
2. 注册/登录账号
3. 进入 API Keys 页面
4. 创建新的 API Key
5. 复制密钥（国内访问速度快，价格实惠）

**本地 Ollama (免费方案):**
1. 安装 Ollama: https://ollama.com/download
2. 运行模型：`ollama run llama3.2`
3. 默认使用本地 http://localhost:11434

#### 配置环境变量

```bash
# .env 文件

# 国际大模型
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# 国内大模型（推荐国内用户使用）
KIMI_API_KEY=your-kimi-key-here          # Moonshot AI
DEEPSEEK_API_KEY=your-deepseek-key-here  # DeepSeek

# 可选：本地 LLM
OLLAMA_BASE_URL=http://localhost:11434
```

#### 验证配置

```python
# tests/test_ai_setup.py
import pytest
from core.driver.browser_use_adapter import AIAgentAdapter

@pytest.mark.ai
class TestAISetup:
    """验证 AI 配置是否正确"""

    def test_openai_connection(self):
        """测试 OpenAI 连接"""
        try:
            adapter = AIAgentAdapter(llm_provider="openai")
            assert adapter.llm is not None
            print("✅ OpenAI 配置成功")
        except Exception as e:
            pytest.fail(f"OpenAI 配置失败: {e}")

    def test_anthropic_connection(self):
        """测试 Anthropic 连接"""
        try:
            adapter = AIAgentAdapter(llm_provider="anthropic")
            assert adapter.llm is not None
            print("✅ Anthropic 配置成功")
        except Exception as e:
            pytest.fail(f"Anthropic 配置失败: {e}")

    def test_kimi_connection(self):
        """测试 Kimi (Moonshot) 连接 - 国内大模型"""
        try:
            adapter = AIAgentAdapter(llm_provider="kimi")
            assert adapter.llm is not None
            print("✅ Kimi 配置成功")
        except Exception as e:
            pytest.fail(f"Kimi 配置失败: {e}")

    def test_deepseek_connection(self):
        """测试 DeepSeek 连接 - 国内大模型"""
        try:
            adapter = AIAgentAdapter(llm_provider="deepseek")
            assert adapter.llm is not None
            print("✅ DeepSeek 配置成功")
        except Exception as e:
            pytest.fail(f"DeepSeek 配置失败: {e}")
```

### 2.2 AIAgentAdapter 核心组件

```python
from core.driver.browser_use_adapter import AIAgentAdapter

# 1. 创建适配器
adapter = AIAgentAdapter(
    llm_provider="openai",    # 选择 LLM 提供商
    headless=False,           # 是否无头模式
    use_vision=True,          # 是否启用视觉能力
    max_iterations=50         # 最大迭代次数
)

# 2. 执行自然语言任务
result = await adapter.execute_task(
    task="在搜索框输入'Python教程'并点击搜索",
    context={                 # 可选：提供上下文
        "search_keyword": "Python教程",
        "expected_results": "Python相关教程"
    }
)

# 3. 检查结果
print(f"成功: {result.success}")
print(f"步骤: {result.steps}")
print(f"耗时: {result.duration}秒")

# 4. 关闭适配器
await adapter.close()
```

#### AIAgentAdapter 工作原理

```
用户输入自然语言指令
        ↓
AIAgentAdapter.execute_task()
        ↓
构建任务提示词（Prompt）
        ↓
LLM 分析任务 → 生成执行步骤
        ↓
浏览器执行步骤（点击、输入、验证）
        ↓
返回执行结果
```

### 2.3 不同 LLM 提供商对比

| 提供商 | 优势 | 劣势 | 适用场景 | 备注 |
|--------|------|------|----------|------|
| OpenAI GPT-4o | 能力最强，速度快 | 需要付费，国内需代理 | 生产环境 | 国际主流 |
| Anthropic Claude | 推理能力强，稳定性好 | 价格较高，国内需代理 | 复杂任务 | 国际主流 |
| **Kimi (Moonshot)** | 国内访问快，中文好 | 功能略逊于 GPT-4 | 国内项目 | **推荐国内用户** |
| **DeepSeek** | 价格便宜，国内访问快 | 模型规模较小 | 国内项目/预算有限 | **推荐国内用户** |
| Ollama 本地 | 免费，数据私密 | 需要硬件资源 | 学习/开发 | 本地部署 |

---

## Day 3-4: 自然语言测试编写

### 4.1 第一个 AI 测试

```python
# tests/ai_driven/test_ai_basics.py
import pytest
import allure

@pytest.mark.ai
@allure.feature("AI 基础测试")
class TestAIBasics:
    """AI 测试入门示例"""
    
    @allure.title("AI 自动完成百度搜索")
    async def test_ai_baidu_search(self, async_ai_agent, async_page):
        """测试 AI 自动完成百度搜索流程"""
        # 1. 打开百度
        await async_page.goto("https://www.baidu.com")
        
        # 2. 让 AI 执行任务（只需说人话！）
        result = await async_ai_agent.execute_task("""
            在搜索框输入"Python自动化测试"，
            然后点击"百度一下"按钮进行搜索
        """)
        
        # 3. 验证成功
        assert result.success, f"任务失败: {result.errors}"
        
        # 4. 附加到报告
        allure.attach(
            str(result.steps),
            name="AI 执行步骤",
            attachment_type=allure.attachment_type.TEXT
        )
    
    @allure.title("AI 完成复杂表单填写")
    async def test_ai_fill_form(self, async_ai_agent, async_page):
        """测试 AI 自动填写复杂表单"""
        await async_page.goto("https://example.com/register")
        
        result = await async_ai_agent.execute_task(
            task="填写用户注册表单",
            context={
                "user_info": {
                    "username": "testuser123",
                    "email": "test@example.com",
                    "password": "TestPass123!",
                    "confirm_password": "TestPass123!"
                },
                "requirements": [
                    "用户名至少6位",
                    "密码需要包含大小写字母和数字",
                    "必须同意用户协议"
                ]
            }
        )
        
        assert result.success
```

### 4.2 自然语言测试 vs 传统测试

**传统测试：**
```python
def test_login_traditional(page):
    # 必须知道具体的选择器
    page.goto("https://example.com/login")
    page.fill("#username", "test")
    page.fill("#password", "pass")
    page.click("button[type='submit']")
    expect(page).to_have_url("/dashboard")
```

**AI 测试：**
```python
async def test_login_ai(async_ai_agent, async_page):
    # 只需描述要做什么
    await async_page.goto("https://example.com/login")
    
    result = await async_ai_agent.execute_task("""
        使用用户名 test 和密码 pass 登录系统，
        验证登录成功后跳转到仪表盘页面
    """)
    
    assert result.success
```

**对比总结：**

| 维度 | 传统测试 | AI 测试 |
|------|----------|---------|
| 代码量 | 较多 | 较少 |
| 维护成本 | 页面改版需修改 | 自适应页面变化 |
| 稳定性 | 依赖选择器 | 依赖 AI 理解能力 |
| 执行速度 | 快 | 稍慢 |
| 成本 | 低 | API 调用费用 |

### 4.3 复杂场景 AI 测试

```python
@pytest.mark.ai
@allure.feature("AI 复杂场景")
class TestAIComplexScenarios:
    """复杂场景 AI 测试"""
    
    @allure.title("AI 完成完整购物流程")
    async def test_ai_shopping_journey(self, async_ai_agent, async_page):
        """让 AI 完成从浏览到下单的完整流程"""
        await async_page.goto("https://example-shop.com")
        
        result = await async_ai_agent.execute_task("""
            完成以下购物流程：
            1. 在首页搜索框输入"无线耳机"
            2. 选择第一个搜索结果
            3. 选择颜色为黑色，数量为2
            4. 点击"加入购物车"
            5. 进入购物车查看
            6. 点击"去结算"
            7. 填写收货地址（使用测试地址）
            8. 选择支付方式为"支付宝"
            9. 确认订单
            10. 验证订单提交成功，记录订单号
        """)
        
        assert result.success
        assert "订单号" in str(result.steps)
    
    @allure.title("AI 自适应页面变化")
    async def test_ai_adaptive(self, async_ai_agent, async_page):
        """测试 AI 自适应页面变化的能力"""
        await async_page.goto("https://example.com/unstable-page")
        
        # 即使页面结构经常变化，AI 也能完成任务
        result = await async_ai_agent.execute_task("""
            当前页面布局可能经常变化，请：
            1. 找到"用户反馈"入口（可能在导航栏、页脚或侧边栏）
            2. 点击打开反馈表单
            3. 填写反馈内容："页面加载速度需要优化"
            4. 选择反馈类型为"性能问题"
            5. 提交反馈
            6. 验证显示"感谢您的反馈"
        """)
        
        assert result.success
```

---

## Day 5-6: 混合模式测试实践

### 5.1 为什么要混合模式？

AI 测试虽然智能，但也有缺点：
- 执行速度慢（需要 AI 推理）
- API 调用成本高
- 结果不如传统测试稳定

**混合模式的优势：**
- 稳定流程用传统方式（快速可靠）
- 易变流程用 AI 方式（自适应）
- 复杂验证用 AI 方式（智能判断）

### 5.2 AIPage 双模式页面对象

```python
from pages.ai_page import AIPage

class TestHybrid:
    """混合模式测试示例"""
    
    async def test_login_with_ai_verification(self, async_smart_page, async_page):
        """传统登录 + AI 验证"""
        smart_page = async_smart_page
        
        # ========== 传统模式：稳定的登录流程 ==========
        smart_page.navigate_to("https://example.com/login")
        smart_page.fill("#username", "test@example.com")  # 传统方式，精确快速
        smart_page.fill("#password", "TestPass123!")
        smart_page.click("#submit-btn")
        smart_page.wait_for_page_load()
        
        # ========== AI 模式：智能验证登录结果 ==========
        # AI 可以判断多种登录成功的情况
        is_logged_in = await smart_page.ai_verify("""
            用户已成功登录系统，页面上应该显示：
            - 用户头像或用户名
            - 退出登录按钮
            - 个人中心入口
        """)
        
        assert is_logged_in
    
    async def test_search_with_ai_filter(self, async_smart_page, async_page):
        """传统搜索 + AI 智能筛选"""
        smart_page = async_smart_page
        
        # 传统方式：执行搜索
        smart_page.navigate_to("https://example-shop.com")
        smart_page.fill("#search", "laptop")
        smart_page.click("#search-btn")
        smart_page.wait_for_element_visible(".product-list")
        
        # AI 方式：智能筛选复杂条件
        result = await smart_page.ai_complete_task("""
            在搜索结果中完成以下筛选：
            1. 价格范围：5000-8000元
            2. 品牌选择：联想、戴尔或惠普
            3. 内存：至少16GB
            4. 评分：4星以上
            5. 按销量排序
            6. 选择第一个符合条件的商品
        """)
        
        assert result.success
```

### 5.3 混合模式最佳实践

```python
@pytest.mark.hybrid
@allure.feature("混合模式最佳实践")
class TestHybridBestPractices:
    """混合模式最佳实践示例"""
    
    async def test_stable_flow_traditional(self, async_page):
        """稳定流程优先使用传统方式"""
        # ✅ 登录流程稳定，用传统方式
        base = BasePage(async_page)
        base.navigate_to("https://example.com/login")
        base.fill("#username", "user")
        base.fill("#password", "pass")
        base.click("#login-btn")
        
        # ✅ 页面跳转验证，用传统方式
        assert "dashboard" in async_page.url
    
    async def test_changing_flow_ai(self, async_smart_page, async_page):
        """易变流程使用 AI 方式"""
        # ✅ 推荐算法经常变，用 AI 方式
        smart_page = async_smart_page
        await async_page.goto("https://example.com/recommendations")
        
        result = await smart_page.ai_complete_task("""
            找到"猜你喜欢"区域的商品，
            选择评分最高的一个商品
        """)
        # 即使推荐区域位置变了，AI 也能找到
        
        assert result.success
    
    async def test_complex_validation_ai(self, async_smart_page, async_page):
        """复杂验证使用 AI 方式"""
        smart_page = async_smart_page
        
        # 先加载数据
        await async_page.goto("https://example.com/reports")
        
        # ✅ 复杂的报表数据验证，用 AI 方式
        is_valid = await smart_page.ai_verify("""
            报表数据应该满足以下条件：
            1. 销售额比上个月增长至少 10%
            2. 退货率低于 5%
            3. 图表显示正确的趋势线（上升）
            4. 所有关键指标都有数据
        """)
        
        assert is_valid
```

---

## Day 7: AI 测试最佳实践

### 7.1 提示词 (Prompt) 优化技巧

**不好的提示词：**
```python
result = await adapter.execute_task("测试登录功能")
# 太模糊，AI 不知道具体要做什么
```

**好的提示词：**
```python
result = await adapter.execute_task("""
    任务：测试用户登录功能
    
    前置条件：
    - 当前在登录页面 https://example.com/login
    
    操作步骤：
    1. 在用户名输入框填写 "test@example.com"
    2. 在密码输入框填写 "TestPass123!"
    3. 点击"登录"按钮
    4. 等待页面跳转
    
    期望结果：
    - 页面跳转到 https://example.com/dashboard
    - 页面显示用户名 "test"
    - 显示"欢迎回来"提示
""")
```

### 7.2 成本优化策略

```python
class TestAIOptimization:
    """AI 测试成本优化"""
    
    # 策略1：只在必要时使用 AI
    async def test_selective_ai(self, async_page, async_ai_agent):
        """选择性使用 AI"""
        # 传统方式：快速执行稳定流程
        base = BasePage(async_page)
        base.navigate_to("https://example.com")
        
        # 检查是否需要 AI 介入
        if base.is_visible(".complex-form"):
            # 只有复杂表单才用 AI
            result = await async_ai_agent.execute_task("填写复杂表单")
        else:
            # 简单表单用传统方式
            base.fill("#simple-input", "value")
    
    # 策略2：批量任务减少 API 调用
    async def test_batch_tasks(self, async_ai_agent, async_page):
        """批量执行减少调用次数"""
        await async_page.goto("https://example.com")
        
        # 一次性让 AI 完成多个相关任务
        result = await async_ai_agent.execute_task("""
            完成以下任务：
            1. 打开用户设置页面
            2. 修改昵称为"TestUser"
            3. 上传头像图片
            4. 修改密码
            5. 保存设置
            6. 验证保存成功
        """)
        # 比分成 6 个单独任务更节省 API 调用
    
    # 策略3：使用本地 LLM 进行开发测试
    async def test_with_local_llm(self, async_page):
        """开发阶段使用本地 LLM 节省成本"""
        # 开发测试用本地模型
        local_adapter = AIAgentAdapter(llm_provider="local")
        
        result = await local_adapter.execute_task("测试任务")
        
        # 生产环境用 OpenAI
        # openai_adapter = AIAgentAdapter(llm_provider="openai")
```

### 7.3 常见错误与解决

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| AI 找不到元素 | 描述不够清晰 | 提供更多上下文信息 |
| AI 操作超时 | 任务太复杂 | 拆分成小任务 |
| AI 理解错误 | 提示词有歧义 | 使用更精确的描述 |
| API 调用失败 | 网络或密钥问题 | 检查网络和 API Key |
| 成本过高 | 调用次数太多 | 优化提示词，合并任务 |

### 7.4 练习项目：AI 测试套件

```python
# tests/ai_driven/test_week3_project.py
"""
Week 3 综合项目：为电商网站编写 AI 测试套件
"""
import pytest
import allure

@pytest.mark.ai
@allure.epic("AI 驱动测试套件")
class TestWeek3AIProject:
    """Week 3 综合练习项目"""
    
    @allure.title("项目1: AI 探索测试")
    async def test_ai_exploratory(self, async_ai_agent, async_page):
        """
        让 AI 自主探索网站功能，找出潜在问题
        """
        await async_page.goto("https://example-shop.com")
        
        result = await async_ai_agent.execute_task("""
            你是一个测试工程师，请探索这个电商网站：
            
            1. 尝试找到并使用以下功能：
               - 搜索商品
               - 浏览分类
               - 查看商品详情
               - 添加购物车
               - 用户注册/登录
            
            2. 记录你发现的任何问题：
               - 功能不可用
               - 页面加载错误
               - 界面显示异常
               - 操作不流畅
            
            3. 给出测试报告
        """)
        
        allure.attach(str(result.steps), "探索过程")
        # 这里不要求断言成功，而是收集 AI 的发现
    
    @allure.title("项目2: AI 回归测试")
    async def test_ai_regression(self, async_ai_agent, async_page):
        """
        使用 AI 进行智能回归测试
        """
        await async_page.goto("https://example-shop.com")
        
        result = await async_ai_agent.execute_task("""
            执行核心业务流程回归测试：
            
            场景1: 新用户注册 → 登录 → 浏览商品 → 下单
            场景2: 老用户登录 → 查看订单 → 申请退款
            场景3: 搜索商品 → 筛选 → 排序 → 加入购物车
            
            验证每个场景都能正常完成，
            记录任何异常或功能变更。
        """)
        
        assert result.success
        allure.attach(str(result.steps), "回归测试报告")
    
    @allure.title("项目3: AI 兼容性测试")
    async def test_ai_compatibility(self, async_ai_agent, async_page):
        """
        让 AI 测试页面在不同情况下的表现
        """
        await async_page.goto("https://example-shop.com")
        
        result = await async_ai_agent.execute_task("""
            测试以下边界情况：
            
            1. 空购物车点击结算
            2. 搜索不存在的关键词
            3. 输入超长文本（1000个字符）
            4. 快速连续点击按钮
            5. 在未登录状态下访问订单页面
            
            验证系统是否能正确处理这些异常情况。
        """)
        
        assert result.success
```

---

## 📝 Week 3 作业清单

- [ ] 配置好至少一种 AI 环境（OpenAI/Anthropic/Ollama）
- [ ] 编写 3 个纯 AI 驱动测试用例
- [ ] 编写 3 个混合模式测试用例
- [ ] 优化 AI 提示词，提高执行成功率到 90% 以上
- [ ] 完成 Week 3 综合项目

---

## 💡 本周重点回顾

1. **AI 测试核心价值**：
   - 自然语言描述，降低编写门槛
   - 自适应页面变化，减少维护成本
   - 智能验证复杂场景

2. **混合模式精髓**：
   - 传统方式：稳定流程，快速执行
   - AI 方式：易变流程，智能适应
   - 合理搭配：取长补短，高效测试

3. **成本优化要点**：
   - 只在必要时使用 AI
   - 批量任务减少 API 调用
   - 开发用本地，生产用云端

---

**恭喜完成 Week 3！** 你已经掌握了 AI 驱动测试的核心技能。继续 Week 4 完成实战项目！
