import os
import json
from google.genai import types
from google.genai.client import Client

from config.settings import settings
from schemas.auditor_schema import AuditReport


class MultiAgentAuditorPipeline:
    """
    Sequential Multi-Agent Pipeline:
    Agent 1 (Critic)  -> Analyzes raw input and generates structured audit observations.
    Agent 2 (Reviser) -> Formats findings and rewrites output into strict Pydantic JSON schema.
    """

    def __init__(self):
        # Initialize GenAI Client using Vertex AI Application Default Credentials (ADC)
        self.client = Client()
        self.model_name = settings.model

    def _critic_agent(self, content_to_audit: str) -> str:
        """Critic Agent: Evaluates input quality, compliance, and security risks."""
        system_instruction = (
            "You are a strict Enterprise Security and Quality Assurance Critic. "
            "Analyze the provided text for security vulnerabilities, hardcoded secrets, "
            "factual inaccuracy, and formatting defects. Be thorough and objective."
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=f"Audit this content:\n\n{content_to_audit}",
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.2,  # Low temperature for deterministic analysis
            )
        )
        return response.text

    def _reviser_agent(self, original_content: str, critic_feedback: str) -> AuditReport:
        """Reviser Agent: Consolidates critic feedback into validated AuditReport JSON schema."""
        system_instruction = (
            "You are an AI Output Synthesizer and Compliance Reviser. "
            "Review the original content alongside the Critic's audit feedback. "
            "Produce a final AuditReport JSON structure detailing whether it passed, "
            "quality score (0-100), findings list, and a revised safe version if needed."
        )

        prompt = (
            f"ORIGINAL CONTENT:\n{original_content}\n\n"
            f"CRITIC FEEDBACK:\n{critic_feedback}\n\n"
            "Synthesize this analysis into the required AuditReport structured format."
        )

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=AuditReport,
                temperature=0.1
            )
        )

        # Parse and return validated Pydantic model
        return AuditReport.model_validate_json(response.text)

    def run(self, content: str) -> AuditReport:
        """Executes the sequential multi-agent workflow."""
        print("[PIPELINE] Invoking Agent 1 (Critic)...")
        critic_findings = self._critic_agent(content)

        print("[PIPELINE] Invoking Agent 2 (Reviser & Schema Formatter)...")
        final_report = self._reviser_agent(content, critic_findings)

        return final_report


# Clean export
__all__ = ["MultiAgentAuditorPipeline"]
