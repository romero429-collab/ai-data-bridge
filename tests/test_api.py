"""
Unit and Integration Tests for FastAPI Cloud API
"""

import unittest
from fastapi.testclient import TestClient
from app import app


class TestFastAPICloudEndpoints(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_root_endpoint(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "Asymptotically Stable")

    def test_health_check(self):
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "healthy")
        self.assertLess(data["spectral_radius"], 1.0)

    def test_demo_endpoint(self):
        res = self.client.get("/api/demo")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("manifold", data)
        self.assertIn("html_replica", data)
        self.assertIn("csv", data)
        self.assertIn("antigravity_payload", data)
        self.assertTrue(len(data["manifold"]["turns"]) >= 4)

    def test_extract_endpoint_text(self):
        payload = {
            "raw": "Gabriel: Initial state vector.\nGemini: Stable fixed point confirmed.",
            "title": "Cloud API Test"
        }
        res = self.client.post("/api/extract", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data["manifold"]["turns"]), 2)
        self.assertEqual(data["manifold"]["turns"][0]["role"], "user")
        self.assertEqual(data["manifold"]["turns"][1]["role"], "assistant")


if __name__ == "__main__":
    unittest.main()
