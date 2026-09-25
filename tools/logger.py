import logging
import os
import google.cloud.logging


def setup_logger(name: str = "agent_auditor") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding duplicate handlers if already initialized
    if logger.handlers:
        return logger

    # Console Handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # Attach Cloud Logging Handler if running in GCP
    try:
        client = google.cloud.logging.Client()
        client.setup_logging()
    except Exception as e:
        logger.warning(f"Google Cloud Logging not initialized (local fallback mode active): {e}")

    return logger


# Global logger instance
logger = setup_logger()
