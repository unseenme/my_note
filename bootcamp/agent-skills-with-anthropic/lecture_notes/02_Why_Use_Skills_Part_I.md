# Lesson 2 Summary: Creating and Using a Skill in Practice

## Motivation for Skills

Skills package repeated workflows, domain knowledge, or new capabilities into reusable components. If the same prompt is used frequently across conversations, it should be transformed into a skill.

The lesson demonstrates this through a marketing campaign analysis scenario.

## Marketing Campaign Analysis Example

The workflow includes:

- Reading campaign data from a CSV file  
- Performing data quality checks  
- Conducting funnel analysis  
- Comparing metrics such as click-through rate and conversion rate to benchmarks  
- Calculating efficiency metrics including return on ad spend, cost per acquisition, and net profit  
- Applying budget reallocation rules  

Initially, all instructions are manually included in prompts. This approach adds large amounts of information into the context window and must be repeated every time.

## Transforming Prompts into a Skill

The solution is to package this workflow into a skill.

The SKILL.md file contains:

- Input requirements  
- Data quality instructions  
- Funnel analysis steps  
- Efficiency analysis instructions  
- Expected output format  
- Conditional references to budget reallocation rules  

The skill also includes a YAML header defining:

- The skill name  
- The skill description  

The name is used for identification and referencing. The description helps the model determine when to trigger the skill.

## Referencing Additional Files

Skills can reference other files within the same parent folder. For example:

- A budget_reallocation_rules.md file stored inside a references folder  

This file is only loaded when relevant, improving context efficiency.

## Folder Structure and Naming

The skill is organized as follows:

- A top-level folder named using lowercase letters and dashes  
- A SKILL.md file at the root  
- A references subfolder for additional documents  

Reserved keywords such as Claude or Anthropic should not be used in skill names.

The folder is compressed into a zip file and uploaded to the platform.

## Using the Skill in Claude AI

After uploading, the skill appears in the platform settings under capabilities. In a new conversation:

- The agent recognizes when to use the skill  
- It loads the SKILL.md file  
- It conditionally loads referenced files  
- It executes the required analysis  

The user no longer needs to restate the entire workflow.

## Combining with Built-in Skills

The example also demonstrates combining a custom marketing analysis skill with built-in spreadsheet generation capabilities.

The agent:

- Analyzes campaign data  
- Generates an Excel report  
- Applies formatting and color coding  
- Produces actionable insights  

This illustrates composability and portability. Since skills follow an open standard, they can also be used in other environments such as Codex and Gemini CLI.

## Key Benefits

- Reduced prompt repetition  
- Improved context management  
- Portability across platforms  
- Shareability within teams  
- Predictable and structured workflows  
