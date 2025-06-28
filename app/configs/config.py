"""
Configuration management for the agent, using Pydantic models and YAML loading.
"""

import os
from functools import lru_cache

import yaml
from pydantic import SecretStr, StrictFloat, StrictInt, StrictStr
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    host: StrictStr
    name: StrictStr
    description: StrictStr
    version: StrictStr
    port: StrictInt
    log_level: StrictStr


class LLMConfig(BaseSettings):
    stock_analyzer_prompt_path: StrictStr
    temperature: StrictFloat
    max_tokens: StrictInt
    retry: StrictInt


class ShioajiConfig(BaseSettings):
    api_key: str
    api_secret: str


class AzureOpenAIConfig(BaseSettings):
    endpoint: StrictStr
    api_version: StrictStr
    deployment: StrictStr
    subscription_key: SecretStr


class Config(BaseSettings):
    app: AppConfig
    llm: LLMConfig
    shioaji: ShioajiConfig
    azure_openai: AzureOpenAIConfig


@lru_cache()
def get_config() -> Config:
    config_path = os.getenv("CONFIG_PATH", "app/configs/config.yaml")

    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    return Config(**raw_config)
