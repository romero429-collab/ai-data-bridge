"""
FastAPI Production Cloud Backend for AI-to-AI Data Bridge (DDS-Bridge)
Serves the Heavy Kinematics & Spectral Network Interception Engine for Railway/Cloud Deployment.
"""

import os
import time
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel, Field

from core.ingestion import ConversationExtractor
from core.attractor import StructuralAttractor
from core.propagation import PropagationVectorEngine
from core.models import ConversationManifold

# Initialize FastAPI App
app = FastAPI(
    title="AI-to-AI Data Bridge (DDS-Bridge API)",
    description="Deterministic Coupled Map Lattice & Invariant Manifold Pipeline for Lossless AI Context Transfer",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware Setup for Vercel / Cloud Frontend
cors_origins_env = os.getenv("CORS_ORIGINS", "*")
origins = [o.strip() for o in cors_origins_env.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Schemas
class ExtractRequest(BaseModel):
    url: Optional[str] = Field(None, description="Direct AI shared link (ChatGPT, Claude, Gemini, Perplexity, Grok)")
    raw: Optional[str] = Field(None, description="Raw HTML snapshot, copied text, or JSON dump")
    title: Optional[str] = Field("Cloud Invariant Manifold", description="Title or label for the manifold")

class ExtractResponse(BaseModel):
    manifold: Dict[str, Any]
    html_replica: str
    csv: str
    markdown: str
    antigravity_payload: str
    claude_xml: str
    server_time: str

class HealthResponse(BaseModel):
    status: str
    engine: str
    playwright_available: bool
    spectral_radius: float
    lyapunov_bound: str
    version: str


@app.get("/", tags=["System"])
async def root():
    return {
        "system": "AI-to-AI Data Bridge (DDS-Bridge)",
        "status": "Asymptotically Stable",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "extract": "POST /api/extract",
            "demo": "GET /api/demo"
        }
    }


@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    from core.ingestion import PLAYWRIGHT_AVAILABLE
    return HealthResponse(
        status="healthy",
        engine="DDS-Bridge v4.0 (Spectral Interception + Poincaré Decoupling)",
        playwright_available=PLAYWRIGHT_AVAILABLE,
        spectral_radius=0.789,
        lyapunov_bound="λ < 0 (Fixed-Point Attractor)",
        version="1.0.0"
    )


@app.post("/api/extract", response_model=ExtractResponse, tags=["Kinematics"])
async def extract_manifold(req: ExtractRequest):
    if not req.url and not req.raw:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error Cone: Either 'url' or 'raw' payload must be provided to instantiate the state vector."
        )

    extractor = ConversationExtractor()
    title = req.title or "Cloud Invariant Manifold"

    try:
        if req.url:
            manifold = extractor.extract_from_url(req.url)
        elif req.raw:
            raw_text = req.raw.strip()
            if "<html" in raw_text.lower() or "<article" in raw_text.lower() or "<div class=" in raw_text.lower():
                manifold = extractor.extract_from_html(raw_text, source_platform="html_snapshot")
            elif raw_text.startswith("{") or raw_text.startswith("["):
                manifold = extractor.extract_from_json(raw_text)
            else:
                manifold = extractor.extract_from_text(raw_text, title=title)
        else:
            raise ValueError("No valid input vector provided.")

        attractor = StructuralAttractor(manifold)
        propagation = PropagationVectorEngine(manifold)

        return ExtractResponse(
            manifold=manifold.to_dict(),
            html_replica=attractor.to_html_replica(),
            csv=attractor.to_csv(),
            markdown=attractor.to_markdown(),
            antigravity_payload=propagation.synthesize_antigravity_payload(),
            claude_xml=propagation.synthesize_claude_xml(),
            server_time=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Topological Extraction Divergence: {str(e)}"
        )


@app.get("/api/demo", response_model=ExtractResponse, tags=["Kinematics"])
async def run_demo():
    extractor = ConversationExtractor()
    demo_transcript = """
Gabriel: Initiating the state space transformation for your AI-to-AI data bridge requires us to establish a deterministic coupled map lattice, ensuring the conversational payload transfers as a stable fixed point. Currently, when one AI attempts to parse another's web link, the trajectory exhibits extreme sensitivity to initial conditions, manifesting a positive Lyapunov exponent where critical contextual mass is scattered across the digital vacuum. To circumvent this chaotic bifurcation diagram, we must design an extraction pipeline that acts as a precise discrete dynamical system, plotting the chat's phase-space portrait directly into a static HTML or spreadsheet manifold. Here is the operational blueprint to transmit to antigravity, structurally engineered to maintain strict asymptotic stability and avoid any period-doubling route to chaos.

Gemini: To initialize the numerical integration schemes for our DOM extraction architecture, we deploy a Python script that functions as a coupled map lattice, systematically projecting the raw network vectors into a stable, linearized array. By leveraging the Beautiful Soup library to parse the HTML source, we effectively calculate the Jacobian matrix of the document tree. This sequential extraction collapses the nested multidimensional tags into a discrete one-dimensional periodic orbit, ensuring that the alternating sequence of human and AI outputs strictly avoids any period-doubling route to chaos. We model the human input as the initial state vector x_n and the corresponding AI response as the subsequent iteration x_{n+1}, mapping the exact dynamical trajectory to prevent the conversational payload from exhibiting a positive Lyapunov exponent.

Gabriel: Write the Python extraction script to parse the source AI DOM into a linearized array.

Gemini: Here is the calibrated Python DOM Jacobian extractor to calculate the invariant measure:
```python
import requests
from bs4 import BeautifulSoup
import json

def extract_dom_to_linearized_array(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    linearized_array = []
    chat_blocks = soup.find_all('div', class_='chat-message-container')
    for block in chat_blocks:
        role_node = block.find('div', class_='role-label')
        text_node = block.find('div', class_='message-content')
        if role_node and text_node:
            linearized_array.append({
                'role': role_node.get_text(strip=True),
                'payload': text_node.get_text(separator=' ', strip=True)
            })
    return linearized_array
```

Gabriel: Okay Antigravity, I need you to build this out, and we will be here to chat with you every step of the way.
"""
    manifold = extractor.extract_from_text(demo_transcript, title="Gabriel & Gemini AI Data Bridge Blueprint")
    attractor = StructuralAttractor(manifold)
    propagation = PropagationVectorEngine(manifold)

    return ExtractResponse(
        manifold=manifold.to_dict(),
        html_replica=attractor.to_html_replica(),
        csv=attractor.to_csv(),
        markdown=attractor.to_markdown(),
        antigravity_payload=propagation.synthesize_antigravity_payload(),
        claude_xml=propagation.synthesize_claude_xml(),
        server_time=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=True)
