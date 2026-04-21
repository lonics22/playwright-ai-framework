# 🚀 Playwright AI 框架 - 新手入门完全指南

> 从零开始，手把手教你搭建并运行第一个自动化测试

---

## 📋 第一步：准备工作（就像准备做饭前要洗好菜）

### 1.1 确认你的电脑有这些"工具"

就像做菜需要锅碗瓢盆一样，写代码也需要一些基础工具：

```
📦 必备清单：
├── ✅ Python 3.11+ (我们的"主厨"，必须安装)
├── ✅ Git (用来下载代码的"运输工具")
├── ✅ 代码编辑器 VS Code (推荐) 或 PyCharm
└── ✅ 稳定的网络 (下载东西要用)
```

### 1.2 检查 Python 是否安装

**Windows 用户：**
1. 按下 `Win + R` 键
2. 输入 `cmd` 回车（打开黑窗口）
3. 输入以下命令：

```bash
python --version
```

看到类似 `Python 3.11.4` 的字样就说明安装成功了！

**Mac 用户：**
1. 打开"终端"（在 应用程序 -> 实用工具 里）
2. 输入：

```bash
python3 --version
```

> 💡 **小提示**：如果提示"找不到命令"，先去官网下载安装 Python：https://www.python.org/downloads/

---

## 📥 第二步：下载框架代码（把菜谱拿回家）

### 2.1 使用 Git 下载（推荐）

```bash
# 1. 先找个地方放代码（比如桌面）
cd Desktop

# 2. 下载代码
git clone https://github.com/your-username/playwright-ai-framework.git

# 3. 进入项目文件夹
cd playwright-ai-framework
```

**看不懂？没关系，图解来了：**

```
┌─────────────────────────────────────────────────────┐
│  你的电脑                                             │
│  ┌─────────────┐                                     │
│  │   桌面      │                                     │
│  │  ┌─────────┐│  ← git clone 后自动生成             │
│  │  │  📁     ││                                     │
│  │  │playwright│                                    │
│  │  │-ai-frame │                                    │
│  │  │ work    ││                                     │
│  │  │ 文件夹   ││                                     │
│  │  └─────────┘│                                     │
│  └─────────────┘                                     │
└─────────────────────────────────────────────────────┘
```

### 2.2 如果没有 Git

直接去网页下载 ZIP 包：
1. 打开项目网页
2. 点击绿色按钮 "Code" → "Download ZIP"
3. 解压到桌面

---

## 🏗️ 第三步：创建虚拟环境（给项目建个"独立小屋"）

**为什么要这样做？**

想象你在做蛋糕，需要特定品牌的面粉。虚拟环境就像给这个蛋糕专门准备的一个储物柜，里面放它需要的所有材料，不会和其他蛋糕的材料混在一起。

### 3.1 创建虚拟环境

```bash
# Windows
python -m venv .venv

# Mac
python3 -m venv .venv
```

### 3.2 激活虚拟环境

**Windows：**
```bash
.venv\Scripts\activate
```

**Mac：**
```bash
source .venv/bin/activate
```

**成功标志：** 你会看到命令行前面多了 `(.venv)` 字样

```
# 激活前：
C:\Users\你的名字\Desktop\playwright-ai-framework>

# 激活后：
(.venv) C:\Users\你的名字\Desktop\playwright-ai-framework>
        ↑
     看到这个就是成功了！
```

---

## 📦 第四步：安装依赖（准备食材）

### 4.1 安装 Python 包

在激活虚拟环境的状态下，输入：

```bash
pip install -r requirements.txt
```

**这个过程会安装什么？**

```
📦 正在安装的"食材"：
├── pytest 🧪         ← 测试框架（相当于"烤箱"）
├── playwright 🎭     ← 浏览器自动化（相当于"锅铲"）
├── allure-pytest 📊  ← 报告工具（相当于"摆盘装饰"）
├── browser-use 🤖    ← AI 功能（相当于"智能助手"）
├── langchain 🔗      ← AI 连接工具
└── ... 其他辅助工具
```

> ⏰ **等待时间**：根据网络情况，大概需要 2-5 分钟。看到绿色文字 "Successfully installed" 就是成功了！

### 4.2 安装浏览器

Playwright 需要特定的浏览器版本，输入：

```bash
playwright install chromium
```

**这是什么意思？**

就像下载了一个特定版本的 Chrome 浏览器专门给自动化测试用，不会影响你平时上网的浏览器。

---

## ⚙️ 第五步：配置环境变量（设置"密码本"）

### 5.1 复制配置文件

```bash
# Windows
copy .env.example .env

# Mac/Linux
cp .env.example .env
```

### 5.2 编辑 .env 文件

用 VS Code 打开项目文件夹，找到 `.env` 文件：

```
📁 playwright-ai-framework
   ├── 📄 .env ← 修改这个文件
   └── 📄 .env.example
```

**文件内容改成这样：**

```env
# API Keys for AI Testing（AI测试用的密钥）
# 如果你只想跑传统测试，可以先不管这些
OPENAI_API_KEY=sk-你的openai密钥
ANTHROPIC_API_KEY=sk-ant-你的anthropic密钥

# Test Environment（测试环境）
TEST_ENV=default

# Browser Configuration（浏览器配置）
BROWSER=headless
```

> 💡 **新手提示**：如果你没有 OpenAI 密钥，没关系！可以先跑传统测试，不需要填这个。

---

## 📝 第六步：写第一个测试用例（做第一道菜）

### 6.1 创建测试文件

在 `tests/traditional/` 文件夹下新建一个文件 `test_my_first.py`：

```
📁 playwright-ai-framework
   ├── 📁 tests
   │   ├── 📁 traditional
   │   │   └── 📄 test_my_first.py ← 新建这个文件
   │   └── ...
```

### 6.2 写入测试代码

把下面的代码复制进去：

```python
# tests/traditional/test_my_first.py
import allure
from pages.base_page import BasePage

@allure.feature("我的第一个测试")
class TestMyFirst:
    """这是注释：新手入门测试"""

    @allure.title("访问百度首页")
    def test_visit_baidu(self, page):
        """测试打开百度首页"""
        # 1. 创建页面对象（拿起锅铲）
        base_page = BasePage(page)
        
        # 2. 打开百度（开火炒菜）
        base_page.navigate_to("https://www.baidu.com")
        
        # 3. 等待页面加载完成（等待菜熟）
        base_page.wait_for_page_load()
        
        # 4. 验证页面标题包含"百度"（尝一口看味道对不对）
        assert "百度" in base_page.get_page_title()
        
        # 5. 截图留念（拍照发朋友圈）
        base_page.take_screenshot("百度首页")
```

**代码解释图解：**

```
🎯 测试代码就像做一道菜的步骤：

Step 1: 准备工具（import + 创建对象）
   ↓
Step 2: 开火下锅（navigate_to 打开网页）
   ↓
Step 3: 等待煮熟（wait_for_page_load）
   ↓
Step 4: 尝味道（assert 断言验证）
   ↓
Step 5: 拍照记录（take_screenshot）
```

---

## ▶️ 第七步：运行测试（开始做菜！）

### 7.1 运行单个测试

在终端输入：

```bash
pytest tests/traditional/test_my_first.py -v
```

**你会看到类似这样的输出：**

```
================================= test session starts ==================================
platform win32 -- Python 3.11.4, pytest-8.0.0, pluggy-1.0.0
rootdir: d:\softfile\playwright-ai-framework-master
collected 1 item

tests\traditional\test_my_first.py::TestMyFirst::test_visit_baidu PASSED          [100%]

================================== 1 passed in 3.42s ==================================
```

**看到绿色的 PASSED 就说明成功了！** 🎉

### 7.2 如果看到红色 FAILED

不要慌，看看错误信息：

```
FAILED tests/traditional/test_my_first.py::TestMyFirst::test_visit_baidu
AssertionError: assert '百度' in 'Google'
```

这说明网页标题不对，可能是网络问题或者网页变了。

---

## 📊 第八步：查看测试报告（欣赏成品）

### 8.1 生成 Allure 报告

```bash
# 1. 生成报告数据
pytest tests/traditional/test_my_first.py --alluredir=reports/allure-results

# 2. 生成 HTML 报告
allure generate reports/allure-results -o reports/allure-report --clean

# 3. 打开报告
allure open reports/allure-report
```

**报告长什么样？**

```
📊 Allure 报告包含：
├── 📈 测试总览（跑了多少，通过多少）
├── 📋 测试用例列表（每个测试的详细信息）
├── 🖼️ 截图附件（你拍的"照片"）
├── ⏱️ 执行时间（花了多长时间）
└── 🏷️ 标签分类（按功能分组）
```

### 8.2 报告截图示意

```
┌─────────────────────────────────────────────────────┐
│  Allure Report                                       │
│  ┌───────────────────────────────────────────────┐  │
│  │  🟢 1 Passed  🔴 0 Failed  ⚪ 0 Skipped       │  │
│  └───────────────────────────────────────────────┘  │
│                                                      │
│  📁 我的第一个测试                                   │
│  └── 📝 访问百度首页                          ✅    │
│       ├─ ⏱️ Duration: 3.42s                         │
│       ├─ 🖼️ 百度首页.png                            │
│       └─ 📄 详细日志...                             │
└─────────────────────────────────────────────────────┘
```

---

## 🧪 第九步：尝试 AI 测试（进阶玩法）

### 9.1 配置 AI 密钥

如果你有 OpenAI API 密钥，在 `.env` 文件中设置：

```env
OPENAI_API_KEY=sk-你的密钥在这里
```

### 9.2 创建 AI 测试

新建文件 `tests/ai_driven/test_ai_demo.py`：

```python
import pytest
import allure

@pytest.mark.ai
@allure.feature("AI 演示测试")
class TestAIDemo:
    
    @allure.title("AI 自动搜索")
    async def test_ai_search(self, async_ai_agent, async_page):
        """让 AI 自动完成搜索任务"""
        # 打开百度
        await async_page.goto("https://www.baidu.com")
        
        # 让 AI 执行搜索
        result = await async_ai_agent.execute_task(
            "在搜索框输入'Python教程'并点击搜索按钮"
        )
        
        # 验证成功
        assert result.success
```

### 9.3 运行 AI 测试

```bash
pytest tests/ai_driven/test_ai_demo.py -v -m ai
```

**AI 测试有什么不同？**

```
传统测试：
你告诉电脑：点击 id='kw' 的元素，输入"Python教程"

AI 测试：
你告诉电脑：在搜索框输入"Python教程"
电脑自己找搜索框，不用你告诉它具体位置
```

---

## 🔧 常见问题排查（ troubleshooting ）

### Q1: 提示 "pip 不是内部或外部命令"

**原因**：Python 安装时没勾选 "Add to PATH"

**解决**：
1. 重新安装 Python
2. 安装时勾选 "Add Python to PATH"

### Q2: 提示 "playwright 不是内部或外部命令"

**原因**：虚拟环境没激活

**解决**：
```bash
# 重新激活虚拟环境
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac
```

### Q3: 浏览器启动失败

**原因**： playwright 浏览器没装好

**解决**：
```bash
playwright install chromium
```

### Q4: 测试运行时浏览器一闪而过

**这是正常的！** 

如果不想看到浏览器（无头模式），在 `.env` 中设置：
```env
BROWSER=headless
```

想看浏览器操作过程，改成：
```env
BROWSER=headed
```

### Q5: AI 测试提示 API Key 错误

**解决**：
1. 检查 `.env` 文件是否存在
2. 检查密钥是否正确
3. 确认账户有余额

---

## 📝 完整命令速查表

| 你想做什么 | 输入什么命令 |
|-----------|-------------|
| 创建虚拟环境 | `python -m venv .venv` |
| 激活虚拟环境 | `.venv\Scripts\activate` |
| 安装依赖 | `pip install -r requirements.txt` |
| 安装浏览器 | `playwright install chromium` |
| 运行所有测试 | `pytest` |
| 运行特定测试 | `pytest tests/traditional/test_login.py` |
| 运行带详细输出 | `pytest -v` |
| 运行 AI 测试 | `pytest -m ai` |
| 生成报告 | `allure generate reports/allure-results -o reports/allure-report --clean` |
| 查看报告 | `allure open reports/allure-report` |

---

## 🎯 下一步学习路线

```
📚 学习路线建议：

Week 1: 基础巩固
├── 练习写 5-10 个传统测试用例
├── 熟悉 BasePage 的各种方法
└── 学会查看 Allure 报告

Week 2: 进阶提升
├── 学习页面对象模式 (POM)
├── 尝试 SmartLocator 智能定位
└── 学习自我修复机制

Week 3: AI 能力
├── 配置 AI 环境
├── 写 AI 驱动测试
└── 混合模式测试实践

Week 4: 实战项目
├── 为自己的项目写测试
├── 配置 CI/CD 自动运行
└── 优化测试套件性能
```

---

## 💡 小提示

1. **先跑通传统测试，再尝试 AI 测试**
2. **多看示例代码**，在 `tests/` 文件夹里有很多例子
3. **善用文档**，框架设计文档在 `docs/` 文件夹
4. **有问题先 Google**，90% 的问题别人都遇到过

---

**恭喜你！** 如果按照这个指南操作到这里，你已经成功运行了第一个自动化测试！🎉

接下来就可以开始探索更多高级功能了，加油！💪
