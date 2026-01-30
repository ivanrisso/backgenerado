import os
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict

class Settings(BaseSettings):
    model_config = ConfigDict(
        env_file=".env.test" if os.getenv("ENV") == "test" else ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Base de datos
    DATABASE_URL: str = Field(..., env="DATABASE_URL")
    ALEMBIC_URL: str | None = Field(None, env="ALEMBIC_URL")

    # AFIP
    AFIP_CERT_CRT_PATH: str = Field(..., env="AFIP_CERT_CRT_PATH")
    AFIP_KEY_CRT_PATH: str = Field(..., env="AFIP_KEY_CRT_PATH")
    AFIP_CUIT: int        = Field(..., env="AFIP_CUIT")
    AFIP_ENVIRONMENT: str = Field("production", env="AFIP_ENVIRONMENT")


    # JWT
    JWT_SECRET_KEY: str                 = Field(..., env="JWT_SECRET_KEY")
    JWT_ALGORITHM: str                  = Field("HS256", env="JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int   = Field(7,  env="JWT_REFRESH_TOKEN_EXPIRE_DAYS")

    # Security
    BACKEND_CORS_ORIGINS: list[str] = Field(default=[], env="BACKEND_CORS_ORIGINS")

    @property
    def IS_PRODUCTION(self) -> bool:
        return self.AFIP_ENVIRONMENT.lower() == "production"

settings = Settings()
