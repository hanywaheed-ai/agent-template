# Enterprise Multi-Agent AI Audit Pipeline Template

Production-grade, modular, security-first multi-agent template built with Google Cloud Vertex AI (Gemini 3.5-flash), Google ADK, and Pydantic V2.

## Key Features
* **Critic/Reviser Architecture:** Multi-agent evaluation and automated revision loop.
* **Structured JSON Enforcement:** Strict schema outputs using Pydantic V2 models.
* **Security First:** Application Default Credentials (ADC) authentication without hardcoded API keys.

## Quickstart
```bash
cp .env.example .env
gcloud auth application-default login
pip install -r requirements.txt
python main.py
---

### Step 2: Resolve the Vertex AI Billing Requirement

To execute `python main.py` and run Gemini 3.5-flash via Vertex AI, choose **one** of the following options:

#### Option A: Link Billing to `agent-template-dev-2041` (Recommended)
1. Open [Google Cloud Console Billing Enable Page](https://console.developers.google.com/billing/enable?project=agent-template-dev-2041).
2. Select your existing Cloud Billing account and click **Set Account**.
3. *(Cost Safety)* Standard usage for development/testing falls within Google's free tier quotas or free trial credits.

#### Option B: Point `.env` to Your Existing Billed Project (`automation-v1-437614`)
If you prefer not to touch billing on `agent-template-dev-2041`, update `.env` to route API calls through your existing project while keeping all code in `~/agent-template`:

```bash
cat << 'EOF' > ~/agent-template/.env
GOOGLE_CLOUD_PROJECT=automation-v1-437614
GOOGLE_CLOUD_LOCATION=global
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_GENAI_USE_ENTERPRISE=true
MODEL=gemini-3.5-flash
