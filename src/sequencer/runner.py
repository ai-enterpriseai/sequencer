"""
Runner module for executing prompt sequences across LLM providers.
"""
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Optional
from pydantic import BaseModel, computed_field
from datetime import datetime, timedelta

from .config import Settings, APIConfig, RunnerConfig, get_settings
from .providers import get_provider, LLMError
from .reader import read_sequence, PromptSection

class RunResult(BaseModel):
    """Result of a single run"""
    model: str
    title: str
    content: str
    response: str
    error: Optional[str] = None
    start_time: datetime
    end_time: datetime

    @computed_field
    def duration_seconds(self) -> timedelta:
        return self.end_time - self.start_time
    
class SequenceRunner:
    """Handles running prompt sequences through LLM providers"""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or get_settings()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _prepare_messages(self, sections: List[PromptSection]) -> List[Dict[str, str]]:
        """Prepare initial messages from sections"""
        if not sections:
            raise ValueError("No sections provided")
        return [{"role": "system", "content": sections[0].content}]

    async def _run_model(self, model: str, sections: List[PromptSection]) -> List[RunResult]:
        """Run sequence through a single model"""
        if not sections:
            raise ValueError("No sections provided")
            
        messages = self._prepare_messages(sections)
        results = []
        
        try:
            runner_config = RunnerConfig(model=model)
            provider = get_provider(self.settings, runner_config)
            
            for section in sections[1:]:
                try:
                    self.logger.info(f"Processing: {section.title}")
                    messages.append({"role": "user", "content": section.content})
                    
                    start_time = datetime.now()
                    response = await provider.generate(messages)
                    end_time = datetime.now()
                    
                    messages.append({"role": "assistant", "content": response})
                    
                    results.append(RunResult(
                        model=model,
                        title=section.title,
                        content=section.content,
                        response=response,
                        start_time=start_time,
                        end_time=end_time
                    ))
                    
                except LLMError as e:
                    self.logger.error(f"Error processing section {section.title}: {str(e)}")
                    results.append(RunResult(
                        model=model,
                        title=section.title,
                        content=section.content,
                        response="",
                        error=str(e),
                        start_time=start_time,
                        end_time=datetime.now()
                    ))
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error running model {model}: {str(e)}")
            raise
    
    async def run_sequence(
        self, 
        sequence_file: str | Path,
        models: List[str],
        num_runs: int = 1
    ) -> List[RunResult]:
        """Run sequence through specified models"""
        if not models:
            raise ValueError("No models provided")
        if num_runs < 1:
            raise ValueError("num_runs must be positive")
            
        sections = read_sequence(sequence_file)
        tasks = [
            self._run_model(model, sections)
            for model in models
            for _ in range(num_runs)
        ]
        
        results = []
        for completed in asyncio.as_completed(tasks):
            try:
                run_results = await completed
                results.extend(run_results)
            except Exception as e:
                self.logger.error(f"Task failed: {str(e)}")
                raise
        
        return results

async def run(
    sequence_file: str | Path,
    models: List[str],
    num_runs: int = 1
) -> List[RunResult]:
    """Run prompts through specified models"""
    runner = SequenceRunner()
    return await runner.run_sequence(sequence_file, models, num_runs)
