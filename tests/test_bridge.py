"""
Unit and Integration Test Suite for AI-to-AI Data Bridge (DDS-Bridge).
Verifies dynamical stability indicators, DOM ingestion dynamics, manifold formatters,
and kinematics injection engines.
"""

import unittest
import json
from pathlib import Path
from core.models import ChatTurn, CodeSnippet, ConversationManifold
from core.dynamics import Quaternion, DynamicalSystemEngine
from core.ingestion import ConversationExtractor
from core.attractor import StructuralAttractor
from core.propagation import PropagationVectorEngine


class TestDynamicalSystems(unittest.TestCase):

    def test_quaternion_norm_preservation(self):
        """Verify Hamilton product preserves S^3 unit norm."""
        q1 = Quaternion(0.5, 0.5, 0.5, 0.5)
        q2 = Quaternion(1.0, 0.0, 0.0, 0.0)
        q3 = q1 * q2
        self.assertAlmostEqual(q3.norm(), 1.0, places=5)

        q4 = Quaternion(0.2, -0.4, 0.8, -0.1)
        q5 = Quaternion(-0.6, 0.1, 0.3, 0.7)
        product = q4 * q5
        self.assertAlmostEqual(product.norm(), 1.0, places=5)

    def test_spectral_radius_and_lyapunov(self):
        """Verify Banach fixed point contractivity and stability."""
        engine = DynamicalSystemEngine()
        turns = [
            ChatTurn(turn_index=1, role="user", content="Test prompt 1"),
            ChatTurn(turn_index=2, role="assistant", content="Test response 1"),
            ChatTurn(turn_index=3, role="user", content="Test prompt 2"),
            ChatTurn(turn_index=4, role="assistant", content="Test response 2"),
        ]
        coords = engine.compute_turn_phase_coordinates(turns)
        self.assertEqual(len(coords), 4)
        
        metrics = engine.calculate_metrics(turns)
        self.assertLess(metrics.spectral_radius, 1.0, "Spectral radius must be < 1.0 for Banach contraction")
        self.assertLess(metrics.lyapunov_exponent, 0.0, "Lyapunov exponent must be negative for asymptotic stability")
        self.assertIn("Stable", metrics.stability_status)


class TestIngestionMap(unittest.TestCase):

    def setUp(self):
        self.extractor = ConversationExtractor()

    def test_extract_transcript_text(self):
        text = """
        Gabriel: Hello Antigravity.
        Gemini: Acknowledged, state vector initialized.
        Gabriel: Let's run the DDS coupled map.
        Gemini: Executing transition map.
        """
        manifold = self.extractor.extract_from_text(text, title="Transcript Test")
        self.assertEqual(len(manifold.turns), 4)
        self.assertEqual(manifold.turns[0].role, "user")
        self.assertEqual(manifold.turns[1].role, "assistant")
        self.assertEqual(manifold.turns[2].role, "user")
        self.assertEqual(manifold.turns[3].role, "assistant")

    def test_extract_html_dom(self):
        html_doc = """
        <!DOCTYPE html>
        <html>
        <head><title>ChatGPT Share Snapshot</title></head>
        <body>
            <article data-message-author-role="user">
                <div class="markdown"><p>What is a Hénon map?</p></div>
            </article>
            <article data-message-author-role="assistant">
                <div class="markdown">
                    <p>A Hénon map is a discrete-time dynamical system defined as:</p>
                    <pre><code class="language-python">x_next = 1 - a * x**2 + y</code></pre>
                </div>
            </article>
        </body>
        </html>
        """
        manifold = self.extractor.extract_from_html(html_doc, source_platform="chatgpt")
        self.assertEqual(len(manifold.turns), 2)
        self.assertEqual(manifold.turns[0].role, "user")
        self.assertEqual(manifold.turns[1].role, "assistant")
        self.assertTrue(len(manifold.turns[1].code_blocks) >= 1)
        self.assertEqual(manifold.turns[1].code_blocks[0].language, "python")

    def test_extract_dehydrated_nextjs_json(self):
        next_data = {
            "props": {
                "pageProps": {
                    "title": "NextJS Shared Chat",
                    "linear_conversation": [
                        {"message": {"author": {"role": "user"}, "content": {"parts": ["Calculate Jacobian."]}}},
                        {"message": {"author": {"role": "assistant"}, "content": {"parts": ["Jacobian calculated."]}}}
                    ]
                }
            }
        }
        html_doc = f'<html><head><script id="__NEXT_DATA__" type="application/json">{json.dumps(next_data)}</script></head><body></body></html>'
        manifold = self.extractor.extract_from_html(html_doc)
        self.assertEqual(len(manifold.turns), 2)
        self.assertEqual(manifold.title, "NextJS Shared Chat")
        self.assertEqual(manifold.turns[0].content, "Calculate Jacobian.")


class TestStructuralAttractorAndKinematics(unittest.TestCase):

    def setUp(self):
        extractor = ConversationExtractor()
        text = "Gabriel: Test prompt\nGemini: Test response with ```python\nprint('hello')\n```"
        self.manifold = extractor.extract_from_text(text, title="Test Attractor")
        self.attractor = StructuralAttractor(self.manifold)
        self.propagation = PropagationVectorEngine(self.manifold)

    def test_html_replica_generation(self):
        html_replica = self.attractor.to_html_replica()
        self.assertIn("<!DOCTYPE html>", html_replica)
        self.assertIn("Phase-Space Portrait", html_replica)
        self.assertIn("Test prompt", html_replica)

    def test_csv_generation(self):
        csv_text = self.attractor.to_csv()
        self.assertIn("Turn,Role,Model", csv_text)
        self.assertIn("USER", csv_text)
        self.assertIn("ASSISTANT", csv_text)

    def test_antigravity_injection_synthesis(self):
        payload = self.propagation.synthesize_antigravity_payload()
        self.assertIn("<INGESTED_CONVERSATION_MANIFOLD>", payload)
        self.assertIn("<turn index=\"1\" role=\"USER\">", payload)
        self.assertIn("</INGESTED_CONVERSATION_MANIFOLD>", payload)

    def test_claude_xml_synthesis(self):
        xml_payload = self.propagation.synthesize_claude_xml()
        self.assertIn("<conversation_manifold", xml_payload)
        self.assertIn("<message index=\"1\" speaker=\"Human\">", xml_payload)


if __name__ == "__main__":
    unittest.main()
