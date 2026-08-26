"""
AI Engine - Model Manager
=========================
Handles loading, managing, and configuring AI models for offline inference.

Owner: Member 1 (AI/ML Lead)
"""

import os
import logging
import subprocess
import psutil
from llama_cpp import Llama

logger = logging.getLogger(__name__)


class ModelManager:
    """
    Manages the lifecycle of AI models.
    """

    SUPPORTED_MODELS = {
        "deepseek-coder-6.7b": {
            "name": "DeepSeek Coder 6.7B",
            "min_ram_gb": 8,
            "formats": ["gguf"],
            "description": "High-quality code analysis, primary model",
            "filename": "deepseek-coder-6.7b-instruct.Q4_K_M.gguf",
        },
        "codellama-7b": {
            "name": "CodeLlama 7B",
            "min_ram_gb": 8,
            "formats": ["gguf"],
            "description": "Good balance of speed and quality",
            "filename": "codellama-7b-instruct.Q4_K_M.gguf",
        },
        "deepseek-coder-1.3b": {
            "name": "DeepSeek Coder 1.3B",
            "min_ram_gb": 4,
            "formats": ["gguf"],
            "description": "Lightweight, fast, good for low-resource systems",
            "filename": "deepseek-coder-1.3b-instruct.Q4_K_M.gguf",
        },
        "starcoder2-3b": {
            "name": "StarCoder2 3B",
            "min_ram_gb": 6,
            "formats": ["gguf"],
            "description": "Strong multi-language support",
            "filename": "starcoder2-3b.Q4_K_M.gguf",
        },
    }

    def __init__(self, models_dir: str = None):
        self.models_dir = models_dir or os.path.join(os.path.dirname(__file__), "models")
        self.loaded_model = None
        self.model_name = None
        logger.info(f"ModelManager initialized. Models directory: {self.models_dir}")

    def list_available_models(self) -> list:
        """List all models available for loading (i.e. actually downloaded)."""
        available = []
        for key, info in self.SUPPORTED_MODELS.items():
            path = os.path.join(self.models_dir, info["filename"])
            if os.path.exists(path):
                available.append({
                    "key": key,
                    "name": info["name"],
                    "description": info["description"],
                    "path": path,
                })
        return available

    def load_model(self, model_name: str) -> bool:
        """
        Load a model into memory for inference.
        """
        if model_name not in self.SUPPORTED_MODELS:
            raise ValueError(f"Unknown model: {model_name}")

        info = self.SUPPORTED_MODELS[model_name]
        model_path = os.path.join(self.models_dir, info["filename"])

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")

        gpu_layers = self._recommended_gpu_layers()
        try:
            self.loaded_model = Llama(
                model_path=model_path,
                n_ctx=2048,
                n_threads=max(1, os.cpu_count() - 1),
                # -1 means "offload every possible layer" in llama.cpp.  The
                # 6.7B Q4 model fits comfortably on the detected 8 GB RTX 4060.
                n_gpu_layers=gpu_layers,
                verbose=False,
            )
            self.model_name = model_name
            logger.info(f"Loaded model: {info['name']} (GPU layers: {gpu_layers})")
            return True
        except Exception as e:
            # A model should remain usable if a CUDA driver or CUDA-enabled
            # binding is unavailable.  Retry on CPU instead of making the API
            # unusable, while leaving a clear log message for troubleshooting.
            if gpu_layers != 0:
                logger.warning(f"GPU model load failed ({e}); retrying on CPU.")
                try:
                    self.loaded_model = Llama(
                        model_path=model_path,
                        n_ctx=2048,
                        n_threads=max(1, os.cpu_count() - 1),
                        n_gpu_layers=0,
                        verbose=False,
                    )
                    self.model_name = model_name
                    logger.warning(f"Loaded model: {info['name']} (CPU fallback)")
                    return True
                except Exception as fallback_error:
                    logger.error(f"CPU fallback failed for model {model_name}: {fallback_error}")
            else:
                logger.error(f"Failed to load model {model_name}: {e}")

            self.loaded_model = None
            self.model_name = None
            return False

    @staticmethod
    def _available_vram_mb() -> int:
        """Return free NVIDIA VRAM, or zero when no NVIDIA GPU is available."""
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=memory.free", "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                check=True,
                timeout=5,
            )
            return int(result.stdout.strip().splitlines()[0])
        except (FileNotFoundError, subprocess.SubprocessError, ValueError, IndexError):
            return 0

    def _recommended_gpu_layers(self) -> int:
        """Choose GPU offload automatically, with an optional user override."""
        configured_layers = os.getenv("AI_ASSISTANT_GPU_LAYERS")
        if configured_layers is not None:
            try:
                return int(configured_layers)
            except ValueError:
                logger.warning("Ignoring invalid AI_ASSISTANT_GPU_LAYERS=%r", configured_layers)

        # Leave roughly 2 GB for model metadata, the 2K context KV cache, and
        # the operating system.  RTX 4060 Laptop (8 GB) uses full offload.
        return -1 if self._available_vram_mb() >= 6000 else 0

    def unload_model(self):
        """Unload the current model to free memory."""
        self.loaded_model = None
        self.model_name = None
        logger.info("Model unloaded")

    def get_system_info(self) -> dict:
        """
        Detect system capabilities for model selection.
        """
        ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 1)
        gpu_available = False
        gpu_name = None
        gpu_vram_gb = None
        try:
            import torch
            if torch.cuda.is_available():
                gpu_available = True
                gpu_name = torch.cuda.get_device_name(0)
                gpu_vram_gb = round(torch.cuda.get_device_properties(0).total_memory / (1024 ** 3), 1)
        except ImportError:
            pass

        return {
            "ram_gb": ram_gb,
            "gpu_available": gpu_available,
            "gpu_name": gpu_name,
            "gpu_vram_gb": gpu_vram_gb,
        }
