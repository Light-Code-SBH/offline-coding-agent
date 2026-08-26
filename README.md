# 🤖 AI-Powered Offline Coding Assistant

An AI-powered offline code debugger and explainer that analyzes code, detects errors, suggests fixes, and provides line-by-line explanations — **all without requiring an internet connection**.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-green.svg)
![Status](https://img.shields.io/badge/status-in%20development-orange.svg)

---

## 🚀 Features

- **🔍 Error Detection** — Automatically detect syntax, runtime, and logic errors
- **🔧 Fix Suggestions** — AI-powered code fix recommendations
- **📖 Line-by-Line Explanations** — Understand what every line of code does
- **🌐 Multi-Language Support** — Python, Java, C, and JavaScript
- **📴 Fully Offline** — No internet connection required
- **🔒 Privacy-First** — Your code never leaves your machine
- **⚡ Real-Time Analysis** — Instant feedback as you code

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                  Desktop App (UI)                │
│              (Electron + Monaco Editor)          │
├─────────────────────────────────────────────────┤
│                 Backend API Layer                │
│              (FastAPI + WebSocket)               │
├──────────────────────┬──────────────────────────┤
│    AI/ML Engine      │   Code Analysis Engine   │
│  (LLM Inference)     │   (Tree-sitter + AST)    │
└──────────────────────┴──────────────────────────┘
```

## 📦 Supported Languages

| Language   | Syntax Check | Error Detection | Fix Suggestions | Explanations |
|------------|:------------:|:---------------:|:---------------:|:------------:|
| Python     | ✅           | ✅              | ✅              | ✅           |
| Java       | ✅           | ✅              | ✅              | ✅           |
| C          | ✅           | ✅              | ✅              | ✅           |
| JavaScript | ✅           | ✅              | ✅              | ✅           |

## 🛠️ Tech Stack

| Component        | Technology                                    |
|------------------|-----------------------------------------------|
| Frontend         | Electron.js, React, Monaco Editor             |
| Backend API      | Python, FastAPI, WebSocket                     |
| AI Engine        | llama-cpp-python, CodeLlama / DeepSeek-Coder  |
| Code Analysis    | tree-sitter, AST parsing                      |
| Database         | SQLite (session storage)                       |
| Testing          | pytest, Jest                                  |
| Packaging        | electron-builder, PyInstaller                 |

## 📁 Project Structure

```
ai-offline-coding-assistant/
├── frontend/              # Desktop app (Electron + React)
│   ├── src/               # React components & logic
│   └── public/            # Static assets
├── backend/               # Backend API server
│   ├── api/               # API route definitions
│   └── services/          # Business logic services
├── ai_engine/             # AI/ML model management
│   ├── models/            # Model files & configs
│   ├── inference/         # Inference pipeline
│   └── prompts/           # Prompt templates
├── code_analysis/         # Code parsing & analysis
│   ├── parsers/           # Language-specific parsers
│   ├── detectors/         # Error detection modules
│   └── explainers/        # Code explanation generators
├── tests/                 # Test suites
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── test_data/         # Sample code for testing
├── docs/                  # Documentation
├── contracts/             # Shared API contracts (JSON schemas)
└── scripts/               # Build & deployment scripts
```

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_ORG/ai-offline-coding-assistant.git
cd ai-offline-coding-assistant

# 2. Set up the backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Download the AI model
cd ../ai_engine
python download_model.py

# 4. Set up the frontend
cd ../frontend
npm install

# 5. Start the application
cd ..
python scripts/start.py
```

## 🧪 Running Tests

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# All tests
python scripts/run_tests.py
```

## 👥 Team

| Member | Role | Responsibilities |
|--------|------|------------------|
| Member 1 | AI/ML Lead | Model integration, inference pipeline, prompt engineering |
| Member 2 | Code Analysis Lead | AST parsing, error detection, fix suggestions |
| Member 3 | Frontend Lead | Desktop UI, code editor, results display |
| Member 4 | Backend Lead | API design, routing, integration layer |
| Member 5 | QA & DevOps Lead | Testing, documentation, packaging |

## 🤝 Contributing

1. Create a feature branch: `git checkout -b feature/your-name/task-name`
2. Make your changes and commit: `git commit -m "Add feature description"`
3. Push to your branch: `git push origin feature/your-name/task-name`
4. Open a Pull Request for review

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
