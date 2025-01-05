"""
Main entry point for sequencer.
"""
import sys
import asyncio
import logging
import argparse
from pathlib import Path

from .config import ModelType
from .runner import run
from .writer import write_results

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
            "meta-llama/Meta-Llama-3.1-405B-Instruct-Turbo",
            "claude-3-5-sonnet-20241022",
            "gpt-4o-2024-08-06",
        ],
        help="Models to run (space-separated)"
    )
    parser.add_argument(
        "-n", "--num-runs",
        type=int,
        default=1,
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
        # Get sequence file path
        sequence_file = get_sequence_path(args.sequence_file)
        
        logger.info(f"Processing sequence file: {sequence_file}")
        logger.info(f"Using models: {', '.join(args.models)}")
        
        results = await run(sequence_file, args.models, args.num_runs)
        write_results(results, args.output_dir)
        
        logger.info("Processing complete")
        
    except Exception as e:
        logger.error(f"Error processing sequence: {str(e)}")
        sys.exit(1)

def cli() -> None:
    """Command line entry point"""
    asyncio.run(main())

if __name__ == "__main__":
    cli()
