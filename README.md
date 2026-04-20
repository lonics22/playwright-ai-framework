# Playwright AI Framework

🎭 AI 增强的自动化测试框架 - 基于 Python + Playwright + Allure + browser-use

## 🌟 核心特性

- **双模式执行**：传统脚本测试 + AI Agent 自然语言测试
- **智能元素定位**：AI 辅助元素识别与自我修复
- **多 LLM 支持**：OpenAI、Anthropic Claude、本地 Ollama
- **完整证据链**：截图 + Trace + 视频 + AI 步骤历史
- **分层测试策略**：Smoke / Regression / AI Explore

## 📁 项目结构

```
playwright-ai-framework/
├── docs/                      # 设计文档
│   ├── framework-design.md
│   ├── framework-best-practice.html
│   └── framework-overview.html
├── config/                    # 配置管理
├── core/                      # 框架核心
│   ├── playwright/           # Playwright 封装
│   ├── ai/                   # AI 增强模块
│   ├── elements/             # 智能元素定位
│   ├── reporting/            # Allure 报告
│   └── security/             # 安全与合规
├── pages/                     # 页面对象模型
├── flows/                     # 业务流程
├── tests/                     # 测试用例
│   ├── e2e/smoke/            # 冒烟测试
│   ├── e2e/regression/       # 回归测试
│   ├── ai_driven/            # AI 驱动测试
│   └── hybrid/               # 混合测试
├── data/                      # 测试数据
├── scripts/                   # 执行脚本
└── reports/                   # 测试报告
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
pip install -e .
playwright install chromium

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，填入必要的配置
```

### 运行测试

```bash
# 运行冒烟测试
pytest tests/e2e/smoke/ -v -m smoke

# 运行回归测试
pytest tests/e2e/regression/ -v -m regression

# 运行 AI 驱动测试（需要配置 LLM API Key）
pytest tests/ai_driven/ -v -m ai

# 生成 Allure 报告
allure generate reports/allure-results -o reports/allure-report --clean
allure open reports/allure-report
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
```

## 📖 设计文档

- [框架设计文档 (MD)](docs/framework_design_best_practice.md)
- [框架概览 (HTML)](docs/framework-overview.html) - 浏览器打开查看
- [最佳实践 (HTML)](docs/framework-best-practice.html) - 浏览器打开查看

## 🔧 技术栈

- **测试框架**：pytest + Playwright
- **AI 能力**：browser-use + LangChain
- **LLM 支持**：OpenAI GPT-4o / Claude 3.5 Sonnet / Ollama 本地模型
- **报告**：Allure Report
- **配置**：YAML + python-dotenv

## 📝 License

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**文档维护者**: QA Team  
**最后更新**: 2026-04-20
