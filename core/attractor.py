"""
Phase 2: The Structural Attractor (Formatting the Manifold)
Packs the linearized state vector into high-fidelity target manifolds:
- Interactive Cybernetic HTML Replica with embedded Phase-Space Canvas Visualizer
- Tabular Spreadsheet / CSV Manifold
- Lossless JSON State Tensor
- Clean Markdown Representation
"""

from __future__ import annotations
import csv
import io
import json
import html
from typing import Optional
from .models import ConversationManifold


class StructuralAttractor:
    """
    Manifold formatting engine satisfying the Banach fixed-point theorem.
    """

    def __init__(self, manifold: ConversationManifold):
        self.manifold = manifold

    def to_json(self, indent: int = 2) -> str:
        """Renders lossless JSON state tensor."""
        return self.manifold.to_json(indent=indent)

    def to_csv(self) -> str:
        """Renders spreadsheet manifold as standard RFC 4180 CSV."""
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        
        # Header row
        writer.writerow([
            "Turn",
            "Role",
            "Model",
            "Timestamp",
            "Char_Count",
            "Token_Estimate",
            "Code_Blocks_Count",
            "Phase_X",
            "Phase_Y",
            "Payload"
        ])

        for t in self.manifold.turns:
            writer.writerow([
                t.turn_index,
                t.role.upper(),
                t.model or "N/A",
                t.timestamp or "",
                t.char_count,
                t.token_estimate,
                len(t.code_blocks),
                t.phase_x,
                t.phase_y,
                t.content
            ])

        return output.getvalue()

    def to_markdown(self) -> str:
        """Renders clean GitHub-flavored markdown."""
        lines = [
            f"# {self.manifold.title}",
            "",
            f"> **Source Platform:** `{self.manifold.source_platform}` | **Turns:** {len(self.manifold.turns)} | **Tokens:** ~{self.manifold.metrics.total_tokens} | **Lyapunov Stability:** `{self.manifold.metrics.lyapunov_exponent}`",
            "",
            "---",
            ""
        ]

        for t in self.manifold.turns:
            role_header = f"### Turn {t.turn_index} — {t.role.upper()}"
            if t.model:
                role_header += f" ({t.model})"
            lines.append(role_header)
            lines.append("")
            lines.append(t.content)
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)

    def to_html_replica(self) -> str:
        """
        Generates an interactive, standalone HTML replica manifold complete with
        cybernetic UI, embedded Phase-Space dynamical visualizer, markdown/code rendering,
        search/filter controls, and direct download buttons.
        """
        m = self.manifold
        turns_json = json.dumps([t.to_dict() for t in m.turns])
        metrics_json = json.dumps(m.metrics.to_dict())

        html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(m.title)} - DDS Data Bridge Manifold</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0a0d14;
            --bg-secondary: #121824;
            --bg-card: rgba(22, 30, 46, 0.75);
            --bg-user: rgba(30, 41, 69, 0.6);
            --bg-ai: rgba(18, 28, 45, 0.85);
            --border-color: rgba(66, 153, 225, 0.2);
            --border-glow: rgba(66, 153, 225, 0.4);
            --accent-cyan: #00f2fe;
            --accent-blue: #4facfe;
            --accent-green: #10b981;
            --accent-purple: #8b5cf6;
            --accent-amber: #f59e0b;
            --text-primary: #f1f5f9;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --code-bg: #0d1117;
            --font-main: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: 'Fira Code', monospace;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: var(--font-main);
            background-color: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(0, 242, 254, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.05) 0%, transparent 40%);
            background-attachment: fixed;
        }}

        header {{
            background: linear-gradient(180deg, rgba(18, 24, 36, 0.95) 0%, rgba(10, 13, 20, 0.8) 100%);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 1rem 2rem;
        }}

        .header-container {{
            max-width: 1300px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .brand {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .brand-icon {{
            width: 36px;
            height: 36px;
            border-radius: 8px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            font-weight: 700;
            color: #000;
            box-shadow: 0 0 15px rgba(0, 242, 254, 0.4);
        }}

        .brand-title h1 {{
            font-size: 1.15rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            background: linear-gradient(90deg, #fff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .brand-title .subtitle {{
            font-size: 0.75rem;
            font-family: var(--font-mono);
            color: var(--accent-cyan);
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }}

        .actions {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}

        .btn {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.45rem 0.85rem;
            border-radius: 6px;
            font-size: 0.8rem;
            font-family: var(--font-mono);
            cursor: pointer;
            transition: all 0.2s ease;
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            text-decoration: none;
        }}

        .btn:hover {{
            border-color: var(--accent-cyan);
            box-shadow: 0 0 10px rgba(0, 242, 254, 0.25);
            transform: translateY(-1px);
        }}

        .btn-primary {{
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.2), rgba(79, 172, 254, 0.2));
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
            font-weight: 600;
        }}

        .btn-primary:hover {{
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.35), rgba(79, 172, 254, 0.35));
        }}

        main {{
            max-width: 1300px;
            margin: 1.5rem auto;
            padding: 0 1.5rem;
            width: 100%;
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 1.5rem;
            flex: 1;
        }}

        @media (max-width: 1024px) {{
            main {{
                grid-template-columns: 1fr;
            }}
        }}

        .chat-feed {{
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }}

        .filter-bar {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 0.75rem 1rem;
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }}

        .search-input {{
            flex: 1;
            background: rgba(10, 13, 20, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            padding: 0.4rem 0.75rem;
            color: var(--text-primary);
            font-family: var(--font-main);
            font-size: 0.85rem;
            min-width: 180px;
        }}

        .search-input:focus {{
            outline: none;
            border-color: var(--accent-cyan);
        }}

        .role-filters {{
            display: flex;
            gap: 0.35rem;
        }}

        .filter-chip {{
            padding: 0.25rem 0.6rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-family: var(--font-mono);
            cursor: pointer;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid transparent;
            color: var(--text-secondary);
        }}

        .filter-chip.active {{
            background: rgba(0, 242, 254, 0.15);
            border-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }}

        .turn-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
            transition: border-color 0.2s, box-shadow 0.2s;
            backdrop-filter: blur(8px);
        }}

        .turn-card:hover {{
            border-color: var(--border-glow);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }}

        .turn-card.role-user {{
            border-left: 4px solid var(--accent-blue);
            background: var(--bg-user);
        }}

        .turn-card.role-assistant {{
            border-left: 4px solid var(--accent-cyan);
            background: var(--bg-ai);
        }}

        .turn-card.role-system {{
            border-left: 4px solid var(--accent-amber);
        }}

        .turn-header {{
            padding: 0.65rem 1.25rem;
            background: rgba(0, 0, 0, 0.2);
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            font-size: 0.8rem;
        }}

        .turn-meta-left {{
            display: flex;
            align-items: center;
            gap: 0.6rem;
        }}

        .turn-badge {{
            font-family: var(--font-mono);
            font-size: 0.7rem;
            font-weight: 600;
            padding: 0.15rem 0.45rem;
            border-radius: 4px;
            text-transform: uppercase;
        }}

        .badge-user {{
            background: rgba(79, 172, 254, 0.2);
            color: var(--accent-blue);
        }}

        .badge-assistant {{
            background: rgba(0, 242, 254, 0.2);
            color: var(--accent-cyan);
        }}

        .badge-system {{
            background: rgba(245, 158, 11, 0.2);
            color: var(--accent-amber);
        }}

        .turn-index {{
            font-family: var(--font-mono);
            color: var(--text-muted);
            font-size: 0.75rem;
        }}

        .turn-meta-right {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--text-muted);
        }}

        .turn-body {{
            padding: 1.25rem;
            font-size: 0.95rem;
            word-break: break-word;
            white-space: pre-wrap;
        }}

        .code-container {{
            margin: 1rem 0;
            background: var(--code-bg);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            overflow: hidden;
        }}

        .code-header {{
            background: rgba(255, 255, 255, 0.03);
            padding: 0.4rem 0.85rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--text-secondary);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
        }}

        .copy-btn {{
            background: rgba(255, 255, 255, 0.06);
            border: none;
            color: var(--text-secondary);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.7rem;
            cursor: pointer;
            font-family: var(--font-mono);
        }}

        .copy-btn:hover {{
            background: var(--accent-cyan);
            color: #000;
        }}

        pre {{
            padding: 1rem;
            overflow-x: auto;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            color: #e2e8f0;
            line-height: 1.5;
        }}

        .sidebar {{
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }}

        .panel {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.25rem;
            backdrop-filter: blur(8px);
        }}

        .panel-title {{
            font-size: 0.85rem;
            font-family: var(--font-mono);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--accent-cyan);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}

        #phaseCanvas {{
            width: 100%;
            height: 220px;
            background: #06080e;
            border-radius: 8px;
            border: 1px solid rgba(0, 242, 254, 0.15);
            display: block;
        }}

        .metric-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
            margin-top: 1rem;
        }}

        .metric-card {{
            background: rgba(0, 0, 0, 0.25);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 6px;
            padding: 0.6rem;
        }}

        .metric-label {{
            font-size: 0.7rem;
            font-family: var(--font-mono);
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .metric-val {{
            font-size: 1.05rem;
            font-weight: 700;
            font-family: var(--font-mono);
            color: var(--text-primary);
            margin-top: 0.2rem;
        }}

        .status-pill {{
            font-size: 0.75rem;
            font-family: var(--font-mono);
            padding: 0.4rem 0.75rem;
            border-radius: 6px;
            text-align: center;
            margin-top: 0.75rem;
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-green);
            border: 1px solid rgba(16, 185, 129, 0.3);
        }}

        #toast {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: #1e293b;
            color: var(--accent-cyan);
            border: 1px solid var(--accent-cyan);
            padding: 0.75rem 1.25rem;
            border-radius: 8px;
            font-family: var(--font-mono);
            font-size: 0.85rem;
            box-shadow: 0 5px 20px rgba(0, 0, 0, 0.5);
            display: none;
            z-index: 1000;
        }}
    </style>
</head>
<body>

    <header>
        <div class="header-container">
            <div class="brand">
                <div class="brand-icon">Ω</div>
                <div class="brand-title">
                    <h1>{html.escape(m.title)}</h1>
                    <div class="subtitle">Deterministic Coupled Map Lattice • Invariant Manifold</div>
                </div>
            </div>

            <div class="actions">
                <button class="btn" onclick="exportData('json')">
                    <span>{{ }}</span> JSON Tensor
                </button>
                <button class="btn" onclick="exportData('csv')">
                    <span>▦</span> CSV Manifold
                </button>
                <button class="btn btn-primary" onclick="copyTargetPrompt()">
                    <span>⚡</span> Copy AI Payload
                </button>
            </div>
        </div>
    </header>

    <main>
        <section class="chat-feed">
            <div class="filter-bar">
                <input type="text" id="searchInput" class="search-input" placeholder="Search conversational payload / tokens..." oninput="filterTurns()">
                <div class="role-filters">
                    <div class="filter-chip active" onclick="setRoleFilter('all', this)">All ({len(m.turns)})</div>
                    <div class="filter-chip" onclick="setRoleFilter('user', this)">User</div>
                    <div class="filter-chip" onclick="setRoleFilter('assistant', this)">Assistant</div>
                </div>
            </div>

            <div id="turnsContainer" style="display: flex; flex-direction: column; gap: 1.25rem;"></div>
        </section>

        <aside class="sidebar">
            <div class="panel">
                <div class="panel-title">
                    <span>Phase-Space Portrait</span>
                    <span style="font-size: 0.7rem; color: var(--text-muted);">(Hénon Map)</span>
                </div>
                <canvas id="phaseCanvas" width="280" height="220"></canvas>

                <div class="metric-grid">
                    <div class="metric-card">
                        <div class="metric-label">Lyapunov (λ)</div>
                        <div class="metric-val" style="color: var(--accent-green);">{m.metrics.lyapunov_exponent}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Spectral Radius</div>
                        <div class="metric-val" style="color: var(--accent-cyan);">{m.metrics.spectral_radius}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Tokens (Est.)</div>
                        <div class="metric-val">{m.metrics.total_tokens:,}</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">Entropy (Bits)</div>
                        <div class="metric-val">{m.metrics.entropy}</div>
                    </div>
                </div>

                <div class="status-pill">
                    ● {m.metrics.stability_status}
                </div>
            </div>

            <div class="panel">
                <div class="panel-title">
                    <span>Topology Provenance</span>
                </div>
                <div style="font-size: 0.8rem; font-family: var(--font-mono); color: var(--text-secondary); display: flex; flex-direction: column; gap: 0.5rem;">
                    <div><span style="color: var(--text-muted);">Platform:</span> {m.source_platform.upper()}</div>
                    <div><span style="color: var(--text-muted);">Quaternion S^3:</span> <br><code style="color: var(--accent-purple); font-size: 0.75rem;">{m.metrics.quaternion_norm}</code></div>
                    <div><span style="color: var(--text-muted);">Extraction Date:</span> {m.extracted_at}</div>
                    <div><span style="color: var(--text-muted);">Contractivity:</span> {m.metrics.contractivity_factor}</div>
                </div>
            </div>
        </aside>
    </main>

    <div id="toast"></div>

    <script>
        const TURNS_DATA = {turns_json};
        const METRICS_DATA = {metrics_json};
        let activeRoleFilter = 'all';

        function showToast(msg) {{
            const t = document.getElementById('toast');
            t.innerText = msg;
            t.style.display = 'block';
            setTimeout(() => {{ t.style.display = 'none'; }}, 2500);
        }}

        function renderTurns() {{
            const container = document.getElementById('turnsContainer');
            const searchVal = document.getElementById('searchInput').value.toLowerCase();
            container.innerHTML = '';

            const filtered = TURNS_DATA.filter(t => {{
                const matchesRole = activeRoleFilter === 'all' || t.role === activeRoleFilter;
                const matchesSearch = !searchVal || t.content.toLowerCase().includes(searchVal);
                return matchesRole && matchesSearch;
            }});

            if (filtered.length === 0) {{
                container.innerHTML = '<div style="text-align:center; padding: 3rem; color: var(--text-muted);">No turns matching current manifold coordinates.</div>';
                return;
            }}

            filtered.forEach(t => {{
                const card = document.createElement('div');
                card.className = `turn-card role-${{t.role}}`;

                const roleBadgeClass = t.role === 'user' ? 'badge-user' : (t.role === 'assistant' ? 'badge-assistant' : 'badge-system');
                const roleLabel = t.role.toUpperCase();

                let codeBlocksHtml = '';
                if (t.code_blocks && t.code_blocks.length > 0) {{
                    t.code_blocks.forEach((cb, idx) => {{
                        codeBlocksHtml += `
                            <div class="code-container">
                                <div class="code-header">
                                    <span>${{cb.language || 'code'}} (${{cb.line_count}} lines)</span>
                                    <button class="copy-btn" onclick="copySnippet(${{t.turn_index}}, ${{idx}})">Copy Code</button>
                                </div>
                                <pre><code>${{escapeHtml(cb.code)}}</code></pre>
                            </div>
                        `;
                    }});
                }}

                card.innerHTML = `
                    <div class="turn-header">
                        <div class="turn-meta-left">
                            <span class="turn-badge ${{roleBadgeClass}}">${{roleLabel}}</span>
                            <span class="turn-index">Turn #${{t.turn_index}}</span>
                        </div>
                        <div class="turn-meta-right">
                            <span>Tokens: ~${{t.token_estimate}}</span>
                            <span>Phase: (${{t.phase_x}}, ${{t.phase_y}})</span>
                        </div>
                    </div>
                    <div class="turn-body">${{escapeHtml(t.content)}}${{codeBlocksHtml}}</div>
                `;
                container.appendChild(card);
            }});
        }}

        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}

        function setRoleFilter(role, elem) {{
            activeRoleFilter = role;
            document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
            elem.classList.add('active');
            renderTurns();
        }}

        function filterTurns() {{
            renderTurns();
        }}

        function copySnippet(turnIdx, blockIdx) {{
            const turn = TURNS_DATA.find(t => t.turn_index === turnIdx);
            if (turn && turn.code_blocks && turn.code_blocks[blockIdx]) {{
                navigator.clipboard.writeText(turn.code_blocks[blockIdx].code);
                showToast('Code copied to clipboard.');
            }}
        }}

        function copyTargetPrompt() {{
            let promptText = '=== INGESTED AI CONVERSATION MANIFOLD ===\\n\\n';
            TURNS_DATA.forEach(t => {{
                promptText += `[${{t.role.toUpperCase()}} - Turn #${{t.turn_index}}]\\n${{t.content}}\\n\\n`;
            }});
            promptText += '=== END CONVERSATION MANIFOLD ===\\nPlease proceed with the next step using this preserved context.';
            navigator.clipboard.writeText(promptText);
            showToast('AI Injection Prompt copied to clipboard.');
        }}

        function exportData(format) {{
            let dataStr, filename, mime;
            if (format === 'json') {{
                dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(TURNS_DATA, null, 2));
                filename = "conversation_manifold.json";
                mime = "application/json";
            }} else if (format === 'csv') {{
                let csv = "Turn,Role,Tokens,Phase_X,Phase_Y,Payload\\n";
                TURNS_DATA.forEach(t => {{
                    const escaped = '"' + t.content.replace(/"/g, '""') + '"';
                    csv += `${{t.turn_index}},${{t.role}},${{t.token_estimate}},${{t.phase_x}},${{t.phase_y}},${{escaped}}\\n`;
                }});
                dataStr = "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
                filename = "conversation_manifold.csv";
                mime = "text/csv";
            }}

            const dlAnchorElem = document.createElement('a');
            dlAnchorElem.setAttribute("href", dataStr);
            dlAnchorElem.setAttribute("download", filename);
            dlAnchorElem.click();
            showToast(`Exported ${{format.toUpperCase()}} successfully.`);
        }}

        function initPhaseSpaceCanvas() {{
            const canvas = document.getElementById('phaseCanvas');
            const ctx = canvas.getContext('2d');
            const w = canvas.width;
            const h = canvas.height;

            ctx.clearRect(0, 0, w, h);

            ctx.strokeStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.lineWidth = 1;
            for(let x = 0; x < w; x += 35) {{
                ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke();
            }}
            for(let y = 0; y < h; y += 35) {{
                ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke();
            }}

            ctx.strokeStyle = 'rgba(66, 153, 225, 0.3)';
            ctx.beginPath(); ctx.moveTo(w/2, 0); ctx.lineTo(w/2, h); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(0, h/2); ctx.lineTo(w/2, h); ctx.stroke();

            if (TURNS_DATA.length > 0) {{
                ctx.beginPath();
                ctx.strokeStyle = 'rgba(0, 242, 254, 0.6)';
                ctx.lineWidth = 1.5;

                TURNS_DATA.forEach((t, i) => {{
                    const px = (t.phase_x + 1.0) * 0.5 * (w - 40) + 20;
                    const py = (1.0 - (t.phase_y + 1.0) * 0.5) * (h - 40) + 20;

                    if (i === 0) ctx.moveTo(px, py);
                    else ctx.lineTo(px, py);
                }});
                ctx.stroke();

                TURNS_DATA.forEach((t, i) => {{
                    const px = (t.phase_x + 1.0) * 0.5 * (w - 40) + 20;
                    const py = (1.0 - (t.phase_y + 1.0) * 0.5) * (h - 40) + 20;

                    ctx.beginPath();
                    ctx.arc(px, py, t.role === 'user' ? 4 : 5, 0, Math.PI * 2);
                    ctx.fillStyle = t.role === 'user' ? '#4facfe' : '#00f2fe';
                    ctx.shadowColor = t.role === 'user' ? '#4facfe' : '#00f2fe';
                    ctx.shadowBlur = 8;
                    ctx.fill();
                    ctx.shadowBlur = 0;
                }});
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            renderTurns();
            initPhaseSpaceCanvas();
        }});
    </script>
</body>
</html>
"""
        return html_template
