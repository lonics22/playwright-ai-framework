"""Browser-Use 适配器 - 集成 AI Agent 能力"""
import os
from typing import Optional, Dict, Any
from browser_use import Agent, Browser as BrowserUseBrowser
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from config.settings import (
    Settings, OPENAI_API_KEY, ANTHROPIC_API_KEY, OLLAMA_BASE_URL,
    KIMI_API_KEY, DEEPSEEK_API_KEY
)


class AIAgentAdapter:
    """Browser-Use 适配器 - 集成 AI Agent 能力"""

    def __init__(
        self,
        llm_provider: str = "openai",
        headless: bool = False,
        use_vision: bool = True,
        max_iterations: int = 50,
    ):
        self.llm_provider = llm_provider
        self.headless = headless
        self.use_vision = use_vision
        self.max_iterations = max_iterations

        self.browser = BrowserUseBrowser(headless=headless)
        self.llm = self._create_llm(llm_provider)
        self._agent: Optional[Agent] = None
        self._last_result: Optional[Any] = None

    def _create_llm(self, provider: str):
        """支持多 LLM 后端"""
        ai_config = Settings.get_ai_config()
        provider_config = ai_config.get("providers", {}).get(provider, {})
        temperature = provider_config.get("temperature", 0.1)

        if provider == "openai":
            if not OPENAI_API_KEY:
                raise ValueError("OPENAI_API_KEY not set in environment variables")
            model = provider_config.get("model", "gpt-4o")
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                api_key=OPENAI_API_KEY,
            )

        elif provider == "anthropic":
            if not ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY not set in environment variables")
            model = provider_config.get("model", "claude-3-5-sonnet")
            return ChatAnthropic(
                model=model,
                temperature=temperature,
                api_key=ANTHROPIC_API_KEY,
            )

        elif provider == "kimi":
            """Moonshot AI (Kimi) - 国内大模型"""
            if not KIMI_API_KEY:
                raise ValueError("KIMI_API_KEY not set in environment variables")
            model = provider_config.get("model", "moonshot-v1-8k")
            base_url = provider_config.get("base_url", "https://api.moonshot.cn/v1")
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                api_key=KIMI_API_KEY,
                base_url=base_url,
            )

        elif provider == "deepseek":
            """DeepSeek - 国内大模型"""
            if not DEEPSEEK_API_KEY:
                raise ValueError("DEEPSEEK_API_KEY not set in environment variables")
            model = provider_config.get("model", "deepseek-chat")
            base_url = provider_config.get("base_url", "https://api.deepseek.com/v1")
            return ChatOpenAI(
                model=model,
                temperature=temperature,
                api_key=DEEPSEEK_API_KEY,
                base_url=base_url,
            )

        elif provider == "local":
            model = provider_config.get("model", "llama3.2")
            base_url = provider_config.get("base_url", OLLAMA_BASE_URL)
            return ChatOllama(
                model=model,
                temperature=temperature,
                base_url=base_url,
            )

        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    async def execute_task(self, task: str, context: Dict[str, Any] = None) -> Any:
        """
        使用自然语言执行测试任务

        Args:
            task: 自然语言描述的任务
            context: 额外的上下文信息

        Returns:
            Agent 执行结果
        """
        # 构建完整任务描述
        full_task = task
        if context:
            full_task += f"\n\n上下文信息: {context}"

        self._agent = Agent(
            task=full_task,
            llm=self.llm,
            browser=self.browser,
            use_vision=self.use_vision,
        )

        self._last_result = await self._agent.run()
        return self._last_result

    async def execute_steps(self, steps: list) -> Any:
        """
        执行多个步骤的任务

        Args:
            steps: 步骤列表，每个步骤是一个字符串描述

        Returns:
            Agent 执行结果
        """
        task = "完成以下任务步骤:\n" + "\n".join(
            f"{i+1}. {step}" for i, step in enumerate(steps)
        )
        return await self.execute_task(task)

    def get_last_result(self) -> Optional[Any]:
        """获取最后一次执行结果"""
        return self._last_result

    def get_execution_log(self) -> str:
        """获取执行日志"""
        if self._agent and hasattr(self._agent, "history"):
            return str(self._agent.history)
        return ""

    async def close(self):
        """关闭浏览器"""
        await self.browser.close()

    @property
    def current_url(self) -> str:
        """获取当前页面 URL"""
        if self.browser and hasattr(self.browser, "page"):
            return self.browser.page.url
        return ""

    async def navigate_to(self, url: str):
        """导航到指定 URL"""
        if self.browser and hasattr(self.browser, "page"):
            await self.browser.page.goto(url)

    async def screenshot(self, path: str = None) -> bytes:
        """截图"""
        if self.browser and hasattr(self.browser, "page"):
            return await self.browser.page.screenshot(path=path)
        return b""


class AIAgentResult:
    """AI Agent 执行结果包装器"""

    def __init__(self, raw_result: Any):
        self.raw_result = raw_result
        self._parse_result()

    def _parse_result(self):
        """解析原始结果"""
        # 根据 browser-use 的实际返回结构解析
        self.success = getattr(self.raw_result, "success", False)
        self.steps = getattr(self.raw_result, "steps", [])
        self.duration = getattr(self.raw_result, "duration", 0)
        self.errors = getattr(self.raw_result, "errors", [])

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "success": self.success,
            "steps": self.steps,
            "duration": self.duration,
            "errors": self.errors,
        }

    def __bool__(self):
        """布尔值判断"""
        return self.success

    def __repr__(self):
        return f"AIAgentResult(success={self.success}, duration={self.duration}s)"
