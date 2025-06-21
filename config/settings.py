import yaml
import os
from typing import Dict, Any


class ModelConfig:
    def __init__(self, config_path: str = "config/models.yaml"):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")

        with open(self.config_path, "r") as file:
            return dict(yaml.safe_load(file))

    def get_default_model(self) -> str:
        """Get the default TTS model"""
        return str(self._config["models"]["default"])

    def get_available_models(self) -> Dict[str, str]:
        """Get all available TTS models"""
        return dict(self._config["models"]["available"])

    def get_model_by_name(self, name: str) -> str:
        """Get model path by name"""
        available = self.get_available_models()
        if name not in available:
            raise ValueError(
                f"Model '{name}' not found. Available: {list(available.keys())}"
            )
        return available[name]

    def get_settings(self) -> Dict[str, Any]:
        """Get TTS settings"""
        return dict(self._config["settings"])

    def get_device(self) -> str:
        """Get configured device"""
        return str(self._config["settings"]["device"])
