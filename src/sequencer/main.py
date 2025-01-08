"""
Main entry point for sequencer.
"""
import sys
import asyncio
import logging
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import AsyncIterator, List

from .runner import RunResult, SequenceRunner
from .runner import run
from .writer import write_results
from .reader import read_sequence

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Define blueprints directory relative to package
BLUEPRINT_DIR = Path(__file__).parent / "blueprints"

def parse_args() -> argparse.Namespace:
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Run prompt sequences through LLM models"
    )
    parser.add_argument(
        "sequence_file",
        type=str,
        help="Name of sequence file in blueprints directory (e.g., sequence.md)"
    )
    parser.add_argument(
        "-m", "--models",
        nargs="+",
        default=[
            "gpt-4o-2024-08-06", # OpenAI 
            # "gpt-4o-mini-2024-07-18", # OpenAI 
            # "gpt-3.5-turbo-0125", # OpenAI 
            # "claude-3-5-sonnet-20241022", # Anthopic 
            # "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo", # Together.ai
            # "Meta-Llama-3.1-405B-Instruct", # SambaNova
            # "llama-3.3-70b", # Cerebras
        ],
        help="Models to run (space-separated)"
    )
    parser.add_argument(
        "-n", "--num-runs",
        type=int,
        default=1, # if >1, and rate limit is reached, can lead to multiple files written with the same content but diff timestamps
        help="Number of runs per model"
    )
    parser.add_argument(
        "-o", "--output-dir",
        type=str,
        default="results",
        help="Output directory for results"
    )
    return parser.parse_args()

def get_sequence_path(filename: str) -> Path:
    """
    Get full path to sequence file in blueprints directory.
    
    Args:
        filename: Name of sequence file
        
    Returns:
        Path: Full path to sequence file
    """
    # Create blueprints directory if it doesn't exist
    BLUEPRINT_DIR.mkdir(exist_ok=True)
    
    # Get full path to sequence file
    sequence_path = BLUEPRINT_DIR / filename
    
    # Verify file exists
    if not sequence_path.exists():
        sample_path = BLUEPRINT_DIR / "sequence.md"
        if not sample_path.exists():
            # Create sample sequence file
            sample_content = """# System Prompt
```
You are a helpful assistant.
```

---
# First Prompt
```
What is artificial intelligence?
```
"""
            sample_path.write_text(sample_content)
            logger.info(f"Created sample sequence file at {sample_path}")
        
        available = [f.name for f in BLUEPRINT_DIR.glob("*.md")]
        if available:
            logger.error(f"Available sequences: {', '.join(available)}")
        raise FileNotFoundError(f"Sequence file not found: {sequence_path}")
    
    return sequence_path

async def main() -> None:
    """Main entry point"""
    args = parse_args()
    
    try:
        runner = SequenceRunner()
        sequence_file = get_sequence_path(args.sequence_file)
        
        logger.info(f"Processing sequence file: {sequence_file}")
        logger.info(f"Using models: {', '.join(args.models)}")
        
        start_time = datetime.now()
        completed_results = []
        
        async for results in runner.run_sequence(sequence_file, args.models, args.num_runs):
            completed_results.extend(results)
            write_results(results, args.output_dir)
           
            # Log progress for each completed result
            for result in results:
                status = "Completed" if not result.error else "Failed"
                logger.info(
                    f"{status} {result.model} - {result.title} - "
                    f"duration: {result.duration_seconds.total_seconds():.1f}s"
                    + (f" (Error: {result.error})" if result.error else "")
                )
            
        # Log total execution time and success rate
        total_duration = datetime.now() - start_time
        total_attempts = len(args.models) * args.num_runs * (len(read_sequence(sequence_file)) - 1)
        success_count = len([r for r in completed_results if not r.error])
        
        logger.info(
            f"Processing complete in {total_duration.total_seconds() / 60:.0f}:{total_duration.total_seconds() % 60:.1f}\n"
            f"Success rate: {success_count}/{total_attempts} ({success_count/total_attempts*100:.1f}%)"
        )
        
    except Exception as e:
        logger.error(f"Error processing sequence: {str(e)}")
        sys.exit(1)

def cli() -> None:
    """Command line entry point"""
    asyncio.run(main())

if __name__ == "__main__":
    cli()
