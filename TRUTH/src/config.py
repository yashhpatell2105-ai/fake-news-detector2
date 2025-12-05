"""Configuration settings for TRUTH system"""

import os
from dotenv import load_dotenv

load_dotenv()

# Flask Configuration
DEBUG = os.getenv("DEBUG", "True") == "True"
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 5000))

# NLP Configuration
NLP_MODEL = "en_core_web_sm"
MIN_CONFIDENCE_SCORE = 0.5

# Fact-Check Configuration
FACT_CHECK_THRESHOLD = 0.7
MAX_SOURCES_TO_CHECK = 5

# API Configuration
API_TIMEOUT = 30
RATE_LIMIT = 100  # requests per minute

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = "logs/truth.log"

# Database (if needed)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///truth.db")
