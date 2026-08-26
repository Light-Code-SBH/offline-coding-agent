"""
Download Model Script
=====================
Downloads the recommended AI model for offline use.

Owner: Member 1 (AI/ML Lead)

Usage:
    python ai_engine/download_model.py
    python ai_engine/download_model.py --model deepseek-coder-1.3b
"""

import os
import argparse

MODELS = {
    "deepseek-coder-1.3b": {
        "url": "https://huggingface.co/TheBloke/deepseek-coder-1.3b-instruct-GGUF",
        "filename": "deepseek-coder-1.3b-instruct.Q4_K_M.gguf",
        "size_gb": 0.8,
        "description": "Lightweight model, works on most machines (4GB+ RAM)"
    },
    "codellama-7b": {
        "url": "https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF",
        "filename": "codellama-7b-instruct.Q4_K_M.gguf",
        "size_gb": 4.1,
        "description": "Higher quality, needs 8GB+ RAM"
    },
}

DEFAULT_MODEL = "deepseek-coder-1.3b"


def download_model(model_name: str):
    """Download a model from HuggingFace."""
    if model_name not in MODELS:
        print(f"Unknown model: {model_name}")
        print(f"Available models: {list(MODELS.keys())}")
        return

    model_info = MODELS[model_name]
    print(f"Downloading {model_name} ({model_info['size_gb']} GB)...")
    print(f"Description: {model_info['description']}")
    print(f"URL: {model_info['url']}")
    
    # TODO (Member 1): Implement actual download using huggingface_hub
    # from huggingface_hub import hf_hub_download
    # hf_hub_download(repo_id=..., filename=..., local_dir=models_dir)
    
    print("\n⚠️  Download not yet implemented. Member 1: implement this script.")
    print(f"Manual download: Visit {model_info['url']}")
    print(f"Save the file as: ai_engine/models/{model_info['filename']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download AI models for offline use")
    parser.add_argument("--model", default=DEFAULT_MODEL, choices=list(MODELS.keys()),
                       help=f"Model to download (default: {DEFAULT_MODEL})")
    args = parser.parse_args()
    download_model(args.model)
