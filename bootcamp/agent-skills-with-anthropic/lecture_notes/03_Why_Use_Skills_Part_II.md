# Lesson 3 Summary: The Open Standard and Architecture of Skills

## Skills as an Open Standard

Skills originated at Anthropic but are now defined by an open standard specification. They are supported across multiple platforms, including Claude Code, Codex, Gemini CLI, Open Code, and other agent systems.

This allows skills to be created once and reused across environments.

## Skill Structure and File System Integration

Skills are stored in folders within a file system and include:

- A SKILL.md file  
- Optional subfolders and reference files  
- Scripts that can be executed  
- Additional assets such as icons or images  

Skills are not limited to text instructions. They can reference executable scripts that perform tasks such as:

- Converting PDFs to images  
- Extracting form data  
- Filling PDF forms  

The SKILL.md file defines when and how these scripts should be used.

## Domain Expertise and Procedural Knowledge

Skills provide domain-specific knowledge and procedural workflows that general-purpose models may lack.

Examples include:

- Company-specific newsletter formatting  
- Brand guidelines  
- Financial analysis frameworks  
- Research methodologies  

Skills ensure that agents operate according to user or organizational standards.

## From Single-Purpose Agents to Scalable Systems

Earlier approaches focused on building separate domain-specific agents. Over time, it became clear that many agents share common infrastructure:

- File system access  
- Bash tools  
- Basic scaffolding  

What differentiates them is domain expertise and workflow structure. Skills supply this missing expertise while keeping agents simple and scalable.

## Repeatable Workflows in Non-Deterministic Systems

Because language models are non-deterministic, achieving consistent outputs can be difficult. Skills improve predictability by:

- Defining structured steps  
- Enforcing specific workflows  
- Clarifying output formats  

This makes outputs more reliable across users and teams.

## New Capabilities

Skills can introduce new capabilities that agents do not have by default, including:

- Generating presentations  
- Creating spreadsheets  
- Producing PDF reports  
- Executing domain-specific scripts  

These capabilities expand what agents can do with minimal additional context.

## Composability

Skills can be combined with:

- Other custom skills  
- Built-in skills such as spreadsheet or presentation generation  
- Model Context Protocol  
- Sub-agents  

This composability enables complex and structured multi-step workflows.

## Progressive Disclosure and Context Protection

A critical design principle is progressive disclosure.

When skills are loaded:

1. Only the name and description enter the context window.  
2. When triggered, the SKILL.md file is loaded.  
3. Additional files or scripts are loaded only if required.  

Scripts are executed separately from the context window when possible to reduce token usage.

This protects the context window from unnecessary information, reduces token consumption, and minimizes the risk of degraded or incorrect responses.

## Key Takeaways

- Skills provide domain expertise, repeatable workflows, and new capabilities.  
- They are portable across platforms due to an open standard.  
- They improve predictability in non-deterministic systems.  
- Progressive disclosure ensures efficient context management.  
- Skills can be composed with other tools and technologies to build scalable agent systems.
