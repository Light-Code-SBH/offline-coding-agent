import time
import os

print("Step 1: Importing modules...")
from ai_engine.model_manager import ModelManager
from ai_engine.inference.pipeline import InferencePipeline
print("Step 1 done.")

print("Step 2: Creating ModelManager...")
mm = ModelManager()
print(f"Step 2 done. CPU count detected: {os.cpu_count()}")

print("Step 3: Loading model...")
start = time.time()
success = mm.load_model("deepseek-coder-6.7b")
print(f"Step 3 done in {time.time() - start:.1f}s. Success: {success}")

print("Step 4: Running debug_code through pipeline...")
pipe = InferencePipeline(mm)
start = time.time()
result = pipe.debug_code("def broken(:\n    return 1\n", "python")
print(f"Done in {time.time() - start:.1f}s")
print("RAW OUTPUT:")
print(repr(result.get("raw", "NO RAW KEY")))
print("PARSED ERRORS:", result["errors"])