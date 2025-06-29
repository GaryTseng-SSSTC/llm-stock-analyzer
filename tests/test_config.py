import os
from unittest.mock import mock_open, patch

import pytest
import yaml

from app.configs import config


def test_get_config_loads_yaml(monkeypatch):
    # Prepare a minimal valid config dict
    config_dict = {
        "app": {
            "host": "127.0.0.1",
            "name": "TestApp",
            "description": "desc",
            "version": "0.1",
            "port": 8000,
            "log_level": "INFO",
        },
        "llm": {
            "stock_analyzer_prompt_path": "./prompt.md",
            "temperature": 0.5,
            "max_tokens": 100,
            "retry": 2,
        },
        "shioaji": {"api_key": "key", "api_secret": "secret"},
        "azure_openai": {
            "endpoint": "https://test",
            "api_version": "2024-01-01",
            "deployment": "gpt-4",
            "subscription_key": "sk-xxx",
        },
    }
    yaml_str = yaml.dump(config_dict)
    # Patch open to return this YAML
    with patch("builtins.open", mock_open(read_data=yaml_str)):
        # Patch os.getenv to force config path
        monkeypatch.setenv("CONFIG_PATH", "dummy.yaml")
        cfg = config.get_config()
        assert cfg.app.name == "TestApp"
        assert cfg.llm.temperature == 0.5
        assert cfg.shioaji.api_key == "key"
        assert cfg.azure_openai.endpoint == "https://test"
