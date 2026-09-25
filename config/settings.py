import os
import sys
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Locate and load the root .env file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(BASE_DIR, '.env')

load_dotenv(dotenv_path=ENV_PATH, override=True)


class AppSettings(BaseModel):
    google_cloud_project: str = Field(
        default_factory=lambda: os.getenv("GOOGLE_CLOUD_PROJECT", "")
    )
    google_cloud_location: str = Field(
        default_factory=lambda: os.getenv("GOOGLE_CLOUD_LOCATION", "global")
    )
    google_genai_use_vertexai: str = Field(
        default_factory=lambda: os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "true")
    )
    google_genai_use_enterprise: str = Field(
        default_factory=lambda: os.getenv("GOOGLE_GENAI_USE_ENTERPRISE", "true")
    )
    model: str = Field(
        default_factory=lambda: os.getenv("MODEL", "gemini-3.5-flash")
    )

    def enforce_environment(self) -> None:
        """Validates configuration and locks values into os.environ."""
        if not self.google_cloud_project or self.google_cloud_project == "your-gcp-project-id":
            print("[ERROR] GOOGLE_CLOUD_PROJECT is missing or invalid in .env")
            sys.exit(1)

        # Force authentication flags globally
        os.environ["GOOGLE_CLOUD_PROJECT"] = self.google_cloud_project
        os.environ["GOOGLE_CLOUD_LOCATION"] = self.google_cloud_location
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = self.google_genai_use_vertexai.lower()
        os.environ["GOOGLE_GENAI_USE_ENTERPRISE"] = self.google_genai_use_enterprise.lower()
        os.environ["MODEL"] = self.model

        print(f"[SUCCESS] Config initialized for project: {self.google_cloud_project} | Model: {self.model}")


# Export initialized instance
settings = AppSettings()
settings.enforce_environment()
