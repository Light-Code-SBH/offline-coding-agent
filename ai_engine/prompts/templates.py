"""
AI Engine - Prompt Templates
=============================
Contains prompt templates for different AI tasks.

Owner: Member 1 (AI/ML Lead)
"""

# ============================================================
# DEBUG PROMPT — Find errors in code
# ============================================================
DEBUG_PROMPT = """You are an expert code debugger. Analyze the following {language} code and identify all errors, bugs, and potential issues.

For each issue found, provide:
1. Line number
2. Error type (syntax/runtime/logic/style)
3. Description of the issue
4. Suggested fix

Code:
```{language}
{code}
```

Respond in this exact format:
ERROR: Line <number> | Type: <type> | <description> | Fix: <suggestion>

If no errors are found, respond with: NO_ERRORS_FOUND
"""

# ============================================================
# EXPLAIN PROMPT — Line-by-line code explanation
# ============================================================
EXPLAIN_PROMPT = """You are a coding instructor. Explain the following {language} code line by line in simple, beginner-friendly language.

Code:
```{language}
{code}
```

For each meaningful line or block, explain:
- What it does
- Why it's written this way
- Any important concepts it uses

Format: LINE <start>-<end>: <explanation>
"""

# ============================================================
# FIX PROMPT — Suggest code fix
# ============================================================
FIX_PROMPT = """You are an expert programmer. The following {language} code has an error:

Error: {error_message}
Location: Line {line_number}

Code:
```{language}
{code}
```

Provide the corrected version of the code and explain what was wrong and how you fixed it.

FIXED CODE:
```{language}
<corrected code here>
```

EXPLANATION: <what was wrong and how it was fixed>
"""


def format_prompt(template: str, **kwargs) -> str:
    """
    Format a prompt template with the given variables.
    
    Args:
        template: One of the prompt templates above
        **kwargs: Variables to fill in the template
        
    Returns:
        Formatted prompt string
    """
    return template.format(**kwargs)
