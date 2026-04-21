"""Agent 工厂 - 创建不同 LLM provider 实例"""
from typing import Optional, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_ollama import ChatOllama
from config.settings import Settings, OPENAI_API_KEY, ANTHROPIC_API_KEY, OLLAMA_BASE_URL


class AgentFactory:
    """AI Agent 工厂类"""

    _instances: Dict[str, Any] = {}

    @classmethod
    def create_llm(cls, provider: str = "openai", **kwargs):
        """
        创建 LLM 实例

        Args:
            provider: LLM 提供商 (openai, anthropic, local)
            **kwargs: 额外的配置参数

        Returns:
            LLM 实例
        """
        if provider in cls._instances:
            return cls._instances[provider]

        ai_config = Settings.get_ai_config()
        provider_config = ai_config.get("providers", {}).get(provider, {})
        temperature = kwargs.get("temperature", provider_config.get("temperature", 0.1))

        llm = None

        if provider == "openai":
            llm = cls._create_openai_llm(provider_config, temperature, **kwargs)
        elif provider == "anthropic":
            llm = cls._create_anthropic_llm(provider_config, temperature, **kwargs)
        elif provider == "local":
            llm = cls._create_local_llm(provider_config, temperature, **kwargs)
        else:
            raise ValueError(f"不支持的 LLM 提供商: {provider}")

        cls._instances[provider] = llm
        return llm

    @classmethod
    def _create_openai_llm(cls, config: dict, temperature: float, **kwargs):
        """创建 OpenAI LLM"""
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY 未在环境变量中设置")

        model = kwargs.get("model", config.get("model", "gpt-4o"))
        return ChatOpenAI(
            model=model,
            temperature=temperature,
            api_key=OPENAI_API_KEY,
            **kwargs
        )

    @classmethod
    def _create_anthropic_llm(cls, config: dict, temperature: float, **kwargs):
        """创建 Anthropic LLM"""
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY 未在环境变量中设置")

        model = kwargs.get("model", config.get("model", "claude-3-5-sonnet"))
        return ChatAnthropic(
            model=model,
            temperature=temperature,
            api_key=ANTHROPIC_API_KEY,
            **kwargs
        )

    @classmethod
    def _create_local_llm(cls, config: dict, temperature: float, **kwargs):
        """创建本地 Ollama LLM"""
        model = kwargs.get("model", config.get("model", "llama3.2"))
        base_url = kwargs.get("base_url", config.get("base_url", OLLAMA_BASE_URL))
        return ChatOllama(
            model=model,
            temperature=temperature,
            base_url=base_url,
            **kwargs
        )

    @classmethod
    def get_default_provider(cls) -> str:
        """获取默认 LLM 提供商"""
        ai_config = Settings.get_ai_config()
        return ai_config.get("default_provider", "openai")

    @classmethod
    def is_vision_enabled(cls) -> bool:
        """检查是否启用了视觉能力"""
        ai_config = Settings.get_ai_config()
        return ai_config.get("vision_enabled", True)

    @classmethod
    def get_max_iterations(cls) -> int:
        """获取最大迭代次数"""
        ai_config = Settings.get_ai_config()
        return ai_config.get("max_iterations", 50)

    @classmethod
    def clear_cache(cls):
        """清除 LLM 实例缓存"""
        cls._instances.clear()


class AgentConfig:
    """Agent 配置类"""

    def __init__(
        self,
        provider: str = None,
        model: str = None,
        temperature: float = 0.1,
        use_vision: bool = None,
        max_iterations: int = None,
        headless: bool = False,
        **kwargs
    ):
        self.provider = provider or AgentFactory.get_default_provider()
        self.model = model
        self.temperature = temperature
        self.use_vision = use_vision if use_vision is not None else AgentFactory.is_vision_enabled()
        self.max_iterations = max_iterations or AgentFactory.get_max_iterations()
        self.headless = headless
        self.extra_kwargs = kwargs

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "provider": self.provider,
            "model": self.model,
            "temperature": self.temperature,
            "use_vision": self.use_vision,
            "max_iterations": self.max_iterations,
            "headless": self.headless,
            **self.extra_kwargs
        }
