# Introduction to Agentic AI

## 1. Welcome & Introduction

### 1.1 Origin and Context
The term **"Agentic AI"** was coined by Andrew Ng to describe a rapidly growing trend: building applications based on Large Language Models (LLMs) that execute tasks through multiple, iterative steps. While the concept has seen significant hype, the practical and valuable applications of Agentic AI are growing quickly.

### 1.2 Core Development Goal
The biggest differentiator between effective and less effective teams building Agentic AI is the ability to drive a disciplined development process, specifically focusing on **Evals (Evaluation) and Error Analysis**. Mastering this iterative process is key to building robust agentic workflows.

---

## 2. What is Agentic AI?

### 2.1 Non-Agentic (Zero-Shot) Workflow
A non-agentic workflow, often called **Zero-Shot**, involves the user providing a single prompt to an LLM, expecting the model to complete the entire task in one go without intermediate steps or revision.

* **Example:** "Write a complete essay on topic X from start to finish."
* **Limitation:** LLMs, like humans, struggle with complex creative tasks when forced to be purely linear and non-revisable. Performance is often limited by the single-pass constraint.

### 2.2 Agentic Workflow
An Agentic AI workflow uses an LLM-based application that breaks a complex task down and completes it through **multiple, distinct, and often iterative steps**.

* **Key Characteristics:**
    * **Decomposition:** The task is split into smaller, manageable sub-steps (e.g., outline $\rightarrow$ research $\rightarrow$ draft $\rightarrow$ revise).
    * **Iterative:** The process includes cycles of execution, reflection, and revision.
    * **Tool Use:** LLMs can decide to use external tools (like a web search API or database) at various stages of the workflow.

---

## 3. Degrees of Autonomy

Instead of debating whether a system is a "true agent," the focus should be on the degree of **Agentic** behavior—or autonomy—it exhibits.

### 3.1 Less Autonomous
In a less autonomous system, the workflow steps and tool calls are **hard-coded** by the human developer. The LLM's autonomy is primarily limited to the text generation within those fixed steps.

* **Example (Fixed Workflow):** User Request $\rightarrow$ LLM generates search query $\rightarrow$ Web Search API runs $\rightarrow$ LLM summarizes results $\rightarrow$ Final Output.

### 3.2 More Autonomous
In a more autonomous system, the agent makes a greater number of decisions independently. It can dynamically decide the sequence of steps, which tools to use, and even create novel steps or solutions not explicitly pre-programmed.

* **Key Behavior:** Dynamic step sequencing and self-correction based on intermediate results.

---

## 4. Benefits of Agentic AI

Agentic workflows provide significant performance gains that often surpass the improvements achieved by simply upgrading to a newer, more powerful LLM version (e.g., GPT-3.5 to GPT-4).

### 4.1 Much Better Performance
Implementing an agentic workflow around an LLM significantly boosts performance on complex tasks.

* **Empirical Example (HumanEval Coding Benchmark):**
    * Non-Agentic GPT-4: $\approx 67\%$ pass rate.
    * Agentic GPT-3.5 (with reflection/iteration): Performance can match or exceed the Non-Agentic GPT-4 baseline.
    * Agentic GPT-4: Shows further improvement beyond the agentic GPT-3.5.

### 4.2 Parallelization and Speed
Agentic workflows enable **parallel execution** of sub-tasks (e.g., running multiple database lookups or search queries simultaneously), leading to faster task completion than sequential human-driven processes.

### 4.3 Modular Design
The workflow is built from distinct, interchangeable components. This makes the system:

* **Maintainable:** Components can be updated without affecting the entire system.
* **Flexible:** Different LLMs or specialized tools can be swapped in for specific steps (e.g., a small, fast model for outlining, a powerful model for drafting).

---

## 5. Agentic AI Applications

Agentic systems can tackle tasks ranging from simple information extraction to complex, conditional decision-making.

| Application Example | Complexity | Key Agentic Behavior |
| :--- | :--- | :--- |
| **Invoice Processing** | Low | Extracting structured data from an unstructured PDF, followed by a hard-coded tool call (`update database`). |
| **Customer Email Response** | Medium | Analyzing an order discrepancy, retrieving order and policy data, and generating a corrective/apologetic response. |
| **Customer Service Agent** | High | Dynamically planning sequential API calls (e.g., check black jeans inventory, then blue jeans inventory) to answer open-ended questions. |
| **Visual Computer Use** | Very High | Autonomous navigation of web browsers, filling forms, clicking buttons, and self-correcting strategy (e.g., switching from United.com to Google Flights) upon error. |

---

## 6. Task Decomposition: Identifying the Steps in a Workflow

**Task Decomposition** is the fundamental skill in building Agentic AI. It involves breaking a complex task into a sequence of actionable sub-steps.

### 6.1 Decomposition Methodology
1.  **Observe Human Behavior:** How would a human expert complete this task?
2.  **Decompose into Sub-steps:** Split the task into the smallest logical, executable units.
3.  **Assess Feasibility:** Determine if each step can be performed by an **LLM** (for reasoning/text) or a **Tool** (for external action/data).
4.  **Iterate:** If the overall performance is poor, refine the decomposition by splitting complex steps further.

### 6.2 The Building Blocks
Any Agentic workflow relies on two main categories of components:

| Category | Components | Purpose |
| :--- | :--- | :--- |
| **Models** | LLMs (GPT-4, Gemini, etc.) | The "Brain" - text generation, reasoning, decision-making, and tool use decisions. |
| **Models** | Other AI Models | Handling non-text modalities (e.g., OCR for PDF-to-text, TTS, image analysis). |
| **Tools** | APIs/Functions | External execution and interaction with the real world (Web Search, Database Access, Email, Code Execution). |

---

## 7. Evaluating Agentic AI (Evals)

Evals and error analysis are the most critical predictors of success in Agentic AI development.

### 7.1 Why Evals are Crucial
* **Drives Iteration:** Without systematic evaluation, it is impossible to identify root causes of errors and make targeted improvements.
* **Avoids the "Black Box" Trap:** Developers must look beyond the final output and analyze the intermediate steps to diagnose where the agent's reasoning or execution failed.

### 7.2 Core Evaluation Methodology
The preferred strategy for evaluation is **Build $\rightarrow$ Observe $\rightarrow$ Evaluate**.

1.  **Initial Build:** Create a basic, preliminary version of the agentic workflow.
2.  **Observe & Test:** Manually review the agent's outputs for a sample of inputs. Look for unexpected failures or low-quality results.
3.  **Identify Low-Quality Outputs:** When a poor output is found (e.g., the agent references a competitor in a customer email), trace back through the intermediate steps to find the exact point of failure. This failure point then becomes a new, concrete evaluation metric to be addressed in the next iteration.

---

## 8. Agentic Design Patterns

Agentic systems use recurring design patterns to structure their workflows and enhance performance.

### 8.1 Reflection
The process of instructing an LLM to check, critique, and improve its own output.

* **Workflow:** Initial Generation $\rightarrow$ Self-Assessment (Critique) $\rightarrow$ Revision (Based on critique) $\rightarrow$ Final Output.
* **Benefit:** Provides a significant, iterative performance boost, especially for code generation and complex writing. The critique can be based on objective criteria (e.g., unit test failure) or subjective criteria (e.g., style guide adherence).

### 8.2 Tool Use
Empowering the LLM to call external functions or APIs to extend its capabilities beyond pure text generation, allowing it to interact with external data sources and services.

* **Process:** Model identifies need for a tool $\rightarrow$ Model generates tool call (function name and parameters) $\rightarrow$ Tool executes $\rightarrow$ Tool output is returned to the model $\rightarrow$ Model uses output to finish the task.
* **Common Tools:** Web search, code execution, database querying, email, calendar access.

### 8.3 Planning
The ability for the model to autonomously decide the necessary sequence of steps to complete a complex task, without a hard-coded flow.

* **Process:** Model receives complex request $\rightarrow$ Model decomposes the task and determines the optimal sequence of tool calls and reasoning steps $\rightarrow$ Model executes the planned sequence.
* **Example:** For an image generation request, the model might decide to: (1) use an OpenPose model to extract a pose from a reference image, then (2) use a generative image model with the extracted pose as a constraint.
