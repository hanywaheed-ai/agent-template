# Enterprise Multi-Agent AI Audit Pipeline Template

Production-grade, modular, security-first multi-agent template built with Google Cloud Vertex AI (Gemini 3.5-flash), Google ADK, and Pydantic V2.

## Key Features
* **Critic/Reviser Architecture:** Multi-agent evaluation and automated revision loop.
* **Structured JSON Enforcement:** Strict schema outputs using Pydantic V2 models.
* **Security First:** Application Default Credentials (ADC) authentication without hardcoded API keys.

## Quickstart

1. **Configure Environment:**
   ```bash
   cp .env.example .env
