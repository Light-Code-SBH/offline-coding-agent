"""
Backend API - Main Server
==========================
FastAPI application that serves as the bridge between Frontend and Backend modules.

Owner: Member 4 (Backend Lead)
"""

import sys
import os
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List

# Make project root importable so ai_engine / code_analysis packages resolve
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from ai_engine.model_manager import ModelManager
from ai_engine.inference.pipeline import InferencePipeline
from code_analysis.error_detector import ErrorDetector

app = FastAPI(
    title="AI Offline Coding Assistant API",
    description="Backend API for offline code analysis, debugging, and explanation",
    version="0.1.0"
)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)


# ============================================================
# Request/Response Models
# ============================================================

class AnalysisOptions(BaseModel):
    include_explanation: bool = True
    include_fixes: bool = True
    max_suggestions: int = 3


class AnalysisRequest(BaseModel):
    code: str
    language: str
    action: str
    options: Optional[AnalysisOptions] = AnalysisOptions()


class ErrorDetail(BaseModel):
    line: int
    column: int = 0
    type: str
    severity: str
    message: str
    suggestion: Optional[str] = None
    fixed_code: Optional[str] = None


class ExplanationDetail(BaseModel):
    line_start: int
    line_end: int
    code: str = ""
    explanation: str


class AnalysisSummary(BaseModel):
    total_errors: int
    total_warnings: int
    overall_assessment: str


class AnalysisResponse(BaseModel):
    status: str
    language: str
    errors: List[ErrorDetail] = []
    explanations: List[ExplanationDetail] = []
    summary: Optional[AnalysisSummary] = None


# ============================================================
# Global instances (loaded on startup)
# ============================================================

model_manager = ModelManager()
inference = InferencePipeline(model_manager)
detector = ErrorDetector()

DEFAULT_MODEL = "deepseek-coder-6.7b"


@app.on_event("startup")
def startup_event():
    logger.info("Loading default model on startup...")
    success = model_manager.load_model(DEFAULT_MODEL)
    if success:
        logger.info(f"Model '{DEFAULT_MODEL}' loaded successfully.")
    else:
        logger.warning(f"Failed to load model '{DEFAULT_MODEL}'. /analyze will fail until a model is loaded.")


# ============================================================
# API Endpoints
# ============================================================

@app.get("/")
def root():
    return {"status": "running", "service": "AI Offline Coding Assistant"}


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_manager.loaded_model is not None,
        "current_model": model_manager.model_name,
        "supported_languages": list(detector.parsers.keys()),
    }


@app.post("/analyze", response_model=AnalysisResponse)
def analyze_code(request: AnalysisRequest):
    if request.language not in detector.parsers:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {request.language}. Supported: {list(detector.parsers.keys())}"
        )

    # Step 1: Static analysis (tree-sitter / ast based)
    static_errors = detector.detect(request.code, request.language)

    error_details = [
        ErrorDetail(
            line=e.line,
            column=getattr(e, "column", 0),
            type=e.error_type,
            severity=getattr(e, "severity", "error"),
            message=e.message,
            suggestion=getattr(e, "suggestion", None),
            fixed_code=getattr(e, "fixed_code", None),
        )
        for e in static_errors
    ]

    # Step 2: AI-enhanced analysis
    ai_result = {}
    if model_manager.loaded_model is not None:
        try:
            ai_result = inference.debug_code(request.code, request.language)
            for ai_err in ai_result.get("errors", []):
                error_details.append(ErrorDetail(
                    line=ai_err.get("line", 0),
                    type=ai_err.get("type", "logic"),
                    severity="warning",
                    message=ai_err.get("message", ""),
                    suggestion=ai_err.get("suggestion"),
                ))
        except Exception as e:
            logger.error(f"AI debug_code failed: {e}")

    # Step 3: Explanations (optional)
    explanation_details = []
    if request.options.include_explanation and model_manager.loaded_model is not None:
        try:
            exp_result = inference.explain_code(request.code, request.language)
            for exp in exp_result.get("explanations", []):
                explanation_details.append(ExplanationDetail(
                    line_start=exp.get("line_start", 0),
                    line_end=exp.get("line_end", 0),
                    explanation=exp.get("explanation", ""),
                ))
        except Exception as e:
            logger.error(f"AI explain_code failed: {e}")

    return AnalysisResponse(
        status="success",
        language=request.language,
        errors=error_details,
        explanations=explanation_details,
        summary=AnalysisSummary(
            total_errors=len([e for e in error_details if e.severity == "error"]),
            total_warnings=len([e for e in error_details if e.severity == "warning"]),
            overall_assessment="Analysis complete"
        )
    )


@app.post("/analyze/static", response_model=AnalysisResponse)
def analyze_static_code(request: AnalysisRequest):
    """Return fast, deterministic diagnostics without waking the local LLM.

    The editor calls this endpoint while the user is typing.  Keeping it
    separate from ``/analyze`` means syntax feedback is available even when a
    model is still loading or a longer AI analysis is in progress.
    """
    if request.language not in detector.parsers:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language: {request.language}. Supported: {list(detector.parsers.keys())}"
        )

    static_errors = detector.detect(request.code, request.language)
    error_details = [
        ErrorDetail(
            line=e.line,
            column=getattr(e, "column", 0),
            type=e.error_type,
            severity=getattr(e, "severity", "error"),
            message=e.message,
            suggestion=getattr(e, "suggestion", None),
            fixed_code=getattr(e, "fixed_code", None),
        )
        for e in static_errors
    ]

    return AnalysisResponse(
        status="success",
        language=request.language,
        errors=error_details,
        summary=AnalysisSummary(
            total_errors=len([e for e in error_details if e.severity == "error"]),
            total_warnings=len([e for e in error_details if e.severity == "warning"]),
            overall_assessment="Live static analysis complete",
        ),
    )


@app.post("/explain", response_model=AnalysisResponse)
def explain_code(request: AnalysisRequest):
    if model_manager.loaded_model is None:
        raise HTTPException(status_code=503, detail="No model loaded")

    result = inference.explain_code(request.code, request.language)
    explanation_details = [
        ExplanationDetail(
            line_start=exp.get("line_start", 0),
            line_end=exp.get("line_end", 0),
            explanation=exp.get("explanation", ""),
        )
        for exp in result.get("explanations", [])
    ]

    return AnalysisResponse(
        status="success",
        language=request.language,
        explanations=explanation_details,
    )


@app.post("/fix", response_model=AnalysisResponse)
def suggest_fix(request: AnalysisRequest):
    if model_manager.loaded_model is None:
        raise HTTPException(status_code=503, detail="No model loaded")

    static_errors = detector.detect(request.code, request.language)
    if not static_errors:
        return AnalysisResponse(status="success", language=request.language, errors=[])

    first_error = static_errors[0]
    result = inference.suggest_fix(
        request.code,
        {"message": first_error.message, "line": first_error.line},
        request.language
    )

    return AnalysisResponse(
        status="success",
        language=request.language,
        errors=[ErrorDetail(
            line=first_error.line,
            type=first_error.error_type,
            severity="error",
            message=first_error.message,
            fixed_code=result.get("fixed_code"),
            suggestion=result.get("explanation"),
        )],
    )


@app.get("/models")
def list_models():
    return {
        "available": model_manager.list_available_models(),
        "current": model_manager.model_name,
    }


@app.post("/models/{model_name}/load")
def load_model(model_name: str):
    success = model_manager.load_model(model_name)
    if not success:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {model_name}")
    return {"status": "loaded", "model": model_name}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
