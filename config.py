"""
Configuration for the Natural Language Database Assistant.
Loads settings from environment variables with sensible defaults.
"""

import os
import secrets
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""

    # Flask
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(32))
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = os.path.join(os.path.dirname(__file__), "flask_session")
    SESSION_PERMANENT = False

    # Gemini API
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL = "gemini-3.6-flash"

    # Safety thresholds
    MAX_SELECT_ROWS = 1000  # Max rows returned by SELECT queries
    WARN_AFFECTED_ROWS = 10  # Warn if UPDATE/DELETE affects more than N rows
    CRITICAL_AFFECTED_ROWS = 100  # Extra warning for large-scale operations

    # Conversation
    MAX_CONVERSATION_HISTORY = 10  # Number of exchanges to keep in context

    # Blocked SQL operations (DDL)
    BLOCKED_OPERATIONS = [
        "DROP", "TRUNCATE", "ALTER", "CREATE", "RENAME",
        "GRANT", "REVOKE", "EXEC", "EXECUTE"
    ]
