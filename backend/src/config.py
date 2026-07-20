"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Central application settings.

    Values are loaded from environment variables or a .env file.
    """

    # --- Database ---
    database_url: str = "postgresql://postgres:postgres@localhost:5432/banking_chatbot"

    # --- LLM ---
    openai_api_key: str = ""
    llm_model: str = "gpt-4o-mini"
    llm_temperature: float = 0.1

    # --- LangSmith ---
    langsmith_api_key: str = ""
    langsmith_project: str = "banking-support-chatbot"
    langsmith_tracing: bool = True

    # --- Agent Server ---
    langgraph_api_url: str = "http://localhost:2024"

    # --- Custom API ---
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: list[str] = [
        "http://localhost:3000",   # Agent Chat UI
        "http://localhost:5173",   # Admin Dashboard (Vite dev)
    ]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
