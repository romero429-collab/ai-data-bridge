"""
AI-to-AI Data Bridge Core Package
"""

from .models import ChatTurn, CodeSnippet, ConversationManifold, PhaseSpaceMetrics
from .dynamics import Quaternion, DynamicalSystemEngine
from .ingestion import ConversationExtractor
from .attractor import StructuralAttractor
from .propagation import PropagationVectorEngine

__all__ = [
    "ChatTurn",
    "CodeSnippet",
    "ConversationManifold",
    "PhaseSpaceMetrics",
    "Quaternion",
    "DynamicalSystemEngine",
    "ConversationExtractor",
    "StructuralAttractor",
    "PropagationVectorEngine",
]
