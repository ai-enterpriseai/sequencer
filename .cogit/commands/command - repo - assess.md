# command - repo - assess 
  
analyze the repository in detail  
filter out .venv, venv, node_modules or similar folders, like pycache
avoid using simplistic commands like ls -R | cat, always filter out 
explain and summarize its functionality  
critique and point out how this can be improved  
do not change anything  
deepen your assessment  
create a text based repo structure with all folders and files  
save it in the assessment.md in the .cogit directory, if latter exists, create if does not

# examples

Get-ChildItem -Recurse -Filter "*.py" | Where-Object {$_.FullName -notlike "*\.venv\*"} | Measure-Object | Select-Object Count
  
---  
  
```instructions  
  
# Repository Critical Assessment Protocol

## Primary Objective
Perform a comprehensive, objective analysis of the repository structure, code quality, and architecture with emphasis on identifying weaknesses and improvement opportunities.

## Analysis Scope
- Analyze all repository contents except:
  * Virtual environment folders (.venv, venv)
  * Cache directories (__pycache__, .pytest_cache)
  * Build artifacts and dependencies (node_modules, dist, build)
  * IDE configuration folders (.idea, .vscode)
- Document complete folder and file structure as a text-based tree

## Assessment Requirements
Evaluate using the following balanced fitness criteria (scale 1-10):

1. **Code Quality**
   - Readability: Is the code consistently formatted and easy to understand?
   - Maintainability: How difficult would it be to modify or extend?
   - Test coverage: Are critical components adequately tested?
   - Technical debt: What patterns indicate accumulated shortcuts?

2. **Architecture Evaluation**
   - Component separation: How well are concerns separated?
   - Dependency management: Is there clear dependency direction?
   - Scalability potential: Will the architecture support growth?
   - Security considerations: What vulnerabilities are present?

3. **Documentation Assessment**
   - Completeness: Are all key components documented?
   - Accuracy: Does documentation match implementation?
   - Accessibility: How easily can new developers understand the system?

4. **Repository Organization**
   - Structure clarity: Is the organization logical and consistent?
   - Build process: How robust is the build/deployment pipeline?
   - Configuration management: How are environment variables handled?

## Output Format Requirements
Create a file named `assessment.md` in the repository's cogit directory (create if not exists) with these sections:

1. **Repository Overview**
   - Basic repository information and primary purpose
   - Text-based repository structure visualization
   - Technology stack identification

2. **Critical Analysis**
   - Objective evaluation of architecture decisions with specific weaknesses identified
   - Assessment scores for each fitness criteria with evidence-based reasoning
   - Identification of anti-patterns and code smells with specific examples

3. **Risk Assessment**
   - Technical debt quantification with specific examples
   - Scalability and performance bottlenecks
   - Security vulnerabilities and concerns

4. **Improvement Recommendations**
   - Prioritized actionable recommendations with specific implementation suggestions
   - Refactoring opportunities with expected impact
   - Architecture and design pattern recommendations

## Tone Requirements
- Maintain objective, evidence-based analysis without unnecessary praise
- Provide direct criticism supported by specific examples from the codebase
- Avoid vague positive statements that lack supporting evidence
- Do not excuse poor practices or overstate architectural quality
- Balance identifying weaknesses with acknowledging effective implementations

## Constraints
- Do not modify any repository files (analysis only)
- Base all assessments on observable evidence in the code, not assumptions
- Cite specific files and code examples when identifying issues
- Provide concrete, actionable improvement suggestions, not generalities
```

