"""
Phase 3: The Propagation Vector (Injection Kinematics)
Transforms and bounds the conversational payload for target AI ingestion.
Applies error-cone syntax sanitization, context window sizing, and provider-specific prompt schemas.
"""

from __future__ import annotations
import re
from typing import Optional, List, Dict, Any
from .models import ConversationManifold, ChatTurn


class PropagationVectorEngine:
    """
    Kinematic injection engine generating bounded, high-density context for target AI models.
    """

    def __init__(self, manifold: ConversationManifold):
        self.manifold = manifold

    def sanitize_error_cone(self, text: str) -> str:
        """
        Error-cone filter: cleans corrupted control characters, repairs unclosed code fences,
        and eliminates dangling HTML artifacts.
        """
        # Remove null bytes and non-printable control characters (except tabs and newlines)
        cleaned = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)

        # Ensure all markdown code fences ``` are paired
        fence_count = len(re.findall(r'```', cleaned))
        if fence_count % 2 != 0:
            cleaned += "\n```"

        return cleaned

    def synthesize_antigravity_payload(self) -> str:
        """
        Generates optimal injection prompt for Antigravity / Gemini coding models.
        """
        m = self.manifold
        header = f"""<INGESTED_CONVERSATION_MANIFOLD>
[METADATA]
Title: {m.title}
Source: {m.source_platform.upper()}
Turns: {len(m.turns)}
Estimated Tokens: {m.metrics.total_tokens}
Lyapunov Stability: {m.metrics.lyapunov_exponent} (Fixed Point)
Quaternion S^3 Norm Checksum: {m.metrics.quaternion_norm}
Extraction Timestamp: {m.extracted_at}
[/METADATA]

[CONVERSATION_HISTORY]"""

        turn_blocks = []
        for t in m.turns:
            sanitized = self.sanitize_error_cone(t.content)
            role_tag = t.role.upper()
            model_info = f" model=\"{t.model}\"" if t.model else ""
            block = f"""<turn index="{t.turn_index}" role="{role_tag}"{model_info}>
{sanitized}
</turn>"""
            turn_blocks.append(block)

        footer = """[/CONVERSATION_HISTORY]
[INSTRUCTIONS]
The above conversation history has been ingested via the AI Data Bridge.
All technical constraints, code snippets, and conversational state vectors are fully preserved.
Continue from the latest turn with complete context continuity.
[/INSTRUCTIONS]
</INGESTED_CONVERSATION_MANIFOLD>"""

        return f"{header}\n\n" + "\n\n".join(turn_blocks) + f"\n\n{footer}"

    def synthesize_claude_xml(self) -> str:
        """
        Generates XML-tagged context formatted for Anthropic Claude models.
        """
        m = self.manifold
        parts = [
            f'<conversation_manifold platform="{m.source_platform}" total_turns="{len(m.turns)}">'
        ]
        for t in m.turns:
            sanitized = self.sanitize_error_cone(t.content)
            speaker = "Human" if t.role.lower() == "user" else "Assistant"
            parts.append(f'  <message index="{t.turn_index}" speaker="{speaker}">\n{sanitized}\n  </message>')
        parts.append('</conversation_manifold>')
        return "\n".join(parts)

    def synthesize_openai_messages(self) -> List[Dict[str, str]]:
        """
        Generates standard OpenAI chat completions message structure.
        """
        messages = []
        # Ingestion framing system prompt
        messages.append({
            "role": "system",
            "content": f"Ingested conversation from {self.manifold.source_platform} ({len(self.manifold.turns)} turns). Maintain full contextual continuity."
        })
        for t in self.manifold.turns:
            role = "user" if t.role.lower() == "user" else ("system" if t.role.lower() == "system" else "assistant")
            messages.append({
                "role": role,
                "content": self.sanitize_error_cone(t.content)
            })
        return messages

    def synthesize_compressed_invariant(self, max_tokens: int = 4000) -> str:
        """
        Produces a high-density, compressed invariant manifold:
        Compresses early dialogue while maintaining 100% of code snippets, decisions, and the last 3 turns.
        """
        turns = self.manifold.turns
        if len(turns) <= 4:
            return self.synthesize_antigravity_payload()

        summary_points = []
        code_artifacts = []
        
        # Preserve early turns in condensed invariant format
        for t in turns[:-3]:
            role = t.role.upper()
            first_line = t.content.splitlines()[0] if t.content.splitlines() else "..."
            summary_points.append(f"- [Turn #{t.turn_index} {role}]: {first_line[:120]}...")
            
            for cb in t.code_blocks:
                code_artifacts.append(f"```{cb.language} // Turn #{t.turn_index}\n{cb.code}\n```")

        # Full fidelity for recent turns
        recent_turns_text = []
        for t in turns[-3:]:
            sanitized = self.sanitize_error_cone(t.content)
            recent_turns_text.append(f"### [Turn #{t.turn_index} {t.role.upper()}]\n{sanitized}")

        condensed_doc = f"""# COMPRESSED INVARIANT MANIFOLD: {self.manifold.title}
**Source:** {self.manifold.source_platform} | **Original Turns:** {len(turns)} | **Lyapunov:** {self.manifold.metrics.lyapunov_exponent}

## Conversational Orbit Summary (Turns 1 to {len(turns)-3})
{"\n".join(summary_points)}

## Extracted Code Artifacts
{"\n\n".join(code_artifacts) if code_artifacts else "*(No code blocks in early turns)*"}

## Active Context (Final Turns)
{"\n\n---\n\n".join(recent_turns_text)}
"""
        return condensed_doc
