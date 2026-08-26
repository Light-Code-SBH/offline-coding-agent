"""
AI Engine - Inference Pipeline
==============================
Handles sending prompts to the loaded model and processing responses.

Owner: Member 1 (AI/ML Lead)
"""

import logging
import re
from typing import Optional

from ai_engine.prompts.templates import DEBUG_PROMPT, EXPLAIN_PROMPT, FIX_PROMPT, format_prompt

logger = logging.getLogger(__name__)


class InferencePipeline:
    """
    Manages the inference process — sending prompts to the model and
    parsing structured responses.
    """

    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.default_params = {
            "max_tokens": 1024,
            "temperature": 0.1,
            "top_p": 0.95,
            "stop": ["```", "###", "\n\n\n"],
        }

    def generate(self, prompt: str, params: Optional[dict] = None) -> str:
        """
        Generate a response from the model.
        """
        if self.model_manager.loaded_model is None:
            raise RuntimeError("No model loaded. Call model_manager.load_model() first.")

        gen_params = {**self.default_params, **(params or {})}

        wrapped_prompt = f"### Instruction:\n{prompt}\n### Response:\n"

        response = self.model_manager.loaded_model(
            wrapped_prompt,
            max_tokens=gen_params["max_tokens"],
            temperature=gen_params["temperature"],
            top_p=gen_params["top_p"],
            stop=gen_params["stop"],
        )
        return response["choices"][0]["text"].strip()

    def debug_code(self, code: str, language: str) -> dict:
        """
        Analyze code for bugs and errors using the AI model.
        """
        prompt = format_prompt(DEBUG_PROMPT, language=language, code=code)
        raw = self.generate(prompt)

        if "NO_ERRORS_FOUND" in raw:
            return {"errors": []}

        errors = []
        pattern = r"ERROR:\s*Line\s*(\d+)\s*\|\s*Type:\s*(\w+)\s*\|\s*(.*?)\s*\|\s*Fix:\s*(.*)"
        for line in raw.strip().split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                errors.append({
                    "line": int(match.group(1)),
                    "type": match.group(2).strip().lower(),
                    "message": match.group(3).strip(),
                    "suggestion": match.group(4).strip(),
                })
        return {"errors": errors, "raw": raw}

    def explain_code(self, code: str, language: str) -> dict:
        """
        Generate line-by-line explanation of code.
        """
        prompt = format_prompt(EXPLAIN_PROMPT, language=language, code=code)
        raw = self.generate(prompt, params={
            "max_tokens": 512,
            "stop": ["```", "###", "\n\n\n", "Line 1:"],
        })

        explanations = []
        seen = set()
        pattern = r"LINE\s*(\d+)(?:-(\d+))?:\s*(.*)"
        for line in raw.strip().split("\n"):
            match = re.match(pattern, line.strip())
            if match:
                start = int(match.group(1))
                end = int(match.group(2)) if match.group(2) else start
                key = (start, end)
                if key in seen:
                    continue
                seen.add(key)
                explanations.append({
                    "line_start": start,
                    "line_end": end,
                    "explanation": match.group(3).strip(),
                })
        return {"explanations": explanations, "raw": raw}

    def suggest_fix(self, code: str, error_info: dict, language: str) -> dict:
        """
        Suggest a fix for a detected error.
        """
        prompt = format_prompt(
            FIX_PROMPT,
            language=language,
            code=code,
            error_message=error_info.get("message", "Unknown error"),
            line_number=error_info.get("line", 0),
        )
        raw = self.generate(prompt, params={"max_tokens": 1024})

        fixed_code = ""
        explanation = ""

        code_match = re.search(r"FIXED CODE:\s*```(?:\w+)?\s*(.*?)```", raw, re.DOTALL)
        if code_match:
            fixed_code = code_match.group(1).strip()

        expl_match = re.search(r"EXPLANATION:\s*(.*)", raw, re.DOTALL)
        if expl_match:
            explanation = expl_match.group(1).strip()

        return {"fixed_code": fixed_code, "explanation": explanation, "raw": raw}