"""
Writer module for saving LLM run results to files.
"""
from pathlib import Path
from typing import List
from datetime import datetime 

from .runner import RunResult

class ResultWriter:
    """Handles writing run results to files"""
    
    def __init__(self, output_dir: str | Path = "results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
    
    def write_results(self, results: List[RunResult]) -> None:
        """Write results to markdown files"""
        if not results:
            return
            
        # Group by model
        model_results = {}
        for result in results:
            model_results.setdefault(result.model, []).append(result)
        
        # Write files
        for model, results in model_results.items():
            timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
            filename = f"results_{model.replace('/', '_')}_{timestamp}.md"
            filepath = self.output_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                for result in results:
                    f.write(f"# {result.title}\n\n")
                    f.write(f">> user:\n\n```\n{result.content}\n```\n\n")
                    f.write("---\n\n")
                    if result.error:
                        f.write(f"error: {result.error}\n\n")
                    else:
                        f.write(f">> ai:\n\n{result.response}\n\n")
                    f.write("---\n\n")

def write_results(results: List[RunResult], output_dir: str | Path = "results") -> None:
    """Write results to markdown files"""
    writer = ResultWriter(output_dir)
    writer.write_results(results)
    