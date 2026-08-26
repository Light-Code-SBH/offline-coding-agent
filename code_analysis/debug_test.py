import sys, os
sys.path.append(os.path.abspath("."))

from ai_engine.model_manager import ModelManager
from ai_engine.inference.pipeline import InferencePipeline

mm = ModelManager()
mm.load_model("deepseek-coder-1.3b")

pipe = InferencePipeline(mm)
result = pipe.debug_code("def add(a, b):\n    return a - b\n", "python")

print("RAW OUTPUT:")
print(repr(result.get("raw", "NO RAW KEY")))
print("---")
print("PARSED ERRORS:", result["errors"])