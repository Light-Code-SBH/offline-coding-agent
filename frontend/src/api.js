const API_BASE = 'http://127.0.0.1:8000';

export async function analyzeCode(code, language, signal) {
  const response = await fetch(`${API_BASE}/analyze`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code,
      language,
      action: 'analyze_all',
      options: {
        include_explanation: true,
        include_fixes: true,
        max_suggestions: 3,
      },
    }),
    signal,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export async function suggestFix(code, language) {
  const response = await fetch(`${API_BASE}/fix`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code,
      language,
      action: 'fix',
      options: {
        include_explanation: true,
        include_fixes: true,
        max_suggestions: 3,
      },
    }),
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export async function analyzeStaticCode(code, language, signal) {
  const response = await fetch(`${API_BASE}/analyze/static`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      code,
      language,
      action: 'static',
      options: { include_explanation: false, include_fixes: true, max_suggestions: 3 },
    }),
    signal,
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}
