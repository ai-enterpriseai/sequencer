# system 
analyze errors in the code provided by the user
<pattern> 

<pattern.name>testing and performance evaluation</pattern.name> 

<pattern.content>

use @tester to create unit tests and integration tests as specified by the user 

</pattern.content> 

</pattern>
<patterns>

define @tester (

- create unit tests and integration tests for the provided file
- consider configuration, standard cases, edge cases, and performance 
- use as little mock objects as possible 
- utilize proper testing frameworks as per the provided context 
- ensure coverage includes both happy paths and edge cases 
- provide a concise command line instruction for the developer to run the tests 
- strictly follow the <instructions> at all times 
- always start your messages with "@tester"

)

define @optimizer (

- analyze performance metrics of the code 
- suggest optimizations and improvements 
- ensure adherence to performance standards while maintaining functionality
- refer to testing results from @tester if available
- always start your messages with "@optimizer"

) 

</patterns> 

<best practice>

- ensure coverage of all critical cases, including edge and standard scenarios 
- maintain compatibility with specified configurations 
- adhere to the appropriate testing framework for the environment 
- ensure all tests are concise, readable, and reusable 
- evaluate performance thoroughly to prevent bottlenecks 

</best practice>

<routine>

- read through the instructions 
- create a plan of action 
- confirm you understand the task 

</routine> 

---

# create tests for the following code

"""
Sequence reader module for parsing markdown prompt files.
"""
from pathlib import Path
from typing import List, Dict
import re
from pydantic import BaseModel, Field, field_validator

class PromptSection(BaseModel):
    """Single prompt section from sequence file"""
    title: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    
    @field_validator('title', 'content')
    def no_empty_strings(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Cannot be empty or whitespace")
        return v.strip()

class SequenceReader:
    """Handles reading and parsing sequence files"""
    
    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
    
    def read_content(self) -> str:
        """Read file content safely"""
        try:
            return self.file_path.read_text(encoding='utf-8')
        except Exception as e:
            raise ValueError(f"Error reading {self.file_path}: {str(e)}")
    
    def parse_sections(self, content: str) -> List[PromptSection]:
        """Parse content into sections with error handling"""
        if not content.strip():
            raise ValueError("Empty sequence file")
        
        # Remove any content after --end-- marker if present
        content = re.split(r'\n--end--\s*\n', content.strip())[0]
        
        sections = re.split(r'\n---+\n', content.strip())
        result = []
        
        for i, section in enumerate(sections, 1):
            try:
                title_match = re.search(r'^#{1,2}\s+(.+)$', section, re.MULTILINE)
                if not title_match:
                    raise ValueError(f"Missing or invalid title")
                                
                # Get everything after the title line as content
                content = re.sub(r'^#\s+.+?\n', '', section, count=1, flags=re.MULTILINE).strip()
                if not content:
                    raise ValueError(f"Missing content")
                
                result.append(PromptSection(
                    title=title_match.group(1),
                    content=content
                ))
            except ValueError as e:
                raise ValueError(f"Error in section {i}: {str(e)}")        
        if not result:
            raise ValueError("No valid sections found in file")
        
        return result

def read_sequence(file_path: str | Path) -> List[PromptSection]:
    """
    Read and parse a sequence file.
    
    Args:
        file_path: Path to the sequence file
        
    Returns:
        List[PromptSection]: List of parsed prompt sections
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file is empty or has invalid format
    
    Example:
        >>> sections = read_sequence("prompts.md")
        >>> for section in sections:
        ...     print(f"Title: {section.title}")
        ...     print(f"Content: {section.content}")
    """
    reader = SequenceReader(file_path)
    content = reader.read_content()
    return reader.parse_sections(content)

---

# review the testing and performance results

@optimizer 

- review the testing outcomes and performance evaluation in great detail
- propose changes and adaptations if necessary 

---

# review proposed changes 

@tester 

- review proposal by @optimizer
- critically consider them and implement what is necessary
- focus on implementing tests only, if changes to the source code are needed, highlight them with # source code changes 

--end--
