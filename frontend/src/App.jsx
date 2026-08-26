import { useEffect, useMemo, useRef, useState } from 'react';
import Editor, { DiffEditor } from '@monaco-editor/react';
import { analyzeCode, analyzeStaticCode, suggestFix } from './api';
import './App.css';

const DEFAULT_CODE = `def add(a, b):
    return a - b

result = add(1, '2')
`;

const markerSeverity = (monaco, severity) => {
  if (severity === 'warning') return monaco.MarkerSeverity.Warning;
  if (severity === 'info') return monaco.MarkerSeverity.Info;
  return monaco.MarkerSeverity.Error;
};

function App() {
  const [code, setCode] = useState(DEFAULT_CODE);
  const [language, setLanguage] = useState('python');
  const [staticResult, setStaticResult] = useState(null);
  const [deepResult, setDeepResult] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [liveStatus, setLiveStatus] = useState('Ready — type to analyze');
  const [error, setError] = useState(null);
  const [fixedCode, setFixedCode] = useState(null);
  const [showDiff, setShowDiff] = useState(false);
  const [fixLoading, setFixLoading] = useState(false);
  const [voiceStatus, setVoiceStatus] = useState('');
  const [voiceAnswer, setVoiceAnswer] = useState('');
  const [editorReady, setEditorReady] = useState(false);

  const editorRef = useRef(null);
  const monacoRef = useRef(null);
  const revisionRef = useRef(0);
  const recognitionRef = useRef(null);

  // The deep endpoint returns static findings plus AI findings, so it becomes
  // the authoritative set as soon as it is available.
  const diagnostics = useMemo(
    () => deepResult?.errors ?? staticResult?.errors ?? [],
    [deepResult, staticResult],
  );
  const displayedResult = deepResult ?? staticResult;

  useEffect(() => {
    if (!editorReady || !editorRef.current || !monacoRef.current) return;

    const model = editorRef.current.getModel();
    if (!model) return;
    const markers = diagnostics.map((diagnostic) => {
      const column = Math.max(1, diagnostic.column || 1);
      return {
        severity: markerSeverity(monacoRef.current, diagnostic.severity),
        startLineNumber: Math.max(1, diagnostic.line || 1),
        startColumn: column,
        endLineNumber: Math.max(1, diagnostic.line || 1),
        endColumn: column + 1,
        message: diagnostic.suggestion
          ? `${diagnostic.message}\n\nSuggested fix: ${diagnostic.suggestion}`
          : diagnostic.message,
      };
    });
    monacoRef.current.editor.setModelMarkers(model, 'offline-coding-assistant', markers);
  }, [diagnostics, editorReady, language]);

  useEffect(() => {
    const revision = ++revisionRef.current;
    const controller = new AbortController();
    const resetTimer = window.setTimeout(() => {
      if (revision !== revisionRef.current) return;
      setStaticResult(null);
      setDeepResult(null);
      setError(null);
      setShowDiff(false);
      setFixedCode(null);
      setLiveStatus(code.trim() ? 'Waiting for a typing pause…' : 'Ready — add code to analyze');
    }, 0);

    if (!code.trim()) {
      return () => {
        controller.abort();
        window.clearTimeout(resetTimer);
      };
    }

    const staticTimer = window.setTimeout(async () => {
      try {
        const data = await analyzeStaticCode(code, language, controller.signal);
        if (revision !== revisionRef.current) return;
        setStaticResult(data);
        setLiveStatus(data.errors.length ? 'Syntax diagnostics updated' : 'Syntax check passed');
      } catch (requestError) {
        if (requestError.name !== 'AbortError' && revision === revisionRef.current) {
          setError(`Live syntax analysis failed: ${requestError.message}`);
        }
      }
    }, 500);

    const aiTimer = window.setTimeout(async () => {
      setAiLoading(true);
      setLiveStatus('Running deeper AI analysis…');
      try {
        const data = await analyzeCode(code, language, controller.signal);
        if (revision !== revisionRef.current) return;
        setDeepResult(data);
        setLiveStatus('AI analysis updated');
      } catch (requestError) {
        if (requestError.name !== 'AbortError' && revision === revisionRef.current) {
          setError(`AI analysis failed: ${requestError.message}`);
          setLiveStatus('Static analysis remains available');
        }
      } finally {
        if (revision === revisionRef.current) setAiLoading(false);
      }
    }, 2000);

    return () => {
      controller.abort();
      window.clearTimeout(resetTimer);
      window.clearTimeout(staticTimer);
      window.clearTimeout(aiTimer);
    };
  }, [code, language]);

  const handleEditorMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
    const markers = diagnostics.map((diagnostic) => {
      const column = Math.max(1, diagnostic.column || 1);
      return {
        severity: markerSeverity(monaco, diagnostic.severity),
        startLineNumber: Math.max(1, diagnostic.line || 1),
        startColumn: column,
        endLineNumber: Math.max(1, diagnostic.line || 1),
        endColumn: column + 1,
        message: diagnostic.suggestion
          ? `${diagnostic.message}\n\nSuggested fix: ${diagnostic.suggestion}`
          : diagnostic.message,
      };
    });
    monaco.editor.setModelMarkers(editor.getModel(), 'offline-coding-assistant', markers);
    setEditorReady(true);
  };

  const handleDebug = async () => {
    const revision = ++revisionRef.current;
    setAiLoading(true);
    setError(null);
    setLiveStatus('Running AI analysis…');
    try {
      const data = await analyzeCode(code, language);
      if (revision !== revisionRef.current) return;
      setDeepResult(data);
      setLiveStatus('AI analysis updated');
    } catch (requestError) {
      if (revision === revisionRef.current) setError(requestError.message);
    } finally {
      if (revision === revisionRef.current) setAiLoading(false);
    }
  };

  const handleShowFix = async () => {
    setFixLoading(true);
    setError(null);
    try {
      const data = await suggestFix(code, language);
      const proposedFix = data.errors?.[0]?.fixed_code;
      if (!proposedFix) throw new Error('No fix is available for the current code.');
      setFixedCode(proposedFix);
      setShowDiff(true);
    } catch (requestError) {
      setError(requestError.message);
    } finally {
      setFixLoading(false);
    }
  };

  const revealLine = (line) => {
    setShowDiff(false);
    window.setTimeout(() => {
      const editor = editorRef.current;
      if (!editor) return;
      editor.revealLineInCenter(line);
      editor.setPosition({ lineNumber: line, column: 1 });
      editor.focus();
    }, 0);
  };

  const speak = (text) => {
    setVoiceAnswer(text);
    if (!window.speechSynthesis) return;
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1;
    window.speechSynthesis.speak(utterance);
  };

  const handleVoiceQuery = (transcript) => {
    const lineMatch = transcript.toLowerCase().match(/line\s+(\d+)/);
    const cursorLine = editorRef.current?.getPosition()?.lineNumber;
    const targetLine = lineMatch ? Number.parseInt(lineMatch[1], 10) : cursorLine;

    if (!displayedResult) {
      speak('I am still analyzing. Please wait for the live analysis to finish or press Debug.');
      return;
    }

    if (targetLine) revealLine(targetLine);
    const matchingError = diagnostics.find((item) => item.line === targetLine);
    const matchingExplanation = deepResult?.explanations?.find(
      (item) => targetLine >= item.line_start && targetLine <= item.line_end,
    );
    let answer;
    if (matchingError) {
      answer = `Line ${targetLine}: ${matchingError.message}`;
      if (matchingError.suggestion) answer += ` Suggested fix: ${matchingError.suggestion}`;
    } else if (matchingExplanation) {
      answer = `Line ${targetLine}: ${matchingExplanation.explanation}`;
    } else if (/explain/.test(transcript.toLowerCase()) && !deepResult) {
      answer = 'The deeper explanation is still running. The syntax check has no finding for this line.';
    } else if (targetLine) {
      answer = `I do not see a diagnostic for line ${targetLine}.`;
    } else {
      answer = 'Say a command such as: what is wrong with line 15, or explain this function with the cursor inside it.';
    }
    speak(answer);
  };

  const handleVoiceCommand = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setError('Speech recognition is unavailable in this browser. Use Chromium or Edge and allow microphone access.');
      return;
    }

    recognitionRef.current?.stop();
    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognition.onstart = () => setVoiceStatus('Listening…');
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setVoiceStatus(`Heard: “${transcript}”`);
      handleVoiceQuery(transcript);
    };
    recognition.onerror = (event) => {
      setVoiceStatus('');
      setError(`Speech recognition error: ${event.error}`);
    };
    recognition.onend = () => {
      if (recognitionRef.current === recognition) setVoiceStatus((status) => status || 'Voice command complete');
    };
    recognitionRef.current = recognition;
    recognition.start();
  };

  return (
    <div className="app">
      <header className="toolbar">
        <h1>🤖 AI Offline Coding Assistant</h1>
        <select value={language} onChange={(event) => setLanguage(event.target.value)} aria-label="Language">
          <option value="python">Python</option>
          <option value="java" disabled>Java (coming soon)</option>
          <option value="c" disabled>C (coming soon)</option>
          <option value="javascript" disabled>JavaScript (coming soon)</option>
        </select>
        <button onClick={handleDebug} disabled={aiLoading}>{aiLoading ? 'Analyzing…' : '🔍 Debug now'}</button>
        <button onClick={handleShowFix} disabled={fixLoading}>{fixLoading ? 'Fixing…' : '🔧 Show diff'}</button>
        {showDiff && <button className="secondary" onClick={() => setShowDiff(false)}>Close diff</button>}
        <button className="voice-button" onClick={handleVoiceCommand}>🎙 Ask by voice</button>
      </header>

      <div className="live-status" aria-live="polite">
        <span className={aiLoading ? 'pulse' : ''}>{liveStatus}</span>
        {voiceStatus && <span>{voiceStatus}</span>}
      </div>

      <main className="main">
        <div className="editor-pane">
          {showDiff && fixedCode ? (
            <DiffEditor
              height="100%"
              language={language}
              original={code}
              modified={fixedCode}
              theme="vs-dark"
              options={{ fontSize: 14, minimap: { enabled: false }, automaticLayout: true, readOnly: true, renderSideBySide: true }}
            />
          ) : (
            <Editor
              height="100%"
              language={language}
              value={code}
              theme="vs-dark"
              onChange={(value) => setCode(value ?? '')}
              onMount={handleEditorMount}
              options={{ fontSize: 14, minimap: { enabled: false }, automaticLayout: true, hover: { enabled: true } }}
            />
          )}
        </div>

        <aside className="results-pane">
          {error && <p className="status error">{error}</p>}
          {voiceAnswer && <section className="voice-answer"><h2>Voice assistant</h2><p>{voiceAnswer}</p></section>}
          <section>
            <h2>Diagnostics ({diagnostics.length})</h2>
            {diagnostics.length === 0 ? <p className="muted">No live diagnostics.</p> : (
              <ul>{diagnostics.map((item, index) => (
                <li key={`${item.line}-${item.message}-${index}`} className={`error-item ${item.severity}`} onClick={() => revealLine(item.line)}>
                  <strong>Line {item.line}</strong> [{item.type}]: {item.message}
                  {item.suggestion && <div className="suggestion">💡 {item.suggestion}</div>}
                </li>
              ))}</ul>
            )}
          </section>

          <section>
            <h2>AI explanation</h2>
            {deepResult?.explanations?.length ? (
              <ul>{deepResult.explanations.map((item, index) => (
                <li key={`${item.line_start}-${index}`} onClick={() => revealLine(item.line_start)}>
                  <strong>Line {item.line_start}{item.line_end !== item.line_start ? `–${item.line_end}` : ''}:</strong> {item.explanation}
                </li>
              ))}</ul>
            ) : <p className="muted">A line-by-line explanation appears after the 2-second AI analysis.</p>}
          </section>

          {displayedResult?.summary && <section><h2>Summary</h2><p>{displayedResult.summary.overall_assessment}</p></section>}
        </aside>
      </main>
    </div>
  );
}

export default App;
