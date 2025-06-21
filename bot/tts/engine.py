import tempfile
import os
from TTS.api import TTS
import torch
from config.settings import ModelConfig


class TTSEngine:
    def __init__(self):
        self.config = ModelConfig()
        self.device = self._get_device()
        self.tts = None
        self._init_model()

    def _get_device(self) -> str:
        """Determine the best device to use"""
        config_device = self.config.get_device()
        if config_device == "auto":
            return "cuda" if torch.cuda.is_available() else "cpu"
        return config_device

    def _init_model(self):
        """Initialize the TTS model"""
        model_name = self.config.get_default_model()
        self.tts = TTS(model_name).to(self.device)

    def synthesize(self, text: str, model_name: str = None) -> str:
        """Synthesize speech from text and return path to audio file"""
        if model_name and model_name != self.config.get_default_model():
            # Switch model if different from current
            new_model = self.config.get_model_by_name(model_name)
            self.tts = TTS(new_model).to(self.device)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
            output_path = temp_file.name

        self.tts.tts_to_file(text=text, file_path=output_path)
        return output_path

    def cleanup_file(self, file_path: str):
        """Clean up temporary audio file"""
        if os.path.exists(file_path):
            os.remove(file_path)
