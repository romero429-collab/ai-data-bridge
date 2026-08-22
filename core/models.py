"""
Data models for the AI-to-AI Data Bridge and Discrete Dynamical System.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Tuple
import hashlib
import json
import time


@dataclass
class CodeSnippet:
    language: str
    code: str
    line_count: int
    hash: str = ""

    def __post_init__(self):
        if not self.hash and self.code:
            self.hash = hashlib.sha256(self.code.encode("utf-8")).hexdigest()[:12]


@dataclass
class ChatTurn:
    turn_index: int
    role: str  # "user" | "assistant" | "system" | "tool"
    content: str
    raw_html: Optional[str] = None
    code_blocks: List[CodeSnippet] = field(default_factory=list)
    timestamp: Optional[str] = None
    model: Optional[str] = None
    citations: List[str] = field(default_factory=list)
    char_count: int = 0
    token_estimate: int = 0
    phase_x: float = 0.0
    phase_y: float = 0.0

    def __post_init__(self):
        if not self.char_count:
            self.char_count = len(self.content)
        if not self.token_estimate:
            self.token_estimate = max(1, len(self.content) // 4)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PhaseSpaceMetrics:
    total_turns: int = 0
    total_tokens: int = 0
    total_chars: int = 0
    lyapunov_exponent: float = -0.15
    spectral_radius: float = 0.85
    entropy: float = 1.42
    quaternion_norm: Tuple[float, float, float, float] = (1.0, 0.0, 0.0, 0.0)
    contractivity_factor: float = 0.78
    is_ergodic: bool = True
    stability_status: str = "Asymptotically Stable"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ConversationManifold:
    id: str
    title: str
    source_platform: str  # "chatgpt" | "claude" | "gemini" | "perplexity" | "generic" | "manual"
    source_url: Optional[str] = None
    extracted_at: str = field(default_factory=lambda: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    turns: List[ChatTurn] = field(default_factory=list)
    metrics: PhaseSpaceMetrics = field(default_factory=PhaseSpaceMetrics)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConversationManifold":
        turns_data = data.get("turns", [])
        turns = []
        for t in turns_data:
            code_blocks = [CodeSnippet(**cb) for cb in t.get("code_blocks", [])]
            t_copy = dict(t)
            t_copy["code_blocks"] = code_blocks
            turns.append(ChatTurn(**t_copy))
        
        metrics_data = data.get("metrics", {})
        if isinstance(metrics_data.get("quaternion_norm"), list):
            metrics_data["quaternion_norm"] = tuple(metrics_data["quaternion_norm"])
        metrics = PhaseSpaceMetrics(**metrics_data) if metrics_data else PhaseSpaceMetrics()

        return cls(
            id=data.get("id", "manifold_0"),
            title=data.get("title", "Untitled Conversation"),
            source_platform=data.get("source_platform", "generic"),
            source_url=data.get("source_url"),
            extracted_at=data.get("extracted_at", ""),
            turns=turns,
            metrics=metrics,
            metadata=data.get("metadata", {})
        )
