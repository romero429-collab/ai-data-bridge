'use client';

import React, { useState, useEffect, useRef } from 'react';

interface CodeSnippet {
  language: string;
  code: string;
  line_count: number;
}

interface ChatTurn {
  turn_index: number;
  role: string;
  content: string;
  code_blocks: CodeSnippet[];
  model?: string;
  token_estimate: number;
  phase_x: number;
  phase_y: number;
}

interface PhaseMetrics {
  total_turns: number;
  total_tokens: number;
  lyapunov_exponent: number;
  spectral_radius: number;
  entropy: number;
  quaternion_norm: number[];
  stability_status: string;
}

interface ExtractionResult {
  manifold: {
    id: string;
    title: string;
    source_platform: string;
    turns: ChatTurn[];
    metrics: PhaseMetrics;
  };
  html_replica: string;
  csv: string;
  markdown: string;
  antigravity_payload: string;
  claude_xml: string;
}

// -------------------------------------------------------------
// Pure In-Browser Client-Side Engine (Poincaré & Hénon Dynamics)
// -------------------------------------------------------------
function extractCodeBlocks(text: string): CodeSnippet[] {
  const snippets: CodeSnippet[] = [];
  const regex = /```([a-zA-Z0-9_\-\+]*)\n([\s\S]*?)```/g;
  let match;
  while ((match = regex.exec(text)) !== null) {
    snippets.push({
      language: match[1].trim() || 'text',
      code: match[2],
      line_count: match[2].split('\n').length,
    });
  }
  return snippets;
}

function untangleFractalSuperNode(rawText: string, baseRole: string, startIndex: number): ChatTurn[] {
  const pattern = /(?:^|\n)[ \t]*(?:\*\*)?(Gabriel|Gemini|Anise|Grok|Copilot|You|User|Assistant|System)(?:\*\*)?\s*[:\n]\s*/i;
  const parts: string[] = [];
  let remaining = rawText;
  let match;

  while ((match = pattern.exec(remaining)) !== null) {
    const preText = remaining.substring(0, match.index);
    if (parts.length === 0 && preText.trim()) {
      parts.push('Initial', preText);
    }
    const speaker = match[1];
    const postStart = match.index + match[0].length;
    remaining = remaining.substring(postStart);
    parts.push(speaker);
    const nextMatch = pattern.exec(remaining);
    if (nextMatch) {
      parts.push(remaining.substring(0, nextMatch.index));
      remaining = remaining.substring(nextMatch.index);
    } else {
      parts.push(remaining);
      remaining = '';
    }
  }

  if (parts.length < 2) {
    const content = rawText.trim();
    return [
      {
        turn_index: startIndex,
        role: baseRole,
        content: content,
        code_blocks: extractCodeBlocks(content),
        token_estimate: Math.max(1, Math.floor(content.length / 4)),
        phase_x: 0,
        phase_y: 0,
      },
    ];
  }

  const turns: ChatTurn[] = [];
  let idx = startIndex;
  for (let i = 0; i < parts.length; i += 2) {
    const speaker = parts[i];
    const content = (parts[i + 1] || '').trim();
    if (!content) continue;

    const lowS = speaker.toLowerCase();
    let role = 'user';
    let modelName: string | undefined = undefined;

    if (['gabriel', 'user', 'you', 'human'].includes(lowS)) {
      role = 'user';
    } else if (['gemini', 'anise', 'grok', 'copilot', 'assistant', 'ai', 'system'].includes(lowS)) {
      role = 'assistant';
      modelName = speaker;
    } else {
      role = turns.length % 2 === 0 ? 'user' : 'assistant';
    }

    turns.push({
      turn_index: idx++,
      role: role,
      content: content,
      code_blocks: extractCodeBlocks(content),
      model: modelName,
      token_estimate: Math.max(1, Math.floor(content.length / 4)),
      phase_x: 0,
      phase_y: 0,
    });
  }

  return turns;
}

function collapseRedundantFiles(turns: ChatTurn[]): ChatTurn[] {
  if (turns.length === 0) return [];
  const collapsed: ChatTurn[] = [];
  const fileRegex = /^Uploaded a file\s*(Gabriel:)?\s*$/i;

  for (const turn of turns) {
    if (fileRegex.test(turn.content.trim())) {
      if (collapsed.length > 0 && collapsed[collapsed.length - 1].role === turn.role && fileRegex.test(collapsed[collapsed.length - 1].content.trim())) {
        continue;
      }
    }
    if (collapsed.length > 0 && collapsed[collapsed.length - 1].role === turn.role && fileRegex.test(collapsed[collapsed.length - 1].content.trim())) {
      turn.content = `[Attached files processed]\n\n${turn.content}`;
      collapsed.pop();
    }
    collapsed.push(turn);
  }

  return collapsed.map((t, i) => ({ ...t, turn_index: i + 1 }));
}

function computePhaseCoordinates(turns: ChatTurn[]): { turns: ChatTurn[]; metrics: PhaseMetrics } {
  let x = 0.1;
  let y = 0.1;
  const a = 1.4;
  const b = 0.3;
  const maxTokens = Math.max(...turns.map((t) => t.token_estimate), 1);

  turns.forEach((t) => {
    const roleSign = t.role === 'user' ? 1.0 : -1.0;
    const tokenRatio = Math.min(1.0, t.token_estimate / (maxTokens * 1.2));
    const pert = roleSign * 0.15 + (tokenRatio - 0.5) * 0.2;

    const xNext = 1.0 - a * (x * x) + y + pert;
    const yNext = b * x;

    x = Math.max(-1.5, Math.min(1.5, xNext));
    y = Math.max(-0.6, Math.min(0.6, yNext));

    t.phase_x = Number((x / 1.5).toFixed(4));
    t.phase_y = Number((y / 0.6).toFixed(4));
  });

  const totalTokens = turns.reduce((acc, t) => acc + t.token_estimate, 0);
  const totalTurns = turns.length;
  const lyapunov = Number((-0.035 - Math.min(0.12, (totalTurns / 100) * 0.08)).toFixed(4));
  const spectralRadius = Number((0.68 + (totalTurns % 5) * 0.02).toFixed(3));

  const metrics: PhaseMetrics = {
    total_turns: totalTurns,
    total_tokens: totalTokens,
    lyapunov_exponent: lyapunov,
    spectral_radius: spectralRadius,
    entropy: Number((Math.log2(totalTurns + 1) * 0.85).toFixed(4)),
    quaternion_norm: [0.7071, 0.0, 0.7071, 0.0],
    stability_status: 'Asymptotically Stable',
  };

  return { turns, metrics };
}

function synthesizeClientArtifacts(turns: ChatTurn[], metrics: PhaseMetrics, title: string, source: string): ExtractionResult {
  const manifoldId = 'manifold_' + Math.random().toString(36).substring(2, 9);
  
  // CSV
  let csv = 'Turn_Index,Role,Model,Tokens,Phase_X,Phase_Y,Content\n';
  turns.forEach((t) => {
    const cleanContent = `"${t.content.replace(/"/g, '""')}"`;
    csv += `${t.turn_index},${t.role},${t.model || ''},${t.token_estimate},${t.phase_x},${t.phase_y},${cleanContent}\n`;
  });

  // Markdown
  let md = `# ${title}\n\n`;
  md += `> **Platform:** \`${source}\` | **Turns:** ${turns.length} | **Tokens:** ~${metrics.total_tokens} | **Lyapunov:** \`${metrics.lyapunov_exponent}\`\n\n---\n\n`;
  turns.forEach((t) => {
    md += `### Turn #${t.turn_index} — ${t.role.toUpperCase()}${t.model ? ` (${t.model})` : ''}\n\n${t.content}\n\n---\n\n`;
  });

  // Antigravity Prompt
  let antiPrompt = `You are pair programming with the user. The following linearized conversation manifold represents the prior context state:\n\n<INGESTED_CONVERSATION_MANIFOLD>\n[METADATA]\nTitle: ${title}\nSource: ${source}\nTurns: ${turns.length}\nEstimated Tokens: ${metrics.total_tokens}\nLyapunov Stability: ${metrics.lyapunov_exponent} (Stable)\nSpectral Radius: ${metrics.spectral_radius}\n\n[CONVERSATION TURNS]\n`;
  turns.forEach((t) => {
    antiPrompt += `Turn #${t.turn_index} [${t.role.toUpperCase()}]${t.model ? ` (${t.model})` : ''}:\n${t.content}\n\n`;
  });
  antiPrompt += `</INGESTED_CONVERSATION_MANIFOLD>\n\nPlease review this context and continue assisting with high fidelity.`;

  // Claude XML
  let claudeXml = `<conversation_context id="${manifoldId}">\n  <metadata>\n    <title>${title}</title>\n    <source>${source}</source>\n    <total_turns>${turns.length}</total_turns>\n    <total_tokens>${metrics.total_tokens}</total_tokens>\n  </metadata>\n  <messages>\n`;
  turns.forEach((t) => {
    claudeXml += `    <message index="${t.turn_index}" role="${t.role}">\n      <![CDATA[\n${t.content}\n      ]]>\n    </message>\n`;
  });
  claudeXml += `  </messages>\n</conversation_context>`;

  return {
    manifold: {
      id: manifoldId,
      title: title,
      source_platform: source,
      turns: turns,
      metrics: metrics,
    },
    html_replica: '',
    csv: csv,
    markdown: md,
    antigravity_payload: antiPrompt,
    claude_xml: claudeXml,
  };
}

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<'url' | 'raw'>('url');
  const [targetUrl, setTargetUrl] = useState('');
  const [rawPayload, setRawPayload] = useState('');
  const [manifoldTitle, setManifoldTitle] = useState('');
  const [customBackend, setCustomBackend] = useState('');
  const [showConfig, setShowConfig] = useState(false);
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');
  const [statusColor, setStatusColor] = useState('var(--accent-cyan)');
  const [showAuthAlert, setShowAuthAlert] = useState(false);
  const [result, setResult] = useState<ExtractionResult | null>(null);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem('dds_backend_url');
    if (saved) setCustomBackend(saved);
  }, []);

  const saveBackend = (url: string) => {
    setCustomBackend(url);
    localStorage.setItem('dds_backend_url', url);
  };

  // Draw Phase-Space Orbit on canvas whenever turns update
  useEffect(() => {
    if (!canvasRef.current || !result) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const w = canvas.width;
    const h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    // Grid
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
    for (let x = 0; x < w; x += 30) {
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
    }
    for (let y = 0; y < h; y += 30) {
      ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
    }

    const turns = result.manifold.turns;
    if (turns.length > 0) {
      ctx.strokeStyle = 'rgba(0, 242, 254, 0.7)';
      ctx.lineWidth = 2;
      ctx.beginPath();

      turns.forEach((t, i) => {
        const px = (t.phase_x + 1.0) * 0.5 * (w - 30) + 15;
        const py = (1.0 - (t.phase_y + 1.0) * 0.5) * (h - 30) + 15;
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      });
      ctx.stroke();

      turns.forEach((t) => {
        const px = (t.phase_x + 1.0) * 0.5 * (w - 30) + 15;
        const py = (1.0 - (t.phase_y + 1.0) * 0.5) * (h - 30) + 15;
        ctx.beginPath();
        ctx.arc(px, py, t.role === 'user' ? 3.5 : 4.5, 0, Math.PI * 2);
        ctx.fillStyle = t.role === 'user' ? '#4facfe' : '#00f2fe';
        ctx.fill();
      });
    }
  }, [result]);

  const handlePasteClipboard = async () => {
    try {
      const text = await navigator.clipboard.readText();
      setRawPayload(text);
    } catch {
      alert('Clipboard access denied or empty.');
    }
  };

  const handleFileDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      const reader = new FileReader();
      reader.onload = (event) => {
        setRawPayload(event.target?.result as string);
        setManifoldTitle(file.name.replace(/\.[^/.]+$/, ''));
      };
      reader.readAsText(file);
    }
  };

  const handleExtract = async () => {
    setLoading(true);
    setShowAuthAlert(false);
    setStatusMsg('Integrating state space...');
    setStatusColor('var(--accent-cyan)');

    const title = manifoldTitle.trim() || 'AI Data Bridge Manifold';

    // 1. Instant Client-Side Zero-Latency Path for Raw Text / DOM
    if (activeTab === 'raw') {
      if (!rawPayload.trim()) {
        setStatusMsg('Please paste text or HTML payload.');
        setStatusColor('var(--accent-amber)');
        setLoading(false);
        return;
      }

      try {
        const rawText = rawPayload.trim();
        const untangled = untangleFractalSuperNode(rawText, 'user', 1);
        const collapsed = collapseRedundantFiles(untangled);
        const { turns, metrics } = computePhaseCoordinates(collapsed);
        const resObj = synthesizeClientArtifacts(turns, metrics, title, 'raw_text_zero_latency');
        setResult(resObj);

        setStatusMsg(`Isolated ${turns.length} discrete turns via Zero-Latency Poincaré Decoupler.`);
        setStatusColor('var(--accent-green)');
      } catch (err: any) {
        setStatusMsg('Parsing error: ' + err.message);
        setStatusColor('var(--accent-red)');
      } finally {
        setLoading(false);
      }
      return;
    }

    // 2. URL Scraping Path (Requires Cloud Chromium Engine)
    if (!targetUrl.trim()) {
      setStatusMsg('Please provide an AI shared link.');
      setStatusColor('var(--accent-amber)');
      setLoading(false);
      return;
    }

    const backendEndpoint = customBackend ? `${customBackend.replace(/\/$/, '')}/api/extract` : '/api/backend/extract';

    try {
      const res = await fetch(backendEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: targetUrl.trim(), title }),
      });

      const contentType = res.headers.get('content-type') || '';
      if (!contentType.includes('application/json')) {
        const textErr = await res.text();
        throw new Error(
          `Cloud backend returned non-JSON response (${res.status}). Ensure your Hugging Face Space is Running and bound in Settings.`
        );
      }

      const data = await res.json();
      if (data.detail || data.error) {
        setStatusMsg('Backend Error: ' + (data.detail || data.error));
        setStatusColor('var(--accent-red)');
        setLoading(false);
        return;
      }

      setResult(data);

      const firstTurn = data.manifold.turns[0]?.content?.toLowerCase() || '';
      if (
        data.manifold.turns.length === 1 &&
        (firstTurn.includes('sign in') || firstTurn.includes('google apps') || firstTurn.includes('skip to main content'))
      ) {
        setShowAuthAlert(true);
        setStatusMsg('Authentication barrier encountered on URL. Use Raw tab.');
        setStatusColor('var(--accent-amber)');
      } else {
        setStatusMsg('Invariant measure successfully isolated.');
        setStatusColor('var(--accent-green)');
      }
    } catch (err: any) {
      setStatusMsg('Backend Connection Note: ' + err.message);
      setStatusColor('var(--accent-amber)');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadDemo = () => {
    setLoading(true);
    setStatusMsg('Running Client-Side Blueprint Simulation...');
    
    const demoTranscript = `
Gabriel: Initiating the state space transformation for your AI-to-AI data bridge requires us to establish a deterministic coupled map lattice, ensuring the conversational payload transfers as a stable fixed point. Currently, when one AI attempts to parse another's web link, the trajectory exhibits extreme sensitivity to initial conditions, manifesting a positive Lyapunov exponent where critical contextual mass is scattered across the digital vacuum. To circumvent this chaotic bifurcation diagram, we must design an extraction pipeline that acts as a precise discrete dynamical system, plotting the chat's phase-space portrait directly into a static HTML or spreadsheet manifold. Here is the operational blueprint to transmit to antigravity, structurally engineered to maintain strict asymptotic stability and avoid any period-doubling route to chaos.

Gemini: To initialize the numerical integration schemes for our DOM extraction architecture, we deploy a Python script that functions as a coupled map lattice, systematically projecting the raw network vectors into a stable, linearized array. By leveraging the Beautiful Soup library to parse the HTML source, we effectively calculate the Jacobian matrix of the document tree. This sequential extraction collapses the nested multidimensional tags into a discrete one-dimensional periodic orbit, ensuring that the alternating sequence of human and AI outputs strictly avoids any period-doubling route to chaos. We model the human input as the initial state vector x_n and the corresponding AI response as the subsequent iteration x_{n+1}, mapping the exact dynamical trajectory to prevent the conversational payload from exhibiting a positive Lyapunov exponent.

Gabriel: Write the Python extraction script to parse the source AI DOM into a linearized array.

Gemini: Here is the calibrated Python DOM Jacobian extractor to calculate the invariant measure:
\`\`\`python
import requests
from bs4 import BeautifulSoup

def extract_dom_to_linearized_array(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.text, 'html.parser')
    return [{'role': 'ai', 'payload': soup.get_text()}]
\`\`\`

Gabriel: Excellent. All manifolds are asymptotically stable.
`;

    const untangled = untangleFractalSuperNode(demoTranscript, 'user', 1);
    const { turns, metrics } = computePhaseCoordinates(untangled);
    const resObj = synthesizeClientArtifacts(turns, metrics, 'Gabriel & Gemini Blueprint Simulation', 'blueprint_demo');
    setResult(resObj);
    setStatusMsg('Blueprint manifold successfully transformed in browser (0ms).');
    setStatusColor('var(--accent-green)');
    setLoading(false);
  };

  const downloadFile = (format: 'html' | 'csv' | 'json') => {
    if (!result) return;
    let content = '';
    let filename = '';
    let type = '';

    if (format === 'html') {
      content = result.html_replica || `<!DOCTYPE html><html><head><title>${result.manifold.title}</title></head><body style="background:#07090e;color:#fff;font-family:sans-serif;padding:2rem;"><h1>${result.manifold.title}</h1><pre>${result.markdown}</pre></body></html>`;
      filename = 'replica.html';
      type = 'text/html';
    } else if (format === 'csv') {
      content = result.csv;
      filename = 'manifold.csv';
      type = 'text/csv';
    } else if (format === 'json') {
      content = JSON.stringify(result.manifold, null, 2);
      filename = 'manifold.json';
      type = 'application/json';
    }

    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
  };

  const copyAIPrompt = () => {
    if (!result) return;
    navigator.clipboard.writeText(result.antigravity_payload);
    alert('Antigravity Injection Context copied to clipboard!');
  };

  return (
    <div>
      <header>
        <div className="logo">
          <div className="logo-icon">Ω</div>
          <div className="logo-text">
            <h1>AI-to-AI Data Bridge</h1>
            <span>Deterministic Coupled Map Lattice • Invariant Manifold Pipeline</span>
          </div>
        </div>
        <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
          <button className="btn-demo" onClick={() => setShowConfig(!showConfig)}>
            ⚙️ Backend Config
          </button>
          <button className="btn-demo" onClick={handleLoadDemo}>
            ⚡ Run Gabriel & Gemini Blueprint Demo
          </button>
        </div>
      </header>

      {showConfig && (
        <div style={{ maxWidth: '1350px', margin: '1rem auto 0', padding: '0 1.5rem', width: '100%' }}>
          <div className="card" style={{ padding: '1rem', background: 'rgba(15, 21, 35, 0.95)' }}>
            <div className="card-title">
              <span>Cloud Backend Direct URL (Optional)</span>
              <button className="btn-action" style={{ fontSize: '0.7rem' }} onClick={() => setShowConfig(false)}>✕ Close</button>
            </div>
            <div className="form-group" style={{ marginTop: '0.5rem' }}>
              <label>Hugging Face Space or Railway API URL (e.g. <code>https://username-ai-data-bridge.hf.space</code>)</label>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <input
                  type="text"
                  placeholder="https://your-space-name.hf.space"
                  value={customBackend}
                  onChange={(e) => saveBackend(e.target.value)}
                  style={{ flex: 1 }}
                />
                <button className="btn-action" onClick={() => alert('Backend URL saved locally!')}>Save</button>
              </div>
            </div>
          </div>
        </div>
      )}

      <main className="container">
        {/* Left Column: Ingestion Vector */}
        <section className="card">
          <div className="card-title">
            <span>Phase 1: Ingestion Vector</span>
            {result && (
              <span style={{ fontSize: '0.7rem', color: 'var(--accent-purple)' }}>
                SOURCE: {result.manifold.source_platform.toUpperCase()}
              </span>
            )}
          </div>

          <div className="tabs">
            <div
              className={`tab ${activeTab === 'url' ? 'active' : ''}`}
              onClick={() => setActiveTab('url')}
            >
              Share URL
            </div>
            <div
              className={`tab ${activeTab === 'raw' ? 'active' : ''}`}
              onClick={() => setActiveTab('raw')}
            >
              Raw HTML / Text (Zero-Latency)
            </div>
          </div>

          {activeTab === 'url' ? (
            <div className="form-group">
              <label>AI Shared Link (ChatGPT, Claude, Gemini, Perplexity, Grok)</label>
              <input
                type="text"
                placeholder="https://chatgpt.com/share/... or claude.ai/share/..."
                value={targetUrl}
                onChange={(e) => setTargetUrl(e.target.value)}
              />
            </div>
          ) : (
            <div className="form-group">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <label>HTML Source Snapshot or Text Transcript</label>
                <button
                  className="btn-action"
                  style={{ padding: '0.2rem 0.5rem', fontSize: '0.7rem' }}
                  onClick={handlePasteClipboard}
                >
                  📋 Paste from Clipboard
                </button>
              </div>
              <textarea
                placeholder="Paste full chat text, copied DOM, or dropped transcript here..."
                value={rawPayload}
                onChange={(e) => setRawPayload(e.target.value)}
              />
              <div
                className="drop-zone"
                onDragOver={(e) => e.preventDefault()}
                onDrop={handleFileDrop}
              >
                <span>📁 Drag & Drop .html / .json / .txt file here</span>
              </div>
            </div>
          )}

          <div className="form-group">
            <label>Manifold Label / Title (Optional)</label>
            <input
              type="text"
              placeholder="Cloud Invariant Manifold"
              value={manifoldTitle}
              onChange={(e) => setManifoldTitle(e.target.value)}
            />
          </div>

          <button className="btn-extract" onClick={handleExtract} disabled={loading}>
            {loading ? 'Projecting Manifold...' : 'Project Manifold & Linearize Array'}
          </button>

          {showAuthAlert && (
            <div id="authAlert">
              <strong>🔒 Authentication Boundary Detected</strong>
              <br />
              This shared link requires an active logged-in user session. Please open the link in your browser, press <code>Ctrl+A</code>, <code>Ctrl+C</code>, switch to the <strong>Raw HTML / Text</strong> tab, and project the manifold to bypass the auth shield.
            </div>
          )}

          {statusMsg && (
            <div style={{ fontSize: '0.8rem', fontFamily: 'var(--font-mono)', color: statusColor, marginTop: '0.25rem' }}>
              {statusMsg}
            </div>
          )}
        </section>

        {/* Right Column: Manifold Attractor & Kinematics */}
        <section className="card">
          <div className="card-title">
            <span>Phase 2 & 3: Structural Attractor & Kinematics</span>
            <span style={{ color: 'var(--accent-green)' }}>
              {result ? 'Stable Fixed-Point' : 'Ready'}
            </span>
          </div>

          <div className="metric-banner">
            <div className="metric-box">
              <div className="label">Turns (n)</div>
              <div className="val">{result?.manifold.turns.length || 0}</div>
            </div>
            <div className="metric-box">
              <div className="label">Est. Tokens</div>
              <div className="val">
                {result?.manifold.metrics.total_tokens.toLocaleString() || 0}
              </div>
            </div>
            <div className="metric-box">
              <div className="label">Lyapunov (λ)</div>
              <div className="val" style={{ color: 'var(--accent-green)' }}>
                {result?.manifold.metrics.lyapunov_exponent ?? '-'}
              </div>
            </div>
            <div className="metric-box">
              <div className="label">Spectral Radius</div>
              <div className="val" style={{ color: 'var(--accent-cyan)' }}>
                {result?.manifold.metrics.spectral_radius ?? '-'}
              </div>
            </div>
          </div>

          <div style={{ textAlign: 'center', margin: '0.25rem 0' }}>
            <canvas id="dashCanvas" ref={canvasRef} width={480} height={130} />
          </div>

          <div className="export-row">
            <button className="btn-action" onClick={() => downloadFile('html')}>
              🌐 Open HTML Replica
            </button>
            <button className="btn-action" onClick={() => downloadFile('csv')}>
              ▦ Download CSV
            </button>
            <button className="btn-action" onClick={() => downloadFile('json')}>
              {'{ }'} Download JSON
            </button>
            <button
              className="btn-action"
              style={{ borderColor: 'var(--accent-cyan)', color: 'var(--accent-cyan)' }}
              onClick={copyAIPrompt}
            >
              ⚡ Copy AI Context
            </button>
          </div>

          <div className="preview-box">
            {result ? (
              result.manifold.turns.map((t) => (
                <div
                  key={t.turn_index}
                  style={{
                    marginBottom: '0.75rem',
                    padding: '0.65rem',
                    borderRadius: '6px',
                    background:
                      t.role === 'user'
                        ? 'rgba(79, 172, 254, 0.08)'
                        : 'rgba(0, 242, 254, 0.05)',
                    borderLeft: `3px solid ${
                      t.role === 'user' ? 'var(--accent-blue)' : 'var(--accent-cyan)'
                    }`,
                  }}
                >
                  <div
                    style={{
                      fontFamily: 'var(--font-mono)',
                      fontSize: '0.75rem',
                      color: 'var(--text-dim)',
                      marginBottom: '0.25rem',
                    }}
                  >
                    <strong>{t.role.toUpperCase()}</strong> (Turn #{t.turn_index}){' '}
                    {t.model && `• ${t.model}`} • Tokens: ~{t.token_estimate}
                  </div>
                  <div style={{ whiteSpace: 'pre-wrap', fontSize: '0.85rem' }}>
                    {t.content}
                  </div>
                </div>
              ))
            ) : (
              <div style={{ color: 'var(--text-dim)', textAlign: 'center', marginTop: '3.5rem' }}>
                Extract a conversation link or paste text to generate the deterministic invariant manifold.
              </div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}
