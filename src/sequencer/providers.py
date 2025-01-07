"""
LLM provider interfaces for different API services.
"""
import asyncio
import logging
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from functools import wraps

from openai import AsyncOpenAI as OpenAI
from anthropic import AsyncAnthropic as Anthropic
from .config import Settings, APIConfig, RunnerConfig, ModelType

class LLMError(Exception):
    """Base exception for LLM errors"""
    pass

class RateLimitError(LLMError):
    """Rate limit exceeded"""
    pass

async def with_retries(func, max_retries: int = 3, base_delay: float = 1.0):
    """Simple retry handler with exponential backoff"""
    for attempt in range(max_retries):
        try:
            return await func()
        except RateLimitError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            await asyncio.sleep(delay)
    raise LLMError("Max retries exceeded")

class LLMProvider(ABC):
    """Base class for LLM providers"""
    
    def __init__(self, api_config: APIConfig, runner_config: RunnerConfig):
        self.api_config = api_config
        self.runner_config = runner_config
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod
    async def generate(self, messages: List[Dict[str, str]]) -> str:
        """Generate response from messages"""
        pass
    
    async def _handle_error(self, e: Exception) -> None:
        """Handle provider errors"""
        error_msg = str(e).lower()
        self.logger.error(f"Provider error: {error_msg}")
        if "rate limit" in error_msg:
            raise RateLimitError(str(e))
        raise LLMError(str(e))

class OpenAIProvider(LLMProvider):
    """OpenAI API provider"""
    
    def __init__(self, api_config: APIConfig, runner_config: RunnerConfig):
        super().__init__(api_config, runner_config)
        self.client = OpenAI(
            api_key=api_config.api_key.get_secret_value(),
            base_url=api_config.base_url,
            timeout=api_config.timeout,
            max_retries=api_config.max_retries
        )
    
    async def generate(self, messages: List[Dict[str, str]]) -> str:
        async def _generate():
            try:
                self.logger.info(f"Generating with OpenAI model: {self.runner_config.model}")
                response = await self.client.chat.completions.create(
                    model=self.runner_config.model,
                    messages=messages,
                    temperature=self.runner_config.temperature,
                    top_p=self.runner_config.top_p,
                    max_tokens=self.runner_config.max_tokens
                )
                return response.choices[0].message.content
            except Exception as e:
                await self._handle_error(e)
                
        return await with_retries(_generate)

class AnthropicProvider(LLMProvider):
    """Anthropic API provider"""
    
    def __init__(self, api_config: APIConfig, runner_config: RunnerConfig):
        super().__init__(api_config, runner_config)
        self.client = Anthropic(
            api_key=api_config.api_key.get_secret_value()
        )
    
    async def generate(self, messages: List[Dict[str, str]]) -> str:
        async def _generate():
            try:
                self.logger.info(f"Generating with Anthropic model: {self.runner_config.model}")
                response = await self.client.messages.create(
                    model=self.runner_config.model,
                    system=messages[0]["content"], # as given by runner.SequenceRunner._prepare_messages
                    messages=messages[1:],  # Exclude system message
                    max_tokens=self.runner_config.max_tokens,
                )
                return response.content[0].text
            except Exception as e:
                await self._handle_error(e)
                
        return await with_retries(_generate)

class OtherProviderOpenAILib(LLMProvider):
    """Other Provider based on the OpenAI library"""
    
    def __init__(self, api_config: APIConfig, runner_config: RunnerConfig):
        super().__init__(api_config, runner_config)
        self.client = OpenAI(
            api_key=api_config.api_key.get_secret_value(),
            base_url=str(api_config.base_url),
            timeout=api_config.timeout,
            max_retries=api_config.max_retries
        )
    
    async def generate(self, messages: List[Dict[str, str]]) -> str:
        async def _generate():
            try:
                self.logger.info(f"Generating with Other AI model: {self.runner_config.model}")
                response = await self.client.chat.completions.create(
                    model=self.runner_config.model,
                    messages=messages,
                    temperature=self.runner_config.temperature,
                    top_p=self.runner_config.top_p
                )
                return response.choices[0].message.content
            except Exception as e:
                await self._handle_error(e)
                
        return await with_retries(_generate)

def get_provider(settings: Settings, runner_config: RunnerConfig) -> LLMProvider:
    """
    Get appropriate provider instance.
    
    Args:
        model: Model type to use
        api_config: API configuration
        runner_config: Runner configuration
        
    Returns:
        LLMProvider: Provider instance for the specified model
        
    Raises:
        ValueError: If model type is not supported
    """
    model = runner_config.model
    if "gpt-4" in model or "o1-" or "gpt-3.5" in model:
        return OpenAIProvider(settings.openai_config, runner_config)
    elif "claude" in model:
        return AnthropicProvider(settings.anthropic_config, runner_config)
    elif "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo" in model:
        return OtherProviderOpenAILib(settings.together_config, runner_config)
    elif "Meta-Llama-3.1-405B-Instruct" in model:
        return OtherProviderOpenAILib(settings.sambanova_config, runner_config)
    elif "llama-3.3-70b" in model:
        return OtherProviderOpenAILib(settings.cerebras_config, runner_config)
    else:
        raise ValueError(f"Unsupported model: {model}")
    