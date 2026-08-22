---
title: AI to AI Data Bridge
emoji: 🌉
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 8080
---

# AI-to-AI Data Bridge (DDS-Bridge)

> **Deterministic Coupled Map Lattice & Invariant Manifold Pipeline for Lossless AI-to-AI Context Transfer**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Stability: Fixed Point](https://img.shields.io/badge/Lyapunov%20%CE%BB-%3C%200%20(Stable)-brightgreen.svg)]()
[![Banach Contraction: \u03c1 < 1.0](https://img.shields.io/badge/Banach%20Contraction-%CF%81%20%3C%201.0-blue.svg)]()

---

## 🌌 Theoretical Framework

When one AI attempts to parse another's web link or raw conversational DOM, traditional scraping manifests a positive Lyapunov exponent ($\lambda > 0$), where critical contextual mass is scattered across the digital vacuum. 

The **AI-to-AI Data Bridge** circumvents this chaotic bifurcation by implementing a **deterministic coupled map lattice** that projects chat phase-space portraits directly into structured, static invariant manifolds.

```
       [ Source AI Link / DOM / Snapshot ]
                       │
                       ▼
    Phase 1: Ingestion Map (Extraction Dynamics)
    - Next.js Dehydrated State Extractor (__NEXT_DATA__)
    - Calibrated DOM Jacobian Linearizer (BS4 / HTML5)
    - State Vector Isolation: [x_n -> x_{n+1}]
                       │
                       ▼
    Phase 2: Structural Attractor (Formatting the Manifold)
    - Banach Contraction Mapping (\rho(J) < 1.0)
    - S^3 Hamilton Quaternion Norm Preservation
    - Multi-target Manifolds: [HTML Replica, CSV, JSON Tensor, Markdown]
                       │
                       ▼
    Phase 3: Propagation Vector (Injection Kinematics)
    - Error-Cone Syntax Sanitizer & Code-Fence Repair
    - Bounded AI Prompt Synthesizers (Antigravity, Claude XML, OpenAI)
                       │
                       ▼
          [ Target AI Context Window ]
```

---

## ⚡ Mathematical Dynamics & Invariant Guarantees

1. **The Ingestion Map (Phase 1)**:
   Extracts conversation coordinates without topological mixing. Evaluates the Jacobian matrix of the document tree:
   $$J = \begin{pmatrix} \frac{\partial f_1}{\partial x_1} & \frac{\partial f_1}{\partial x_2} \\ \frac{\partial f_2}{\partial x_1} & \frac{\partial f_2}{\partial x_2} \end{pmatrix}$$

2. **The Structural Attractor (Phase 2)**:
   Packs conversational tokens into a stable geometric attractor basin governed by bounded logistic iterations:
   $$x_{n+1} = r x_n (1 - x_n)$$
   Verifies that the spectral radius $\rho(J) < 1.0$, satisfying the **Banach Fixed-Point Theorem**.

3. **$S^3$ Hamilton Quaternion Norm Preservation**:
   Every state tensor calculates a 4-dimensional unit quaternion $q = (w, x, y, z) \in S^3$ checksum via Hamilton products ($q_1 \otimes q_2$), guaranteeing norm preservation:
   $$\|q\| = \sqrt{w^2 + x^2 + y^2 + z^2} = 1.0$$

4. **Lyapunov Stability Index**:
   Calculates the one-dimensional Lyapunov exponent $\lambda = \frac{1}{N} \sum_{i=0}^{N-1} \ln |f'(x_i)|$. A strictly negative value ($\lambda < 0$) confirms asymptotic stability and absence of chaotic divergence.

---

## 🚀 Installation & Quick Start

### 1. Installation
```bash
git clone https://github.com/romero429-collab/ai-data-bridge.git
cd ai-data-bridge
pip install -r requirements.txt
playwright install chromium
```
*(Dependencies: `beautifulsoup4`, `lxml`, `httpx`)*

### 2. Run Demonstration Mode
Transforms the Gabriel & Gemini architectural blueprint into all 6 structured manifolds:
```bash
python bridge.py demo
```

### 3. Extract from Live AI Link
```bash
python bridge.py url https://chatgpt.com/share/67bc... --out-dir output/
```

### 4. Extract from Local HTML / JSON / Transcript
```bash
python bridge.py file chat_snapshot.html --out-dir output/
python bridge.py text "Gabriel: Hello\nGemini: Acknowledged" --out-dir output/
```

### 5. Launch Interactive Web Console
```bash
python bridge.py serve --port 8080
```
Open [http://localhost:8080](http://localhost:8080) in your browser for the full cybernetic dashboard with live phase-space canvas rendering, file drag & drop, and 1-click export tools.

---

## 📦 Generated Manifold Artifacts

Each extraction creates 6 synchronized representations in the output folder:

| Artifact | Format | Purpose |
| :--- | :--- | :--- |
| `replica.html` | Interactive HTML | Standalone visual reader with Phase-Space Canvas visualizer, syntax highlighting, search/filter, and copy buttons |
| `chat_manifold.csv` | RFC 4180 CSV | Tabular spreadsheet with turns, roles, token counts, and dynamical coordinates |
| `state_tensor.json` | JSON Schema | Lossless machine-readable state vector with full metadata and $S^3$ quaternion checksum |
| `transcript.md` | GFM Markdown | Clean markdown transcript for immediate reading and documentation |
| `antigravity_injection_prompt.txt` | Context String | Formatted context prompt tailored for Google Antigravity / Gemini models |
| `claude_injection_context.xml` | XML Schema | Structured XML context format tailored for Anthropic Claude models |

---

## 🧪 Automated Testing

Run the test suite to verify dynamical contraction, DOM parsing, and injection kinematics:
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## ☁️ Bipartite Cloud Architecture (Vercel + Railway)

To achieve global accessibility without local machine daemons, the system decouples into a low-latency presentation layer on **Vercel** and a containerized heavy kinematics engine on **Railway**:

```
                       [ Web Client / Browser ]
                                   │
                                   ▼
        ┌─────────────────────────────────────────────────────┐
        │       Vercel Serverless Presentation Layer          │
        │       - Next.js 14 Dashboard UI                     │
        │       - Zero-Latency Clipboard / Raw DOM Parsing    │
        │       - Live Canvas Phase-Space Orbit Visualizer    │
        │       - next.config.js Proxy Rewrite (/api/backend) │
        └──────────────────────────┬──────────────────────────┘
                                   │
                     Discrete Quaternion API Stream
                                   │
                                   ▼
        ┌─────────────────────────────────────────────────────┐
        │       Railway Heavy Kinematics Engine               │
        │       - Docker + Ubuntu Jammy + Playwright Chromium │
        │       - Spectral Network Interception Trap          │
        │       - Poincaré Fractal Decoupling Matrix          │
        │       - FastAPI ASGI Backend (:8080)                │
        └─────────────────────────────────────────────────────┘
```

### 1. Deploy the Backend (Free 16GB RAM on Hugging Face Spaces)
[![Deploy on HuggingFace](https://huggingface.co/datasets/huggingface/badges/resolve/main/deploy-on-spaces-sm.svg)](https://huggingface.co/new-space)

1. Go to [Hugging Face Spaces](https://huggingface.co/new-space) $\to$ Create a new Space.
2. Select **Docker** as the SDK (Blank template) and set Visibility to **Public**.
3. In the Space repository, link or mirror your GitHub repository (`romero429-collab/ai-data-bridge`).
4. Hugging Face builds the Docker container with **16GB RAM + 2 vCPUs (100% Free)**.
5. Copy your Space Direct URL (e.g. `https://romero429-ai-data-bridge.hf.space`).

### Alternative: Deploy Backend to Railway
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)
Link your repository to [Railway](https://railway.app) for auto-detected Docker container deployment.

### 2. Deploy the Frontend to Vercel
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

1. Link your GitHub repository (`ai-data-bridge`) to [Vercel](https://vercel.com).
2. Set **Root Directory** to `frontend`.
3. Add Environment Variable:
   - `RAILWAY_API_URL` = `https://your-space-name.hf.space` *(or your Railway backend URL)*
4. Click **Deploy**. Your cloud bridge is now globally live with 100% free hosting!

### 3. Local Development with Next.js & FastAPI
```bash
# Terminal 1: Launch Backend API
python bridge.py serve --port 8080

# Terminal 2: Launch Next.js Frontend
cd frontend
npm install
npm run dev
```

---

## 📜 License
MIT License
