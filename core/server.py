"""
Local Interactive Web Server & API for AI-to-AI Data Bridge.
Provides a modern visual interface for pasting URLs, dropping HTML snapshots,
inspecting real-time dynamical phase portraits, and downloading formatted manifolds.
Now equipped with Smart Auth-Shield Detection and Drag-and-Drop file ingestion.
"""

from __future__ import annotations
import http.server
import socketserver
import json
import urllib.parse
from typing import Optional
from .ingestion import ConversationExtractor
from .attractor import StructuralAttractor
from .propagation import PropagationVectorEngine


DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-to-AI Data Bridge • DDS Control Console</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-dark: #07090e;
            --bg-panel: #0f1523;
            --bg-input: #0a0d17;
            --border: rgba(0, 242, 254, 0.2);
            --accent-cyan: #00f2fe;
            --accent-blue: #4facfe;
            --accent-purple: #9d4edd;
            --accent-green: #10b981;
            --accent-amber: #f59e0b;
            --accent-red: #ef4444;
            --text: #f8fafc;
            --text-dim: #94a3b8;
            --font-main: 'Inter', sans-serif;
            --font-mono: 'Fira Code', monospace;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: var(--font-main);
            background: var(--bg-dark);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            background-image: radial-gradient(circle at 20% 20%, rgba(0, 242, 254, 0.04) 0%, transparent 50%),
                              radial-gradient(circle at 80% 80%, rgba(157, 78, 221, 0.04) 0%, transparent 50%);
        }

        header {
            padding: 1.25rem 2rem;
            border-bottom: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(15, 21, 35, 0.8);
            backdrop-filter: blur(10px);
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .logo-icon {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            color: #000;
            font-size: 1.3rem;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.3);
        }

        .logo-text h1 { font-size: 1.2rem; font-weight: 700; }
        .logo-text span { font-size: 0.75rem; font-family: var(--font-mono); color: var(--accent-cyan); }

        .container {
            max-width: 1350px;
            margin: 1.5rem auto;
            padding: 0 1.5rem;
            width: 100%;
            display: grid;
            grid-template-columns: 480px 1fr;
            gap: 1.5rem;
            flex: 1;
        }

        @media (max-width: 1000px) {
            .container { grid-template-columns: 1fr; }
        }

        .card {
            background: var(--bg-panel);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.2rem;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.4);
        }

        .card-title {
            font-size: 0.9rem;
            font-family: var(--font-mono);
            color: var(--accent-cyan);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        label {
            font-size: 0.8rem;
            font-family: var(--font-mono);
            color: var(--text-dim);
        }

        input[type="text"], textarea {
            background: var(--bg-input);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 0.75rem;
            color: var(--text);
            font-family: var(--font-main);
            font-size: 0.9rem;
            transition: border-color 0.2s;
        }

        input[type="text"]:focus, textarea:focus {
            outline: none;
            border-color: var(--accent-cyan);
        }

        textarea {
            resize: vertical;
            min-height: 140px;
            font-family: var(--font-mono);
            font-size: 0.8rem;
        }

        .drop-zone {
            border: 2px dashed rgba(0, 242, 254, 0.3);
            border-radius: 8px;
            padding: 1rem;
            text-align: center;
            background: rgba(0, 242, 254, 0.02);
            cursor: pointer;
            transition: all 0.2s;
        }

        .drop-zone.dragover {
            background: rgba(0, 242, 254, 0.1);
            border-color: var(--accent-cyan);
        }

        .drop-zone span {
            font-size: 0.75rem;
            font-family: var(--font-mono);
            color: var(--text-dim);
        }

        .btn-extract {
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
            border: none;
            color: #000;
            padding: 0.8rem;
            border-radius: 8px;
            font-weight: 700;
            font-family: var(--font-mono);
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .btn-extract:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
        }

        .btn-demo {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: var(--text-dim);
            padding: 0.5rem 0.8rem;
            border-radius: 6px;
            font-family: var(--font-mono);
            font-size: 0.75rem;
            cursor: pointer;
        }

        .btn-demo:hover {
            color: var(--text);
            border-color: var(--accent-purple);
        }

        .tabs {
            display: flex;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            gap: 1rem;
            margin-bottom: 0.25rem;
        }

        .tab {
            padding: 0.5rem 0.25rem;
            font-size: 0.85rem;
            font-family: var(--font-mono);
            color: var(--text-dim);
            cursor: pointer;
            border-bottom: 2px solid transparent;
        }

        .tab.active {
            color: var(--accent-cyan);
            border-bottom-color: var(--accent-cyan);
        }

        .metric-banner {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 0.75rem;
        }

        .metric-box {
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            padding: 0.6rem;
            text-align: center;
        }

        .metric-box .label { font-size: 0.65rem; font-family: var(--font-mono); color: var(--text-dim); }
        .metric-box .val { font-size: 1.1rem; font-weight: 700; font-family: var(--font-mono); color: var(--accent-cyan); margin-top: 0.2rem; }

        .preview-box {
            flex: 1;
            background: var(--bg-input);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 1rem;
            overflow-y: auto;
            max-height: 440px;
            font-size: 0.85rem;
        }

        .export-row {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
        }

        .btn-action {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 0.45rem 0.85rem;
            border-radius: 6px;
            font-family: var(--font-mono);
            font-size: 0.8rem;
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-action:hover {
            border-color: var(--accent-cyan);
            background: rgba(0, 242, 254, 0.1);
        }

        #authAlert {
            display: none;
            background: rgba(239, 68, 68, 0.1);
            border: 1px solid rgba(239, 68, 68, 0.4);
            border-radius: 8px;
            padding: 0.85rem 1rem;
            font-size: 0.8rem;
            color: #fca5a5;
            font-family: var(--font-mono);
            line-height: 1.4;
        }

        #canvasWrapper { text-align: center; margin: 0.25rem 0; }
        #dashCanvas {
            background: #05070c;
            border: 1px solid rgba(0, 242, 254, 0.2);
            border-radius: 8px;
        }
    </style>
</head>
<body>

    <header>
        <div class="logo">
            <div class="logo-icon">Ω</div>
            <div class="logo-text">
                <h1>AI-to-AI Data Bridge</h1>
                <span>Deterministic Coupled Map Lattice • Invariant Manifold Pipeline</span>
            </div>
        </div>
        <button class="btn-demo" onclick="loadDemo()">⚡ Run Gabriel & Gemini Blueprint Demo</button>
    </header>

    <div class="container">
        <!-- Input Form -->
        <div class="card">
            <div class="card-title">
                <span>Phase 1: Ingestion Vector</span>
                <span id="platformBadge" style="font-size: 0.7rem; color: var(--accent-purple);"></span>
            </div>

            <div class="tabs">
                <div class="tab active" onclick="switchInputTab('url', this)">Share URL</div>
                <div class="tab" onclick="switchInputTab('raw', this)">Raw HTML / Text (Zero-Latency)</div>
            </div>

            <div id="urlInputGroup" class="form-group">
                <label>AI Shared Link (ChatGPT, Claude, Gemini, Perplexity, Grok)</label>
                <input type="text" id="targetUrl" placeholder="https://chatgpt.com/share/... or claude.ai/share/...">
            </div>

            <div id="rawInputGroup" class="form-group" style="display:none;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <label>HTML Source Snapshot or Text Transcript</label>
                    <button class="btn-action" style="padding: 0.2rem 0.5rem; font-size: 0.7rem;" onclick="pasteFromClipboard()">📋 Paste from Clipboard</button>
                </div>
                <textarea id="rawPayload" placeholder="Paste full chat text, copied DOM, or dropped transcript here..."></textarea>
                
                <div class="drop-zone" id="dropZone" onclick="document.getElementById('fileInput').click()">
                    <span>📁 Drag & Drop .html / .json / .txt file here or click to browse</span>
                    <input type="file" id="fileInput" style="display:none;" onchange="handleFileSelect(event)">
                </div>
            </div>

            <div class="form-group">
                <label>Manifold Label / Title (Optional)</label>
                <input type="text" id="manifoldTitle" placeholder="Autonomous Bridge Manifold">
            </div>

            <button class="btn-extract" onclick="executeExtraction()">Project Manifold & Linearize Array</button>

            <!-- Authentication Boundary Detection Alert -->
            <div id="authAlert">
                <strong>🔒 Authentication Boundary Detected</strong><br>
                This shared link requires an active logged-in user session. Please open the link in your browser, press <code>Ctrl+A</code>, <code>Ctrl+C</code>, switch to the <strong>Raw HTML / Text</strong> tab, and project the manifold to bypass the auth shield.
            </div>

            <div id="statusMessage" style="font-size: 0.8rem; font-family: var(--font-mono); color: var(--accent-cyan); display: none;"></div>
        </div>

        <!-- Output Panel -->
        <div class="card">
            <div class="card-title">
                <span>Phase 2 & 3: Structural Attractor & Kinematics</span>
                <span id="statusIndicator" style="color: var(--accent-green);">Ready</span>
            </div>

            <div class="metric-banner">
                <div class="metric-box">
                    <div class="label">Turns (n)</div>
                    <div class="val" id="metricTurns">0</div>
                </div>
                <div class="metric-box">
                    <div class="label">Est. Tokens</div>
                    <div class="val" id="metricTokens">0</div>
                </div>
                <div class="metric-box">
                    <div class="label">Lyapunov (λ)</div>
                    <div class="val" id="metricLyapunov">-</div>
                </div>
                <div class="metric-box">
                    <div class="label">Spectral Radius</div>
                    <div class="val" id="metricRadius">-</div>
                </div>
            </div>

            <div id="canvasWrapper">
                <canvas id="dashCanvas" width="480" height="130"></canvas>
            </div>

            <div class="export-row">
                <button class="btn-action" onclick="downloadFile('html')">🌐 Open HTML Replica</button>
                <button class="btn-action" onclick="downloadFile('csv')">▦ Download CSV</button>
                <button class="btn-action" onclick="downloadFile('json')">{ } Download JSON</button>
                <button class="btn-action" onclick="copyAIPrompt()" style="border-color: var(--accent-cyan); color: var(--accent-cyan);">⚡ Copy AI Context</button>
            </div>

            <div class="preview-box" id="previewContainer">
                <div style="color: var(--text-dim); text-align: center; margin-top: 3.5rem;">
                    Extract a conversation link or paste text to generate the deterministic invariant manifold.
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentExtraction = null;
        let activeInputMode = 'url';

        function switchInputTab(mode, elem) {
            activeInputMode = mode;
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            elem.classList.add('active');
            document.getElementById('urlInputGroup').style.display = mode === 'url' ? 'flex' : 'none';
            document.getElementById('rawInputGroup').style.display = mode === 'raw' ? 'flex' : 'none';
        }

        async function pasteFromClipboard() {
            try {
                const text = await navigator.clipboard.readText();
                document.getElementById('rawPayload').value = text;
            } catch (e) {
                alert('Clipboard access denied or empty.');
            }
        }

        // Drag & Drop Setup
        const dropZone = document.getElementById('dropZone');
        ['dragenter', 'dragover'].forEach(name => {
            dropZone.addEventListener(name, (e) => { e.preventDefault(); dropZone.classList.add('dragover'); });
        });
        ['dragleave', 'drop'].forEach(name => {
            dropZone.addEventListener(name, (e) => { e.preventDefault(); dropZone.classList.remove('dragover'); });
        });
        dropZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) readFile(files[0]);
        });

        function handleFileSelect(e) {
            if (e.target.files.length > 0) readFile(e.target.files[0]);
        }

        function readFile(file) {
            const reader = new FileReader();
            reader.onload = (event) => {
                document.getElementById('rawPayload').value = event.target.result;
                document.getElementById('manifoldTitle').value = file.name.replace(/\\.[^/.]+$/, "");
            };
            reader.readAsText(file);
        }

        async function executeExtraction() {
            const status = document.getElementById('statusMessage');
            const authAlert = document.getElementById('authAlert');
            authAlert.style.display = 'none';
            status.style.display = 'block';
            status.innerText = 'Calculating Jacobian and integrating DOM coordinates...';

            const payload = {
                url: activeInputMode === 'url' ? document.getElementById('targetUrl').value.trim() : null,
                raw: activeInputMode === 'raw' ? document.getElementById('rawPayload').value.trim() : null,
                title: document.getElementById('manifoldTitle').value.trim() || 'AI Data Bridge Manifold'
            };

            try {
                const res = await fetch('/api/extract', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(payload)
                });
                const data = await res.json();
                if (data.error) {
                    status.innerText = 'Error: ' + data.error;
                    status.style.color = 'var(--accent-red)';
                    return;
                }
                currentExtraction = data;
                displayResults(data);

                // Check for auth boundary wall
                if (data.manifold.turns.length === 1 && (
                    data.manifold.turns[0].content.toLowerCase().includes('sign in') ||
                    data.manifold.turns[0].content.toLowerCase().includes('google apps') ||
                    data.manifold.turns[0].content.toLowerCase().includes('skip to main content')
                )) {
                    authAlert.style.display = 'block';
                    status.innerText = 'Authentication barrier encountered on URL.';
                    status.style.color = 'var(--accent-amber)';
                } else {
                    status.innerText = 'Invariant measure successfully isolated.';
                    status.style.color = 'var(--accent-green)';
                }
            } catch (err) {
                status.innerText = 'Extraction error: ' + err.message;
                status.style.color = 'var(--accent-red)';
            }
        }

        async function loadDemo() {
            const status = document.getElementById('statusMessage');
            status.style.display = 'block';
            status.innerText = 'Loading Gabriel & Gemini blueprint simulation...';
            try {
                const res = await fetch('/api/demo');
                const data = await res.json();
                currentExtraction = data;
                displayResults(data);
                status.innerText = 'Blueprint manifold successfully transformed.';
                status.style.color = 'var(--accent-green)';
            } catch (err) {
                status.innerText = 'Demo error: ' + err.message;
            }
        }

        function displayResults(data) {
            const m = data.manifold;
            document.getElementById('metricTurns').innerText = m.turns.length;
            document.getElementById('metricTokens').innerText = m.metrics.total_tokens.toLocaleString();
            document.getElementById('metricLyapunov').innerText = m.metrics.lyapunov_exponent;
            document.getElementById('metricRadius').innerText = m.metrics.spectral_radius;
            document.getElementById('platformBadge').innerText = 'SOURCE: ' + m.source_platform.toUpperCase();

            const preview = document.getElementById('previewContainer');
            preview.innerHTML = '';
            m.turns.forEach(t => {
                const div = document.createElement('div');
                div.style.marginBottom = '0.75rem';
                div.style.padding = '0.65rem';
                div.style.borderRadius = '6px';
                div.style.background = t.role === 'user' ? 'rgba(79, 172, 254, 0.08)' : 'rgba(0, 242, 254, 0.05)';
                div.style.borderLeft = `3px solid ${t.role === 'user' ? 'var(--accent-blue)' : 'var(--accent-cyan)'}`;
                
                div.innerHTML = `
                    <div style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-dim); margin-bottom: 0.25rem;">
                        <strong>${t.role.toUpperCase()}</strong> (Turn #${t.turn_index}) ${t.model ? '• ' + t.model : ''} • Tokens: ~${t.token_estimate}
                    </div>
                    <div style="white-space: pre-wrap; font-size: 0.85rem;">${escapeHtml(t.content)}</div>
                `;
                preview.appendChild(div);
            });

            drawPhasePortrait(m.turns);
        }

        function drawPhasePortrait(turns) {
            const canvas = document.getElementById('dashCanvas');
            const ctx = canvas.getContext('2d');
            const w = canvas.width;
            const h = canvas.height;
            ctx.clearRect(0, 0, w, h);

            ctx.strokeStyle = 'rgba(255, 255, 255, 0.04)';
            for(let x=0; x<w; x+=30) { ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,h); ctx.stroke(); }
            for(let y=0; y<h; y+=30) { ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }

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

            turns.forEach(t => {
                const px = (t.phase_x + 1.0) * 0.5 * (w - 30) + 15;
                const py = (1.0 - (t.phase_y + 1.0) * 0.5) * (h - 30) + 15;
                ctx.beginPath();
                ctx.arc(px, py, t.role === 'user' ? 3.5 : 4.5, 0, Math.PI * 2);
                ctx.fillStyle = t.role === 'user' ? '#4facfe' : '#00f2fe';
                ctx.fill();
            });
        }

        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }

        function downloadFile(format) {
            if (!currentExtraction) return;
            let content, filename, type;
            if (format === 'html') {
                content = currentExtraction.html_replica;
                filename = 'replica.html';
                type = 'text/html';
            } else if (format === 'csv') {
                content = currentExtraction.csv;
                filename = 'manifold.csv';
                type = 'text/csv';
            } else if (format === 'json') {
                content = JSON.stringify(currentExtraction.manifold, null, 2);
                filename = 'manifold.json';
                type = 'application/json';
            }
            const blob = new Blob([content], {type});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
        }

        function copyAIPrompt() {
            if (!currentExtraction) return;
            navigator.clipboard.writeText(currentExtraction.antigravity_payload);
            alert('Antigravity Injection Context copied to clipboard!');
        }
    </script>
</body>
</html>
"""


class BridgeRequestHandler(http.server.BaseHTTPRequestHandler):
    """HTTP Request Handler providing REST API and Dashboard."""

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path in ["/", "/index.html"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(DASHBOARD_HTML.encode("utf-8"))
        elif parsed.path == "/api/demo":
            extractor = ConversationExtractor()
            demo_text = (
                "Gabriel: Initiating the state space transformation for your AI-to-AI data bridge requires us to establish a deterministic coupled map lattice...\n\n"
                "Gemini: To initialize the numerical integration schemes for our DOM extraction architecture, we deploy a Python script that functions as a coupled map lattice...\n\n"
                "Gabriel: Write the Python extraction script to parse the source AI DOM into a linearized array.\n\n"
                "Gemini: Here is the calibrated Python DOM Jacobian extractor:\n```python\nimport requests\nfrom bs4 import BeautifulSoup\n\ndef extract_dom(url):\n    soup = BeautifulSoup(requests.get(url).text, 'html.parser')\n    return [{'role': 'ai', 'payload': soup.get_text()}]\n```"
            )
            manifold = extractor.extract_from_text(demo_text, title="Gabriel & Gemini DDS Bridge Blueprint")
            attractor = StructuralAttractor(manifold)
            propagation = PropagationVectorEngine(manifold)

            response_data = {
                "manifold": manifold.to_dict(),
                "html_replica": attractor.to_html_replica(),
                "csv": attractor.to_csv(),
                "markdown": attractor.to_markdown(),
                "antigravity_payload": propagation.synthesize_antigravity_payload(),
                "claude_xml": propagation.synthesize_claude_xml()
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/extract":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode("utf-8")
            data = json.loads(body)

            extractor = ConversationExtractor()
            url = data.get("url")
            raw = data.get("raw")
            title = data.get("title", "AI Data Bridge Manifold")

            try:
                if url:
                    manifold = extractor.extract_from_url(url)
                elif raw:
                    if "<html" in raw.lower() or "<article" in raw.lower() or "<div class=" in raw.lower():
                        manifold = extractor.extract_from_html(raw, source_platform="html_snapshot")
                    elif raw.strip().startswith("{") or raw.strip().startswith("["):
                        manifold = extractor.extract_from_json(raw)
                    else:
                        manifold = extractor.extract_from_text(raw, title=title)
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Either 'url' or 'raw' payload must be provided."}).encode("utf-8"))
                    return

                attractor = StructuralAttractor(manifold)
                propagation = PropagationVectorEngine(manifold)

                response_data = {
                    "manifold": manifold.to_dict(),
                    "html_replica": attractor.to_html_replica(),
                    "csv": attractor.to_csv(),
                    "markdown": attractor.to_markdown(),
                    "antigravity_payload": propagation.synthesize_antigravity_payload(),
                    "claude_xml": propagation.synthesize_claude_xml()
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))

            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))

    def log_message(self, format, *args):
        return


def start_server(port: int = 8080):
    """Starts the local DDS Data Bridge Web Dashboard."""
    with socketserver.TCPServer(("", port), BridgeRequestHandler) as httpd:
        print(f"[DDS-Bridge] Web Console active at http://localhost:{port}")
        print(f"[DDS-Bridge] Serving deterministic coupled map lattice interface...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[DDS-Bridge] Shutting down server gracefully.")
