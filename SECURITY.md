# Security & Zero-Trust Policy

## 🔒 Security Architecture

The **AI-to-AI Data Bridge (DDS-Bridge)** is engineered with strict mathematical and cybernetic zero-trust invariants:

1. **Zero Secret Retention**: No API keys, credentials, or personal session tokens are stored, persisted, or required by the core engine.
2. **Input Sanitization & Error-Cone Filtering**: All conversational text passes through `PropagationVectorEngine.sanitize_error_cone()` to eliminate malicious control bytes (`\x00`), unclosed code fence attacks, and raw script tag injections before target manifold synthesis.
3. **HTML XSS Prevention**: The `StructuralAttractor` HTML replica renders content via rigorous character entity escaping (`escapeHtml`), neutralizing arbitrary script execution vectors.
4. **Local Execution**: All transformations occur 100% locally on the host machine. No telemetry or conversational state is transmitted to third-party endpoints.

## 🛡️ Reporting a Vulnerability

If you discover a potential security vulnerability in this project, please open a security advisory or notify the maintainers directly. Vulnerabilities will be triaged and resolved with high priority.
