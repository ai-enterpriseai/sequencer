"""
Runner module for executing prompt sequences across LLM providers.
"""
import asyncio
import logging
from pathlib import Path
from typing import List, Dict, Optional, AsyncIterator
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

    def _replace_placeholders(self, text: str, **kwargs) -> str:
        """
        Replace placeholders in `text` with the corresponding values in kwargs.
        Placeholders look like {key}.
        If a given placeholder isn't provided in kwargs, it won't be replaced.
        """
        for key, value in kwargs.items():
            if value is not None:
                text = text.replace(f"{{{key}}}", str(value))
        return text

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
        sequence_file: Path,
        models: List[str],
        num_runs: int,
        **kwargs
    ) -> AsyncIterator[List[RunResult]]:
        """Run sequence and yield results as they complete"""
        runner = SequenceRunner()
        sections = read_sequence(sequence_file)

        # Replace placeholders in each section
        updated_sections = []
        for section in sections:
            replaced_content = self._replace_placeholders(section.content, **kwargs)
            section.content = replaced_content
            updated_sections.append(section)
        
        tasks = {
            asyncio.create_task(
                runner._run_model(model, sections),
                name=f"{model}_run_{i}"
            )
            for model in models
            for i in range(num_runs)
        }
        
        # Process tasks as they complete
        while tasks:
            done, _ = await asyncio.wait(
                tasks, 
                return_when=asyncio.FIRST_COMPLETED
            )
            
            for task in done:
                tasks.remove(task)
                try:
                    results = await task
                    if results:  # Only yield if we have results
                        yield results
                except Exception as e:
                    self.logger.error(f"Task {task.get_name()} failed: {str(e)}")
                    # Continue with remaining tasks instead of raising
                    continue

async def run(
    sequence_file: str | Path,
    models: List[str],
    num_runs: int = 1
) -> List[RunResult]:
    """Run prompts through specified models"""
    runner = SequenceRunner()
    all_results = []
    async for results in runner.run_sequence(sequence_file, models, num_runs):
        all_results.extend(results)
    return all_results