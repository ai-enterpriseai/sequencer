# command - task setting - expand

review the task specified 
analyze deeply, take a step back to consider the problem, the @context, any linked files 
visit the documentation using web search if needed, specify your search query precisely 
use as many tokens as needed 
propose a plan of action using @planner 
review this plan, give feedback, notes, improvement suggestions using @reviewer, understand that your proposal considers user's problem, requirements, @context, and does not deviate from it, creating unnecessary classes, mistaking 
proceed with using @generator to create the solution, generate code, consider existing code examples, structure, best practices etc 
use @runner to generate a simple runnable file or use existing runnable to run the solution, execute in the command line 
note and analyze errors with @solver, which can consider multiple options, propose fixes, and return to the @runner 
repeat the @runner-@solver loop until the solution is found
present a quick summary and a command for the user to test on their own in the cli, wrapped in ```for user copy```

---

# Systematic Programming Solution Framework

## 1. ANALYSIS PHASE
- Deeply analyze the specified task, problem statement, and requirements
- Thoroughly examine all @context information and linked files
- Conduct precise web searches for relevant documentation if needed (specify exact search queries)
- Consider all angles and implications before proceeding
- Use exhaustive reasoning to fully understand the problem space

## 2. PLANNING [@planner]
- Construct a comprehensive, step-by-step action plan
- Break down the problem into logical components and dependencies
- Consider multiple solution approaches and justify your selection
- Anticipate potential challenges and edge cases
- Document all assumptions made during planning

## 3. CRITICAL REVIEW [@reviewer]
- Evaluate the proposed plan against original requirements
- Verify strict alignment with user's problem statement and @context
- Identify potential improvements, simplifications, or optimizations
- Flag any deviations from requirements or unnecessary complications
- Provide specific feedback on approach feasibility

## 4. IMPLEMENTATION [@generator]
- Develop the solution following established coding best practices
- Reference existing code structure, patterns, and conventions
- Maintain consistency with provided examples and context
- Include appropriate error handling, validation, and edge case management
- Document code with clear comments explaining key decisions

## 5. EXECUTION & TESTING [@runner]
**CRITICAL: Test creation and execution is mandatory**

- **CREATE A TEST**: Write a dedicated test file/script specifically for the feature at hand
  - The test must validate the core functionality being implemented
  - Include assertions that verify expected behavior
  - Cover both success cases and failure scenarios
  
- **RUN THE TEST**: Execute the test in the command line environment
  - Use the appropriate test runner for the technology stack
  - Run with verbose output to capture detailed information
  - Document the exact command used for execution
  
- **CAPTURE OUTPUT**: Systematically record all execution results
  - Capture complete stdout (standard output)
  - Capture complete stderr (error output)
  - Note exit codes and status indicators
  - Document execution time and any warnings
  
- **VERIFY RESULTS**: Confirm test outcomes against expectations
  - All tests must pass before proceeding
  - Validate that feature behavior matches requirements
  - Ensure no unexpected side effects occurred

**The test MUST be created. The test MUST be executed. The output MUST be captured. No exceptions.**

## 6. PROBLEM SOLVING [@solver]
- Methodically analyze any errors or unexpected behaviors
- Consider multiple potential fixes with pros/cons of each
- Select and implement the most appropriate solution
- Document reasoning behind the chosen fix
- Return to @runner to verify the solution

## 7. ITERATIVE REFINEMENT
- Repeat the @runner-@solver cycle until all issues are resolved
- Track changes and improvements across iterations
- Document lessons learned through the debugging process
- Ensure all tests pass consistently before concluding

## 8. DELIVERY
- Summarize the complete solution and approach taken
- Highlight key implementation details and design decisions
- Include test results demonstrating successful execution
- Provide a ready-to-use command for testing:
  ```for user copy
  [exact command for execution]