# Contributing to AI-Powered Offline Coding Assistant

Thank you for contributing! Here's how to get started.

## 🌿 Branch Naming Convention

Use this format for all branches:

```
feature/<your-name>/<short-description>
```

**Examples:**
- `feature/rahul/model-loader`
- `feature/priya/error-detection`
- `feature/amit/desktop-ui`
- `feature/sneha/api-routes`
- `feature/vikram/unit-tests`

## 🔄 Git Workflow

### Starting New Work

```bash
# Always start from the dev branch
git checkout dev
git pull origin dev

# Create your feature branch
git checkout -b feature/your-name/task-name
```

### Making Changes

```bash
# Stage your changes
git add .

# Write meaningful commit messages
git commit -m "feat: add Python AST parser with error detection"

# Push to remote
git push origin feature/your-name/task-name
```

### Creating a Pull Request

1. Go to GitHub → your branch → **"New Pull Request"**
2. Set base branch to `dev` (NOT `main`)
3. Fill in the PR template
4. Request review from at least 1 teammate
5. Wait for approval before merging

## 📝 Commit Message Format

Use this format: `<type>: <short description>`

| Type     | When to Use                        |
|----------|------------------------------------|
| `feat`   | Adding a new feature               |
| `fix`    | Fixing a bug                       |
| `docs`   | Documentation changes              |
| `test`   | Adding or updating tests           |
| `refactor` | Code changes that don't add features or fix bugs |
| `style`  | Formatting, missing semicolons, etc. |
| `chore`  | Build scripts, configs, etc.       |

**Examples:**
```
feat: add tree-sitter parser for Java
fix: resolve model loading crash on low-memory systems
docs: update API endpoint documentation
test: add unit tests for error detector
```

## 📁 Where to Put Your Code

| Member | Directory | Description |
|--------|-----------|-------------|
| Member 1 (AI/ML) | `ai_engine/` | Models, inference, prompts |
| Member 2 (Code Analysis) | `code_analysis/` | Parsers, detectors, explainers |
| Member 3 (Frontend) | `frontend/` | UI components, editor, styles |
| Member 4 (Backend) | `backend/` | API routes, services |
| Member 5 (Testing) | `tests/`, `docs/` | Tests, documentation |
| Shared | `contracts/` | API schemas everyone uses |

## ⚠️ Important Rules

1. **Never push directly to `main` or `dev`** — always use Pull Requests
2. **Pull from `dev` daily** to stay up-to-date
3. **Don't commit model files** (.bin, .gguf) — they are too large for Git
4. **Write tests** for any new feature you add
5. **Update the contracts/** folder if you change any API interface

## 🧪 Before Submitting a PR

- [ ] Code runs without errors
- [ ] Tests pass: `pytest` (backend) or `npm test` (frontend)
- [ ] No hardcoded paths or secrets
- [ ] Commit messages follow the format
- [ ] Updated relevant documentation
