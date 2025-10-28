# create requirements.txt

## Objective
Analyze Python source files to identify dependencies, update requirements.txt accordingly, and create a standards-compliant pyproject.toml file that supports installation with UV.

## Detailed Instructions

### 1. Source Code Analysis
- Examine all Python (.py) files 
- Identify all import statements and module dependencies
- Distinguish between standard library and third-party packages
- Note any version requirements specified in comments or docstrings

### 2. requirements.txt Management
- If requirements.txt exists:
  * Preserve existing dependencies and their version specifications
  * Add newly discovered dependencies not already listed
  * Ensure proper formatting (one package per line)
- If requirements.txt doesn't exist:
  * Create a new file listing all third-party dependencies
  * Use appropriate version specifiers (>= or ~= recommended)

### 3. pyproject.toml Creation
- Generate a PEP 621 compliant pyproject.toml file that includes:
  * Project metadata (name, version, description)
  * Dependencies list (matching requirements.txt)
  * Build system configuration compatible with UV
- Include these specific sections:
  * [build-system] with appropriate build backend
  * [project] with metadata and dependencies
  * [project.optional-dependencies] for development dependencies if applicable
  * Any necessary [tool] sections

## Output Deliverables
1. Updated or new requirements.txt file with all project dependencies
2. Complete pyproject.toml file configured for UV compatibility
3. Brief summary of dependencies identified and changes made

## Notes
- UV is a modern Python package installer written in Rust
- Ensure the pyproject.toml build-system section is compatible with UV
- If project metadata cannot be determined from code, use placeholders and note what information is needed