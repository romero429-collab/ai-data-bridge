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

export default function Dashboard() {
  const [activeTab, setActiveTab] = useState<'url' | 'raw'>('url');
  const [targetUrl, setTargetUrl] = useState('');
  const [rawPayload, setRawPayload] = useState('');
  const [manifoldTitle, setManifoldTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [statusMsg, setStatusMsg] = useState('');
  const [statusColor, setStatusColor] = useState('var(--accent-cyan)');
  const [showAuthAlert, setShowAuthAlert] = useState(false);
  const [result, setResult] = useState<ExtractionResult | null>(null);

  const canvasRef = useRef<HTMLCanvasElement | null>(null);

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
    setStatusMsg('Calculating Jacobian and integrating state space...');
    setStatusColor('var(--accent-cyan)');

    const payload = {
      url: activeTab === 'url' ? targetUrl.trim() : null,
      raw: activeTab === 'raw' ? rawPayload.trim() : null,
      title: manifoldTitle.trim() || 'AI Data Bridge Manifold',
    };

    try {
      // Calls Next.js proxy route which forwards to Railway backend
      const res = await fetch('/api/backend/extract', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (data.detail || data.error) {
        setStatusMsg('Error: ' + (data.detail || data.error));
        setStatusColor('var(--accent-red)');
        setLoading(false);
        return;
      }

      setResult(data);

      // Check for auth boundary wall
      const firstTurn = data.manifold.turns[0]?.content?.toLowerCase() || '';
      if (
        data.manifold.turns.length === 1 &&
        (firstTurn.includes('sign in') || firstTurn.includes('google apps') || firstTurn.includes('skip to main content'))
      ) {
        setShowAuthAlert(true);
        setStatusMsg('Authentication barrier encountered on URL.');
        setStatusColor('var(--accent-amber)');
      } else {
        setStatusMsg('Invariant measure successfully isolated.');
        setStatusColor('var(--accent-green)');
      }
    } catch (err: any) {
      setStatusMsg('Connection Error: ' + err.message);
      setStatusColor('var(--accent-red)');
    } finally {
      setLoading(false);
    }
  };

  const handleLoadDemo = async () => {
    setLoading(true);
    setStatusMsg('Loading Gabriel & Gemini blueprint simulation...');
    try {
      const res = await fetch('/api/backend/demo');
      const data = await res.json();
      setResult(data);
      setStatusMsg('Blueprint manifold successfully transformed.');
      setStatusColor('var(--accent-green)');
    } catch (err: any) {
      setStatusMsg('Demo Error: ' + err.message);
      setStatusColor('var(--accent-red)');
    } finally {
      setLoading(false);
    }
  };

  const downloadFile = (format: 'html' | 'csv' | 'json') => {
    if (!result) return;
    let content = '';
    let filename = '';
    let type = '';

    if (format === 'html') {
      content = result.html_replica;
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
        <button className="btn-demo" onClick={handleLoadDemo}>
          ⚡ Run Gabriel & Gemini Blueprint Demo
        </button>
      </header>

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
            <div style={{ fontSize: '0.8rem', fontFamily: 'var(--font-mono)', color: statusColor }}>
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
