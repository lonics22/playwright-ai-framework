"""全局配置管理"""
import os
import yaml
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Settings:
    """框架全局配置类"""

    # 项目根目录
    BASE_DIR = Path(__file__).parent.parent

    # 配置目录
    CONFIG_DIR = BASE_DIR / "config"

    # 报告目录
    REPORTS_DIR = BASE_DIR / "reports"

    # 测试数据目录
    FIXTURES_DIR = BASE_DIR / "fixtures"

    @classmethod
    def load_yaml(cls, filename: str) -> dict:
        """加载 YAML 配置文件"""
        filepath = cls.CONFIG_DIR / filename
        if filepath.exists():
            with open(filepath, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    @classmethod
    def get_env_config(cls, env: str = None) -> dict:
        """获取环境配置"""
        env = env or os.getenv("TEST_ENV", "default")
        config = cls.load_yaml("env_config.yaml")
        default_config = config.get("default", {})
        env_config = config.get(env, {})
        # 合并配置，环境特定配置覆盖默认配置
        return {**default_config, **env_config}

    @classmethod
    def get_browser_config(cls) -> dict:
        """获取浏览器配置"""
        return cls.load_yaml("browser_config.yaml")

    @classmethod
    def get_ai_config(cls) -> dict:
        """获取 AI 配置"""
        config = cls.load_yaml("env_config.yaml")
        return config.get("ai", {})


# API Keys (从环境变量读取)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# 国内大模型 API Keys
KIMI_API_KEY = os.getenv("KIMI_API_KEY")  # Moonshot AI (Kimi)
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # DeepSeek

# 测试环境
TEST_ENV = os.getenv("TEST_ENV", "default")

# Allure 配置
ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", "reports/allure-results")
ALLURE_REPORT_DIR = os.getenv("ALLURE_REPORT_DIR", "reports/allure-report")

# 并发配置
PARALLEL_WORKERS = int(os.getenv("PARALLEL_WORKERS", "4"))
