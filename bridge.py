#!/usr/bin/env python3
"""
AI-to-AI Data Bridge CLI (DDS-Bridge)
Deterministic Coupled Map Lattice & Invariant Manifold Pipeline
"""

import sys
import os
import argparse
from pathlib import Path

# Enable UTF-8 for console output on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

from core.ingestion import ConversationExtractor
from core.attractor import StructuralAttractor
from core.propagation import PropagationVectorEngine
from core.server import start_server


def export_all_manifolds(manifold, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    attractor = StructuralAttractor(manifold)
    propagation = PropagationVectorEngine(manifold)

    # 1. HTML Replica
    html_file = out_dir / "replica.html"
    html_file.write_text(attractor.to_html_replica(), encoding="utf-8")

    # 2. CSV Spreadsheet
    csv_file = out_dir / "chat_manifold.csv"
    csv_file.write_text(attractor.to_csv(), encoding="utf-8")

    # 3. JSON State Tensor
    json_file = out_dir / "state_tensor.json"
    json_file.write_text(attractor.to_json(), encoding="utf-8")

    # 4. Markdown Transcript
    md_file = out_dir / "transcript.md"
    md_file.write_text(attractor.to_markdown(), encoding="utf-8")

    # 5. Antigravity AI Injection Payload
    prompt_file = out_dir / "antigravity_injection_prompt.txt"
    prompt_file.write_text(propagation.synthesize_antigravity_payload(), encoding="utf-8")

    # 6. Claude XML Injection Payload
    claude_file = out_dir / "claude_injection_context.xml"
    claude_file.write_text(propagation.synthesize_claude_xml(), encoding="utf-8")

    print("\n" + "="*70)
    print(f"  [*] INVARIANT MANIFOLD TRANSFORMATION COMPLETE")
    print("="*70)
    print(f"  • Title:             {manifold.title}")
    print(f"  • Source Platform:   {manifold.source_platform.upper()}")
    print(f"  • Total Turns (n):   {len(manifold.turns)}")
    print(f"  • Estimated Tokens:  {manifold.metrics.total_tokens:,}")
    print(f"  • Lyapunov Stability: λ = {manifold.metrics.lyapunov_exponent} (Fixed-Point Attractor)")
    print(f"  • Spectral Radius:   ρ = {manifold.metrics.spectral_radius} (< 1.0 Banach Contraction)")
    print(f"  • S^3 Quaternion:    {manifold.metrics.quaternion_norm}")
    print("-"*70)
    print(f"  Output Artifacts saved in: {out_dir.resolve()}")
    print(f"    1. [HTML Replica]:       {html_file.name}")
    print(f"    2. [CSV Spreadsheet]:    {csv_file.name}")
    print(f"    3. [JSON State Tensor]:  {json_file.name}")
    print(f"    4. [Markdown Summary]:   {md_file.name}")
    print(f"    5. [AI Injection Prompt]:{prompt_file.name}")
    print(f"    6. [Claude XML Context]: {claude_file.name}")
    print("="*70 + "\n")


def cmd_url(args):
    extractor = ConversationExtractor()
    print(f"[DDS-Bridge] Ingesting URL: {args.url}")
    manifold = extractor.extract_from_url(args.url)
    out_dir = Path(args.out_dir)
    export_all_manifolds(manifold, out_dir)


def cmd_file(args):
    extractor = ConversationExtractor()
    path = Path(args.file)
    if not path.exists():
        print(f"Error: File not found: {path}")
        sys.exit(1)
    
    content = path.read_text(encoding="utf-8")
    ext = path.suffix.lower()
    
    print(f"[DDS-Bridge] Ingesting file: {path.name} (type: {ext})")
    if ext in [".html", ".htm"]:
        manifold = extractor.extract_from_html(content, source_platform=extractor.identify_platform(content))
    elif ext == ".json":
        manifold = extractor.extract_from_json(content)
    else:
        manifold = extractor.extract_from_text(content, title=path.stem)

    out_dir = Path(args.out_dir)
    export_all_manifolds(manifold, out_dir)


def cmd_text(args):
    extractor = ConversationExtractor()
    print(f"[DDS-Bridge] Ingesting raw conversational transcript...")
    manifold = extractor.extract_from_text(args.text, title=args.title or "Text Conversation Manifold")
    out_dir = Path(args.out_dir)
    export_all_manifolds(manifold, out_dir)


def cmd_demo(args):
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
    print("[DDS-Bridge] Running deterministic coupled map lattice simulation on Gabriel & Gemini Blueprint...")
    manifold = extractor.extract_from_text(demo_transcript, title="Gabriel & Gemini AI Data Bridge Blueprint")
    out_dir = Path(args.out_dir)
    export_all_manifolds(manifold, out_dir)


def cmd_serve(args):
    start_server(port=args.port)


def main():
    parser = argparse.ArgumentParser(description="AI-to-AI Data Bridge (Deterministic Coupled Map Lattice)")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    p_url = subparsers.add_parser("url", help="Extract manifold from live AI share URL")
    p_url.add_argument("url", help="Target URL (ChatGPT, Claude, Gemini, Perplexity share link)")
    p_url.add_argument("--out-dir", default="output", help="Output directory (default: output)")

    p_file = subparsers.add_parser("file", help="Extract manifold from local HTML, JSON, or text file")
    p_file.add_argument("file", help="Path to input file")
    p_file.add_argument("--out-dir", default="output", help="Output directory (default: output)")

    p_text = subparsers.add_parser("text", help="Extract manifold from raw text dialogue transcript")
    p_text.add_argument("text", help="Conversational text string")
    p_text.add_argument("--title", default=None, help="Title of conversation")
    p_text.add_argument("--out-dir", default="output", help="Output directory (default: output)")

    p_demo = subparsers.add_parser("demo", help="Run full blueprint demo and generate all output artifacts")
    p_demo.add_argument("--out-dir", default="output", help="Output directory (default: output)")

    p_serve = subparsers.add_parser("serve", help="Launch local interactive Web Dashboard")
    p_serve.add_argument("--port", type=int, default=8080, help="Web server port (default: 8080)")

    args = parser.parse_args()

    if args.command == "url":
        cmd_url(args)
    elif args.command == "file":
        cmd_file(args)
    elif args.command == "text":
        cmd_text(args)
    elif args.command == "demo":
        cmd_demo(args)
    elif args.command == "serve":
        cmd_serve(args)
    else:
        print("No command provided. Running demonstration mode...\n")
        class DefaultArgs:
            out_dir = "output"
        cmd_demo(DefaultArgs())


if __name__ == "__main__":
    main()
