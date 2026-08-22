"""
Phase 1: The Ingestion Map (Extraction Dynamics) - V4
(Spectral Network Interception + Playwright Hydration + Fractal Decoupling)
Extracts conversation turns from live AI share links via Headless Chromium,
intercepts raw XHR JSON payloads to bypass UI obfuscation, and decouples nested strange attractors.
"""

from __future__ import annotations
import re
import json
import uuid
from typing import List, Optional, Tuple, Dict, Any
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup, Tag

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from .models import ChatTurn, CodeSnippet, ConversationManifold, PhaseSpaceMetrics
from .dynamics import DynamicalSystemEngine


class ConversationExtractor:
    """
    DOM, Spectral JSON Interception, and Headless Browser Extraction Engine.
    """

    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout
        self.dynamics = DynamicalSystemEngine()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

    def _fetch_spectral_network(self, url: str) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Antigravity Kinematic Network Interception Map.
        Spoofs human interaction, intercepts JSON XHR arrays, and extracts hydrated DOM.
        """
        captured_json = []
        html_content = ""

        if not PLAYWRIGHT_AVAILABLE:
            print("[DDS-Bridge] Playwright not installed. Network interception disabled.")
            return "", []

        def intercept_response(response):
            try:
                if response.status == 200 and response.request.resource_type in ["fetch", "xhr"]:
                    url_lower = response.url.lower()
                    if any(k in url_lower for k in [
                        "backend-api", "api/chat", "graphql", "share", "conversation",
                        "response", "messages", "query_stream", "get_chat", "grok"
                    ]):
                        content_type = response.headers.get("content-type", "")
                        if "application/json" in content_type or "text" in content_type:
                            data = response.json()
                            if isinstance(data, (dict, list)):
                                captured_json.append(data)
                                print(f"[DDS-Bridge] Spectral XHR isolated from trajectory: {response.url[:70]}...")
            except Exception:
                pass

        try:
            print(f"[DDS-Bridge] Instantiating Headless Chromium for Spectral Interception: {url}")
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--disable-infobars",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--window-size=1280,900"
                    ]
                )
                context = browser.new_context(
                    user_agent=self.headers["User-Agent"],
                    viewport={"width": 1280, "height": 900}
                )
                
                # Universal provider matrix stealth injection
                context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                
                page = context.new_page()
                page.on("response", intercept_response)
                
                page.goto(url, wait_until="domcontentloaded", timeout=int(self.timeout * 1000))
                
                # Execute kinematic scroll sweep to force full history hydration
                last_height = 0
                for _ in range(12):
                    page.mouse.wheel(0, 5000)
                    page.wait_for_timeout(800)
                    new_height = page.evaluate("document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                for _ in range(8):
                    page.mouse.wheel(0, -8000)
                    page.wait_for_timeout(300)
                    if page.evaluate("window.scrollY") <= 0:
                        break
                
                # Final delay to let isolated periodic orbits resolve
                page.wait_for_timeout(2000)
                html_content = page.content()
                browser.close()
                print(f"[DDS-Bridge] Traversal complete. Captured {len(captured_json)} spectral JSON payloads.")
        except Exception as e:
            print(f"[DDS-Bridge] Playwright interception bounded by error cone: {e}")

        return html_content, captured_json

    def identify_platform(self, source: str) -> str:
        low = source.lower()
        if "chatgpt.com" in low or "openai.com" in low: return "chatgpt"
        elif "claude.ai" in low or "anthropic" in low: return "claude"
        elif "gemini.google.com" in low or "google.com/gemini" in low or "bard.google.com" in low: return "gemini"
        elif "perplexity.ai" in low: return "perplexity"
        elif "poe.com" in low: return "poe"
        elif "grok" in low or "x.ai" in low: return "grok"
        return "generic"

    def extract_from_url(self, url: str) -> ConversationManifold:
        platform = self.identify_platform(url)
        
        # 1. Kinematic Network Interception
        html_content, json_payloads = self._fetch_spectral_network(url)
        
        # Static HTTP Fallback if Playwright fails
        if not html_content:
            try:
                with httpx.Client(headers=self.headers, timeout=self.timeout, follow_redirects=True) as client:
                    response = client.get(url)
                    response.raise_for_status()
                    html_content = response.text
            except httpx.HTTPError as e:
                raise RuntimeError(f"Ingestion Network Error: Failed to fetch {url} -> {str(e)}")

        # 2. Attempt to construct invariant manifold from pure spectral JSON (Bypasses DOM entirely)
        for payload in json_payloads:
            try:
                manifold = self.extract_from_json(payload)
                if len(manifold.turns) > 1:
                    manifold.source_platform = platform
                    manifold.source_url = url
                    manifold.title = manifold.title if manifold.title != "Imported JSON Conversation" else f"{platform.upper()} Extracted Session"
                    print(f"[DDS-Bridge] Successfully constructed {len(manifold.turns)} turns from Spectral JSON.")
                    return manifold
            except Exception:
                continue

        # 3. Fallback to extracting from the hydrated DOM
        print("[DDS-Bridge] Spectral JSON yielded no direct turns. Reverting to hydrated DOM extraction.")
        return self.extract_from_html(html_content, source_platform=platform, source_url=url)

    def extract_from_html(self, html_content: str, source_platform: str = "generic", source_url: Optional[str] = None) -> ConversationManifold:
        dehydrated_turns, title = self._extract_dehydrated_json(html_content)
        if dehydrated_turns:
            return self._build_manifold(self._collapse_redundant_files(dehydrated_turns), title or "Extracted AI Conversation", source_platform, source_url)

        soup = BeautifulSoup(html_content, "html.parser")
        extracted_title = ""
        if soup.title and soup.title.string:
            extracted_title = soup.title.string.strip()
        h1 = soup.find("h1")
        if h1 and not extracted_title:
            extracted_title = h1.get_text(strip=True)
        if not extracted_title:
            extracted_title = "Extracted AI Conversation"

        extracted_title = re.sub(r"\s*\|\s*(ChatGPT|Claude|Gemini|Perplexity|Grok).*", "", extracted_title, flags=re.IGNORECASE)

        turns: List[ChatTurn] = []
        if source_platform == "chatgpt": turns = self._parse_chatgpt_dom(soup)
        elif source_platform == "claude": turns = self._parse_claude_dom(soup)
        elif source_platform == "gemini": turns = self._parse_gemini_dom(soup)
        elif source_platform == "perplexity": turns = self._parse_perplexity_dom(soup)

        if not turns: turns = self._parse_generic_dom(soup)
        if not turns:
            raw_text = soup.get_text(separator="\n", strip=True)
            turns = self._parse_transcript_text(raw_text)

        return self._build_manifold(self._collapse_redundant_files(turns), extracted_title, source_platform, source_url)

    def extract_from_text(self, text: str, title: str = "Imported Transcript") -> ConversationManifold:
        turns = self._parse_transcript_text(text)
        return self._build_manifold(self._collapse_redundant_files(turns), title, "text_transcript", None)

    def extract_from_json(self, json_data: Any) -> ConversationManifold:
        if isinstance(json_data, str): json_data = json.loads(json_data)
        if isinstance(json_data, dict) and "turns" in json_data: return ConversationManifold.from_dict(json_data)

        turns = []
        raw_turns = json_data if isinstance(json_data, list) else json_data.get("messages", json_data.get("conversation", []))
        
        # Fallback for GraphQL / Relay / Nested structures
        if not raw_turns and isinstance(json_data, dict):
            # Check mapping dict (ChatGPT / Grok)
            mapping = json_data.get("mapping") or json_data.get("serverResponse", {}).get("data", {}).get("mapping")
            if mapping and isinstance(mapping, dict):
                ordered = []
                for node_id, node in mapping.items():
                    msg = node.get("message")
                    if msg and msg.get("content"):
                        role = msg.get("author", {}).get("role", "assistant")
                        parts = msg.get("content", {}).get("parts", [])
                        content = "\n".join(str(p) for p in parts if isinstance(p, str))
                        if role in ["user", "assistant", "system"] and content.strip():
                            create_time = msg.get("create_time") or 0
                            ordered.append((create_time, role, content, msg.get("metadata", {}).get("model_slug")))
                ordered.sort(key=lambda x: x[0])
                for _, role, content, model in ordered:
                    nested = self._untangle_fractal_super_node(content, role, len(turns) + 1)
                    for nt in nested:
                        if not nt.model and model: nt.model = model
                    turns.extend(nested)
                if turns:
                    return self._build_manifold(self._collapse_redundant_files(turns), "Imported JSON Mapping", "json_import", None)

            raw_str = json.dumps(json_data)
            if "content" in raw_str and ("user" in raw_str.lower() or "assistant" in raw_str.lower()):
                return self.extract_from_text(raw_str, title="Raw JSON Dump")
        
        for i, item in enumerate(raw_turns):
            if isinstance(item, dict):
                role = item.get("role", item.get("speaker", item.get("author", "user")))
                content = item.get("content", item.get("text", item.get("payload", item.get("message", ""))))
                if isinstance(content, list):
                    parts = []
                    for p in content:
                        if isinstance(p, str): parts.append(p)
                        elif isinstance(p, dict) and "text" in p: parts.append(p["text"])
                    content = "\n".join(parts)
                elif isinstance(content, dict):
                    content = json.dumps(content)

                if content and isinstance(content, str):
                    nested = self._untangle_fractal_super_node(content, role.lower(), len(turns) + 1)
                    turns.extend(nested)

        return self._build_manifold(self._collapse_redundant_files(turns), "Imported JSON Conversation", "json_import", None)

    def _extract_dehydrated_json(self, html: str) -> Tuple[List[ChatTurn], Optional[str]]:
        try:
            match = re.search(r'<script id="__NEXT_DATA__" type="application/json">({.*?})</script>', html, re.DOTALL)
            if match:
                data = json.loads(match.group(1))
                page_props = data.get("props", {}).get("pageProps", {})
                title = page_props.get("title")

                shared_conv = page_props.get("serverResponse", {}).get("data", {}) or page_props.get("sharedConversation", {})
                if not shared_conv and "linear_conversation" in page_props:
                    shared_conv = page_props

                turns: List[ChatTurn] = []
                linear = shared_conv.get("linear_conversation", [])
                if linear:
                    for node in linear:
                        role = node.get("message", {}).get("author", {}).get("role", "assistant")
                        parts = node.get("message", {}).get("content", {}).get("parts", [])
                        content = "\n".join(str(p) for p in parts if isinstance(p, str))
                        if content:
                            nested_turns = self._untangle_fractal_super_node(content, role, len(turns) + 1)
                            turns.extend(nested_turns)
                    if turns: return turns, title

                mapping = shared_conv.get("mapping", {})
                if mapping:
                    ordered_nodes = []
                    for node_id, node in mapping.items():
                        msg = node.get("message")
                        if msg and msg.get("content"):
                            role = msg.get("author", {}).get("role")
                            parts = msg.get("content", {}).get("parts", [])
                            content = "\n".join(str(p) for p in parts if isinstance(p, str))
                            if role in ["user", "assistant", "system"] and content:
                                create_time = msg.get("create_time")
                                ordered_nodes.append((create_time or 0, role, content, msg.get("metadata", {}).get("model_slug")))

                    ordered_nodes.sort(key=lambda x: x[0])
                    for _, role, content, model in ordered_nodes:
                        nested_turns = self._untangle_fractal_super_node(content, role, len(turns) + 1)
                        for nt in nested_turns:
                            if not nt.model: nt.model = model
                        turns.extend(nested_turns)
                    if turns: return turns, title
        except Exception:
            pass
        return [], None

    def _untangle_fractal_super_node(self, raw_text: str, base_role: str, start_index: int) -> List[ChatTurn]:
        pattern = r"(?:^|\n)[ \t]*(?:\*\*)?(Gabriel|Gemini|Anise|Grok|Copilot|You|User|Assistant|System)(?:\*\*)?\s*[:\n]\s*"
        splits = re.split(pattern, raw_text, flags=re.IGNORECASE)
        
        if len(splits) < 3:
            return [ChatTurn(
                turn_index=start_index,
                role=base_role,
                content=raw_text.strip(),
                code_blocks=self._extract_code_blocks(raw_text)
            )]
            
        untangled_turns = []
        i = 1
        current_index = start_index
        
        while i < len(splits) - 1:
            speaker = splits[i].strip()
            content = splits[i+1].strip()
            
            low_s = speaker.lower()
            if low_s in ["gabriel", "user", "you"]: role = "user"
            elif low_s in ["gemini", "anise", "grok", "copilot", "assistant"]: role = "assistant"
            else: role = "user" if len(untangled_turns) % 2 == 0 else "assistant"
                
            if content:
                untangled_turns.append(ChatTurn(
                    turn_index=current_index,
                    role=role,
                    content=content,
                    code_blocks=self._extract_code_blocks(content),
                    model=speaker if low_s not in ["user", "you", "gabriel"] else None
                ))
                current_index += 1
            i += 2
            
        return untangled_turns

    def _collapse_redundant_files(self, turns: List[ChatTurn]) -> List[ChatTurn]:
        if not turns: return []
        collapsed = []
        file_pattern = r"^Uploaded a file\s*(Gabriel:)?\s*$"
        
        for turn in turns:
            if re.match(file_pattern, turn.content.strip(), re.IGNORECASE):
                if collapsed and collapsed[-1].role == turn.role and re.match(file_pattern, collapsed[-1].content.strip(), re.IGNORECASE):
                    continue
            if collapsed and collapsed[-1].role == turn.role and re.match(file_pattern, collapsed[-1].content.strip(), re.IGNORECASE):
                turn.content = f"[Attached files processed]\n\n{turn.content}"
                collapsed.pop()
            collapsed.append(turn)

        for i, t in enumerate(collapsed):
            t.turn_index = i + 1
        return collapsed

    def _parse_chatgpt_dom(self, soup: BeautifulSoup) -> List[ChatTurn]:
        turns = []
        articles = soup.find_all("article")
        if not articles: articles = soup.find_all("div", attrs={"data-message-author-role": True})

        for i, article in enumerate(articles):
            role = article.get("data-message-author-role")
            if not role:
                if article.find(attrs={"data-message-author-role": "user"}): role = "user"
                elif article.find(attrs={"data-message-author-role": "assistant"}): role = "assistant"
                else: role = "user" if i % 2 == 0 else "assistant"

            content_div = article.find("div", class_=lambda c: c and "markdown" in c) or article
            text = content_div.get_text(separator="\n", strip=True)
            soup_codes = self._extract_code_blocks_from_soup(content_div)
            if text:
                nested_turns = self._untangle_fractal_super_node(text, role, len(turns) + 1)
                if soup_codes:
                    for nt in nested_turns:
                        if not nt.code_blocks: nt.code_blocks = soup_codes
                turns.extend(nested_turns)
        return turns

    def _parse_claude_dom(self, soup: BeautifulSoup) -> List[ChatTurn]:
        turns = []
        msg_elements = soup.find_all("div", attrs={"data-testid": ["user-message", "claude-message"]}) or \
                       soup.find_all("div", class_=lambda c: c and ("font-claude-message" in c or "font-user-message" in c))
        for i, elem in enumerate(msg_elements):
            testid = elem.get("data-testid", "")
            role = "user" if "user" in testid or "user" in elem.get("class", []) else "assistant"
            text = elem.get_text(separator="\n", strip=True)
            soup_codes = self._extract_code_blocks_from_soup(elem)
            if text:
                nested_turns = self._untangle_fractal_super_node(text, role, len(turns) + 1)
                if soup_codes:
                    for nt in nested_turns:
                        if not nt.code_blocks: nt.code_blocks = soup_codes
                turns.extend(nested_turns)
        return turns

    def _parse_gemini_dom(self, soup: BeautifulSoup) -> List[ChatTurn]:
        turns = []
        blocks = soup.find_all(["user-query", "model-response"]) or \
                 soup.find_all("div", class_=lambda c: c and ("query-content" in c or "response-content" in c or "chat-turn" in c))
        for i, block in enumerate(blocks):
            tag_name = block.name.lower()
            classes = " ".join(block.get("class", []))
            if tag_name == "user-query" or "query" in classes or "user" in classes: role = "user"
            else: role = "assistant"
            text = block.get_text(separator="\n", strip=True)
            soup_codes = self._extract_code_blocks_from_soup(block)
            if text:
                nested_turns = self._untangle_fractal_super_node(text, role, len(turns) + 1)
                if soup_codes:
                    for nt in nested_turns:
                        if not nt.code_blocks: nt.code_blocks = soup_codes
                turns.extend(nested_turns)
        return turns

    def _parse_perplexity_dom(self, soup: BeautifulSoup) -> List[ChatTurn]:
        turns = []
        containers = soup.find_all("div", class_=lambda c: c and ("wrapper" in c or "query" in c or "answer" in c))
        for c in containers:
            text = c.get_text(separator="\n", strip=True)
            if text and len(text) > 10:
                role = "user" if len(turns) % 2 == 0 else "assistant"
                nested_turns = self._untangle_fractal_super_node(text, role, len(turns) + 1)
                turns.extend(nested_turns)
        return turns

    def _parse_generic_dom(self, soup: BeautifulSoup) -> List[ChatTurn]:
        turns = []
        for unwanted in soup(["script", "style", "nav", "footer", "header", "noscript"]):
            unwanted.decompose()
        candidates = soup.find_all(["div", "section", "article", "li"], class_=lambda c: c and any(
            k in str(c).lower() for k in ["message", "chat", "turn", "bubble", "prompt", "response", "dialogue", "speech"]
        ))
        for elem in candidates:
            if elem.find_parent(lambda p: p in candidates): continue
            text = elem.get_text(separator="\n", strip=True)
            if not text or len(text) < 3: continue
            elem_classes = " ".join(elem.get("class", []))
            role = "assistant"
            if any(u in elem_classes.lower() for u in ["user", "human", "prompt", "client", "sender"]): role = "user"
            elif any(a in elem_classes.lower() for u in ["assistant", "ai", "bot", "model", "response"]): role = "assistant"
            else: role = "user" if len(turns) % 2 == 0 else "assistant"
            nested_turns = self._untangle_fractal_super_node(text, role, len(turns) + 1)
            turns.extend(nested_turns)
        return turns

    def _parse_transcript_text(self, text: str) -> List[ChatTurn]:
        return self._untangle_fractal_super_node(text, "user", 1)

    def _extract_code_blocks_from_soup(self, soup_elem: Tag) -> List[CodeSnippet]:
        snippets = []
        for pre in soup_elem.find_all("pre"):
            code_elem = pre.find("code") or pre
            code_text = code_elem.get_text()
            if not code_text.strip(): continue
            lang = "text"
            classes = code_elem.get("class", [])
            for c in classes:
                if c.startswith("language-") or c.startswith("lang-"):
                    lang = c.replace("language-", "").replace("lang-", "")
                    break
            snippets.append(CodeSnippet(language=lang, code=code_text, line_count=len(code_text.splitlines())))
        return snippets

    def _extract_code_blocks(self, text: str) -> List[CodeSnippet]:
        snippets = []
        pattern = r"```([a-zA-Z0-9_\-\+]*)\n(.*?)```"
        matches = re.finditer(pattern, text, re.DOTALL)
        for m in matches:
            lang = m.group(1).strip() or "text"
            code = m.group(2)
            snippets.append(CodeSnippet(language=lang, code=code, line_count=len(code.splitlines())))
        return snippets

    def _build_manifold(self, turns: List[ChatTurn], title: str, source_platform: str, source_url: Optional[str]) -> ConversationManifold:
        self.dynamics.compute_turn_phase_coordinates(turns)
        metrics = self.dynamics.calculate_metrics(turns)
        manifold_id = f"manifold_{uuid.uuid4().hex[:8]}"

        return ConversationManifold(
            id=manifold_id,
            title=title,
            source_platform=source_platform,
            source_url=source_url,
            turns=turns,
            metrics=metrics,
            metadata={
                "parser_engine": "DDS-Bridge v4.0 (Spectral JSON Intercept + Playwright Hydration + Fractal Decoupling)",
                "phase_space_dimension": 2,
                "hamilton_quaternion_normalized": True
            }
        )
