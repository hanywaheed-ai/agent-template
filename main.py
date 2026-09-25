import sys
import json
from config.settings import settings
from agents.auditor_agent import MultiAgentAuditorPipeline


def main():
    print("=" * 60)
    print("Multi-Agent AI Auditor Pipeline Execution")
    print("=" * 60)

    # Sample text containing a mock security vulnerability for testing
    sample_content = """
    # Infrastructure Configuration
    DATABASE_URL = "postgres://admin:password123@db.internal:5432/prod"
    API_KEY = "AIzaSyD_TEST_MOCK_KEY_VAL"
    DEBUG = True
    
    System Overview:
    This service processes internal user requests without additional input sanitization.
    """

    print("\n[INPUT CONTENT TO AUDIT]:")
    print(sample_content.strip())
    print("-" * 60)

    try:
        pipeline = MultiAgentAuditorPipeline()
        report = pipeline.run(sample_content)

        print("\n[FINAL VALIDATED AUDIT REPORT]:")
        print(report.model_dump_json(indent=2))
        print("=" * 60)
        print("[SUCCESS] Pipeline execution complete.")

    except Exception as e:
        print(f"\n[ERROR] Pipeline execution failed: {e}")
        if "BillingNotEnabled" in str(e) or "API has not been used" in str(e):
            print("\n[DIAGNOSTIC] Vertex AI requires an active Cloud Billing account attached to project "
                  f"'{settings.google_cloud_project}' to process LLM inference calls.")
        sys.exit(1)


if __name__ == "__main__":
    main()
