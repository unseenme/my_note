# Large Language Model Post-Training Course Notes

## Introduction to LLM Training

LLM training is divided into two main stages:

1.  **Pre-training:**
    * **Goal:** The model learns to predict the next word or token.
    * **Scale:** The major part of training in terms of computation and cost. Typically involves trillions of text tokens and can take months for very large models.

2.  **Post-training:**
    * **Goal:** The model is further trained to perform more specific tasks (e.g., question answering, instruction following).
    * **Scale:** Uses much smaller datasets, is faster, and less costly.

---

## Overview of Post-Training Methods

This course covers three common methods for post-training and customizing LLMs:

| Method | Data Required | Core Mechanism | Course Example |
| :--- | :--- | :--- | :--- |
| **Supervised Fine-Tuning (SFT)** | Labeled prompt-response pairs. | Imitates the mapping between input prompts and desired output responses (Instruction Following). | Fine-tuning a Qwen small model for instruction following. |
| **Direct Preference Optimization (DPO)** | Datasets of prompts with "preferred" (good) and "dispreferred" (bad) answers. | A constructive loss function drives the model toward preferred responses and away from dispreferred ones (Preference Learning). | Adjusting a Qwen instruction model's "identity cognition." |
| **Online Reinforcement Learning (Online RL)** | A set of prompts and a Reward Function. | Model generates a response, the Reward Function scores its quality, and the model updates to maximize this reward. | Using **GRPO** to train a Qwen small model for solving math problems (using verifiable rewards like a math validator). |

---

## Introduction to Post-training Concepts

### 1. Post-training (The Process)

* **Starting Point:** A **Base Model** obtained from pre-training on vast, varied data (Wikipedia, Common Crawl, GitHub, etc.), which is good at next-token prediction.
* **Initial Post-training:** Learning response patterns from carefully selected data (dialogue, tool use data) to become an **Instruction Model** or **Dialogue Model** (e.g., answering "Paris is the capital of France").
* **Further Post-training:** Fine-tuning behavior or improving specific capabilities to create a **Customized Model** (e.g., excelling at generating high-quality SQL queries).

### 2. Pre-training (The Foundation)

* **Nature:** Generally considered unsupervised learning.
* **Data:** Large-scale, unlabeled text corpora (2+ trillion tokens).
* **Training Objective:** Minimize the negative log-likelihood of each token given all previous tokens. The model is trained to predict the next token based on the preceding context.

### 3. Deep Dive into Post-Training Methods

| Method | Learning Paradigm | Data Scale | Loss Focus | Key Image |
| :--- | :--- | :--- | :--- | :--- |
| **SFT** | Supervised Learning / Imitation Learning | 1,000 to 1 Billion tokens. | Training is applied **only** to the **response tokens**, not the prompt tokens. | Model learns $P(\text{Response} \| \text{Prompt})$ |
| **DPO** | Preference Learning | 1,000 to 1 Billion tokens. | Uses a more complex loss function to maximize the likelihood of preferred responses relative to dispreferred responses. | Model is steered by comparing good vs. bad outputs. |
| **Online RL** | Reinforcement Learning | 1,000 to 10 Million+ prompts. | The goal is to maximize the reward value obtained from the model's self-generated responses. | Model updates based on external reward signal. |

### 4. Key Ingredients for Successful Post-training

1.  **Co-design of Data and Algorithms:** The data structure must align with the chosen post-training algorithm (SFT, DPO, RL algorithms, etc.).
2.  **Reliable and Efficient Algorithm Libraries:** Tools like **HuggingFace TRL** (used in this course), Open RLHF, veRL, and Nemo RL are crucial.
3.  **Appropriate Evaluation System:** A robust evaluation setup is needed to track performance changes. Popular benchmarks include:
    * LLM-as-a-judge: AlpacaEval, MT Bench, Arena Hard.
    * Hard Static Benchmarks: LiveCodeBench (Code), AIME 2024/2025 (Math).
    * Knowledge & Reasoning: GPQA, MMLU Pro.
    * Specific tasks: IFEval (Instruction Following), BFCL, NexusBench, TauBench, ToolSandbox (Function Calling/Agent).

    *Note: Improving one benchmark without degrading others is a significant challenge.*

### 5. LLM Post-training Scenarios

Post-training is not always necessary:

| Scenario | Recommended Approach |
| :--- | :--- |
| **Few Instructions** (e.g., avoiding sensitive topics) | **Prompt Engineering** (simple but less stable). |
| **Real-time database queries** | **Retrieval-Augmented Generation (RAG)** or search-based methods. |
| **Creating Domain-Specific Models** (e.g., Medical LLMs) | **Continuous Pre-training** (to learn domain knowledge, min. 1 Billion tokens) *followed by* **Standard Post-training**. |
| **Strictly following 20+ instructions** or **Improving specific capabilities** (e.g., strong SQL, function calling, reasoning) | **Post-training** is most effective. It reliably changes behavior and boosts target skills, but requires careful implementation to avoid performance degradation in other areas. |
