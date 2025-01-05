"""
Handles API configurations and settings for different LLM providers.
"""
from typing import Dict, Optional, Literal
from pydantic import BaseModel, Field, SecretStr, AnyHttpUrl
from pydantic_settings import BaseSettings

ModelType = Literal[
    "gpt-4o-2024-08-06", # OpenAI 
    "claude-3-5-sonnet-20241022", # Anthopic 
    "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", # Together.ai
    "Meta-Llama-3.1-405B-Instruct", # SambaNova
    "llama-3.3-70b", # Cerebras
    # "o1-2024-12-17",
    # "o1-preview-2024-09-12",
    # "o1-mini-2024-09-12",
]

class APIConfig(BaseModel):
    """Base configuration for API providers"""
    api_key: SecretStr
    base_url: Optional[AnyHttpUrl] = None
    timeout: float = Field(default=30.0, ge=0.0)
    max_retries: int = Field(default=3, ge=0)

class RunnerConfig(BaseModel):
    """Configuration for LLM execution"""
    model: ModelType
    temperature: float = Field(default=0.1, ge=0.0, le=1.0)
    top_p: float = Field(default=0.1, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(default=4096, gt=0)
    system_prompt: str = "You are a helpful assistant."

class Settings(BaseSettings):
    """Global settings for the LLM runner"""
    openai_api_key: SecretStr
    anthropic_api_key: SecretStr
    together_api_key: SecretStr
    hf_api_key: SecretStr
    cerebras_api_key: SecretStr
    sambanova_api_key: SecretStr
    
    @property
    def openai_config(self) -> APIConfig:
        """Get OpenAI API configuration"""
        return APIConfig(api_key=self.openai_api_key)
    
    @property
    def anthropic_config(self) -> APIConfig:
        """Get Anthropic API configuration"""
        return APIConfig(api_key=self.anthropic_api_key)
    
    @property
    def together_config(self) -> APIConfig:
        """Get Together AI API configuration"""
        return APIConfig(
            api_key=self.together_api_key,
            base_url="https://api.together.ai/v1"
        )
    
    @property
    def cerebras_config(self) -> APIConfig:
        """Get Cerebras API configuration"""
        return APIConfig(
            api_key=self.cerebras_api_key,
            base_url="https://api.cerebras.ai/v1"
        )
    
    @property
    def sambanova_config(self) -> APIConfig:
        """Get SambaNova API configuration"""
        return APIConfig(
            api_key=self.sambanova_api_key,
            base_url="https://api.sambanova.ai/v1"
        )
    
    @property
    def hf_config(self) -> APIConfig:
        """Get HuggingFace API configuration"""
        return APIConfig(api_key=self.hf_api_key)
    
    class Config:
        """Pydantic settings configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"

def get_settings() -> Settings:
    """
    Get settings instance with environment variables.
    
    Returns:
        Settings: Configuration instance with loaded environment variables
        
    Raises:
        pydantic.ValidationError: If required environment variables are missing
    """
    return Settings()


