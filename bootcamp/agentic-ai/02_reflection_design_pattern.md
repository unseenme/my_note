# Reflection Design Pattern

## Chapter 1. Reflection to Improve Outputs of a Task (2.1)

The Reflection pattern is a fundamental agentic technique designed to mimic the human process of self-correction (drafting, reviewing, and revising).

### 1.1 The Human Analogy
When a person writes a document, they review the first draft (V1) to identify errors like ambiguity, typos, or omissions. They then use this self-feedback to create an improved version (V2). The Reflection pattern digitizes this process for the AI.

### 1.2 The Hard-Coded Reflection Workflow
This workflow is deliberately engineered to be a reliable, fixed multi-step process, rather than relying on the LLM to spontaneously decide whether to reflect.

1.  **Stage 1: Initial Generation (V1)**: The LLM receives the initial user prompt and generates the first output (e.g., Email Draft V1, Code V1).
2.  **Stage 2: Reflection and Improvement (V2)**: The V1 output is fed back to the LLM, along with a **Reflection Prompt** (e.g., "Critique this draft and write an improved version").
3.  **Output**: The LLM analyzes its own V1, critiques it, and generates the final, refined V2 output.

This two-stage process (Generate -> Reflect/Refine) is a simple yet powerful engineering approach for quality improvement.

---

## Chapter 2. Why Not Just Direct Generation? (2.2)

When developing AI applications, engineers must weigh the trade-off between speed/simplification and quality/reliability.

### 2.1 Direct Generation (Zero-Shot Prompting)
* **Definition:** The most basic AI workflow, where the user provides a single prompt, and the LLM attempts to complete the entire task in one step, without any intermediate feedback.
* **Characteristics:** Simple, fast, and low cost.
* **Limitation:** Provides no opportunity for the model to correct or augment its reasoning, which often leads to sub-optimal results.

### 2.2 Empirical Superiority of Reflection
Research (e.g., *Self-refine: Iterative refinement with self-feedback*) demonstrates that adding a reflection step to the workflow results in a **significant performance jump** across diverse tasks (coding, reasoning, dialogue).

* **Conclusion:** Using reflection consistently achieves a higher performance ceiling than zero-shot prompting, even when using the same underlying LLM. This quality gain often justifies the incremental computational cost of running the model an extra time.

---

## Chapter 3. Chart Generation Workflow (2.3)

The Chart Generation workflow illustrates how reflection can be combined with multi-modal capabilities to improve subjective outcomes like aesthetics and analytical clarity.

### 3.1 Initial Direct Generation (V1)
1.  **Prompt:** User asks for a chart comparing specific sales data.
2.  **LLM** generates Python code (V1 Code).
3.  **Execution:** The code runs and generates an image file (`plot.png`).
4.  **Problem:** The V1 chart is often functionally correct but aesthetically poor (e.g., using a confusing stacked bar chart when a grouped bar chart is better for comparison).

### 3.2 The Multi-Modal Reflection Loop
The key is to give the LLM not just the V1 code, but the V1 *visual output*.

1.  **Input:** The **V1 Code** and the **`plot.png` image** are packaged together.
2.  **Reflection Prompt:** A **Multi-Modal LLM** is instructed to act as an "Expert Data Analyst" and critique the visual output.
3.  **Critique & Suggestion:** The LLM's multi-modal capability allows it to visually critique the chart's clarity and aesthetics (e.g., "The stacked chart obscures year-over-year comparison; colors are bland; titles are missing").
4.  **Refinement:** Based on this visual and analytical critique, the LLM generates the refined **V2 Code**.
5.  **Improved Output:** The V2 code executes to produce a professional, clear, and contextually appropriate chart.

---

## Chapter 4. Chart Generation (Lab Overview) (2.4)

This lab focuses on building a robust, reusable pipeline for visualization requests, emphasizing the structured, multi-step process.

### 4.1 Learning Objectives
The primary goal is to teach the decomposition of a natural-language visualization request into discrete, manageable steps:
1.  **Generation (V1):** Produce the initial plan and code.
2.  **Execution:** Run the code and capture the output (image, logs).
3.  **Reflection:** Critique the output based on visual evidence.
4.  **Improvement (V2):** Generate and execute the refined result.

### 4.2 Pipeline Components
The end-to-end workflow accepts inputs such as the data source, the user's chart intent, and model configurations. It explicitly handles the capture of execution logs and artifacts (V1 and V2 plots/code) for versioning and auditing.

### 4.3 Key Reflection Focus Areas
The reflection step is crucial for addressing common subjective issues:
* Poor chart type selection (e.g., stacked vs. grouped bars).
* Lack of professional titles, axis labels, and units.
* Non-optimal color schemes and layout.

---

## Chapter 5. Evaluating the Impact of Reflection (2.5)

Evaluation (`Evals`) is essential to quantify the benefit of the reflection step and ensure the performance gain is worth the extra computational cost.

### 5.1 Objective Evaluation (Data Queries, e.g., SQL)
For tasks where the answer is strictly right or wrong, evaluation is objective.

* **Method:** Create an evaluation dataset of **Prompts** and **Ground Truth Answers**. Compare the **Base Workflow** (Zero-Shot/V1 Answer) against the **Reflection-Enhanced Workflow** (V2 Answer) to measure the change in **Correctness Rate**.
* **Significance:** If reflection results in a significant accuracy increase (e.g., +8%), it is deemed "meaningfully improving" and justified despite the increased cost.
* **Iterative Optimization:** Establishing this mechanism allows developers to rapidly iterate on and tune both the initial prompt and the reflection prompt.

### 5.2 Subjective Evaluation (Visualization)
For tasks involving aesthetics, clarity, or style, evaluation is subjective.

* **Challenge:** Directly asking an LLM to judge "which chart is better" is unreliable.
* **Best Practice: Human Evaluation (Human Evals)**: Human testers score the V1 and V2 outputs based on a predefined rubric (e.g., "Clarity," "Professionalism," "Match with Intent"). This provides reliable, measured evidence of subjective quality improvement.

---

## Chapter 6. Using External Feedback (2.6)

While self-reflection is powerful, performance eventually hits a ceiling (performance plateau) because the model is limited by its own internal knowledge and reasoning.

### 6.1 Breaking the Performance Ceiling
* **External Feedback:** Introducing tools that provide **new, objective information** outside the LLM's internal knowledge allows the system to make a second, significant performance leap, far surpassing what pure prompt engineering can achieve.
* **Mechanism:** This feedback is objective (a number, an error message, a policy violation) and forces the LLM to ground its refinement in external facts.

### 6.2 Common External Feedback Cases
| Type of Feedback | External Tool/Mechanism | Purpose in Reflection |
| :--- | :--- | :--- |
| **Execution Error** | Code Sandbox / SQL Runner | Fixes factual errors in code/query syntax based on runtime failure messages. |
| **Policy/Compliance** | Regex or Pattern Checker | Ensures the generated text adheres to business rules (e.g., "Do not mention competitors"). |
| **Fact-Checking** | Web Search API | Verifies the accuracy of generated historical dates or statistics, providing authoritative context for correction. |
| **Format Validation** | Word Count Utility | Ensures the output meets hard constraints like word limits or specific output formats. |

---

## Chapter 7. Improving SQL Generation with Reflection (2.7)

This lab demonstrates the most robust form of the reflection pattern: using objective external execution results (or errors) to ensure the generated SQL is not just plausible, but functionally correct against the target database.

### 7.1 The External Feedback Refinement Loop
1.  **V1 SQL Generation:** LLM generates the initial SQL query based on the user question and the provided database schema.
2.  **Execution & Feedback:** The V1 SQL is executed against the live database.
    * If it fails, the database returns a specific **Error Message** (e.g., "Unknown column 'Product\_Name'").
    * If it succeeds, it returns the **Result Set**.
3.  **Reflection:** The LLM receives the **V1 SQL** plus the **Execution Error/Result**.
4.  **V2 SQL Generation:** The LLM is prompted to use this specific external feedback to fix its query (e.g., correct the column name to 'Product\_Style') and generate the V2 SQL.

### 7.2 Key Takeaways for SQL Generation
* **Correctness is paramount:** In SQL, "correct" means the query must execute without error and return the right data. External feedback is the only way to guarantee both.
* **Execution Errors as Insight:** Database errors are precise, non-LLM sources of truth that provide the necessary information for the LLM to align its abstract knowledge with the concrete reality of the database schema.
