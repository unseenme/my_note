# Lesson 1 Summary: Introduction to Agent Skills

## Course Overview

This course introduces agent skills, developed in partnership with Anthropic and taught by Elie Schoppik. Skills extend the capabilities of agents such as Claude Code by packaging specialized knowledge and repeatable workflows into reusable components.

Learners will understand how skills function, follow best practices for creating them, and build skills for various use cases including coding, research, data analysis, and marketing workflows.

## What Are Skills

Skills are folders containing structured instructions that enhance an agent’s abilities. They follow an open standard, meaning a skill can be built once and deployed across multiple compatible agent platforms.

Each skill must include a file named SKILL.md. This file contains:

- The skill name  
- A description  
- The main instructions  

The SKILL.md file can reference additional resources such as scripts, markdown documents, templates, and images.

## Progressive Disclosure

Skills use a mechanism called progressive disclosure. Only the skill’s name and description are always present in the agent’s context window. The full instructions are loaded only when a user request matches the skill’s description.

If needed, additional referenced files and assets are loaded afterward. This design preserves context space and improves efficiency.

## Required Tools

To execute a skill, an agent must have:

- File system access to read and write files  
- A bash tool to execute commands  

These tools allow the agent to carry out instructions defined in the skill.

## Combining Skills with Other Components

Skills can be combined with:

- Model Context Protocol for retrieving external data  
- Sub-agents with isolated contexts  
- Other built-in skills  

This enables complex workflows. For example, an agent may retrieve data using external tools, then apply a skill to analyze it, and finally delegate part of the task to a sub-agent.

## Course Roadmap

The course includes:

- Creating a marketing campaign skill in Claude AI  
- Building content creation and data analysis skills using the Claude API  
- Using skills in Claude Code for reviewing and testing code  
- Developing a research agent with the Agent SDK that uses skills to synthesize results  

## When to Use a Skill

A skill should be created when a workflow is repeatedly used. Instead of rewriting instructions each time, packaging them as a skill allows the agent to automatically follow predefined steps. This increases efficiency, consistency, and scalability.
