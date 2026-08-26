"""
AI Engine - Model Manager
=========================
Handles loading, managing, and configuring AI models for offline inference.

Owner: Member 1 (AI/ML Lead)
"""

import os
import logging

logger = logging.getLogger(__name__)


class ModelManager:
    """
    Manages the lifecycle of AI models.
    
    Responsibilities:
    - Load and unload models
    - Detect available hardware (CPU/GPU)
    - Select appropriate model size based on system resources
    - Handle model quantization formats (GGUF, GPTQ)
    """

    SUPPORTED_MODELS = {
        "codellama-7b": {
            "name": "CodeLlama 7B",
            "min_ram_gb": 8,
            "formats": ["gguf"],
            "description": "Good balance of speed and quality"
        },
        "deepseek-coder-1.3b": {
            "name": "DeepSeek Coder 1.3B",
            "min_ram_gb": 4,
            "formats": ["gguf"],
            "description": "Lightweight, fast, good for low-resource systems"
        },
        "starcoder2-3b": {
            "name": "StarCoder2 3B",
            "min_ram_gb": 6,
            "formats": ["gguf"],
            "description": "Strong multi-language support"
        },
    }

    def __init__(self, models_dir: str = None):
        self.models_dir = models_dir or os.path.join(os.path.dirname(__file__), "models")
        self.loaded_model = None
        self.model_name = None
        logger.info(f"ModelManager initialized. Models directory: {self.models_dir}")

    def list_available_models(self) -> list:
        """List all models available for loading."""
        # TODO: Scan models directory for downloaded model files
        # TODO: Cross-reference with SUPPORTED_MODELS
        raise NotImplementedError("Member 1: Implement model discovery")

    def load_model(self, model_name: str) -> bool:
        """
        Load a model into memory for inference.
        
        Args:
            model_name: Key from SUPPORTED_MODELS dict
            
        Returns:
            True if model loaded successfully
        """
        # TODO: Load model using llama-cpp-python or ctransformers
        # TODO: Auto-detect GPU availability and use it if possible
        # TODO: Handle out-of-memory gracefully
        raise NotImplementedError("Member 1: Implement model loading")

    def unload_model(self):
        """Unload the current model to free memory."""
        # TODO: Release model from memory
        raise NotImplementedError("Member 1: Implement model unloading")

    def get_system_info(self) -> dict:
        """
        Detect system capabilities for model selection.
        
        Returns:
            Dict with ram_gb, gpu_available, gpu_name, gpu_vram_gb
        """
        # TODO: Detect RAM, GPU, VRAM
        raise NotImplementedError("Member 1: Implement system detection")
