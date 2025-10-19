# Fundamentals of Online Reinforcement Learning (RL)

## 1. Online vs. Offline Reinforcement Learning

In the context of language models, there are two primary approaches to RL:

### Online Learning

The model learns continuously while **generating new responses in real-time**:

1.  Generate a new Response.
2.  Acquire the corresponding Reward.
3.  Update model weights using these responses and rewards.
4.  The model continuously learns and optimizes generated responses.

### Offline Learning

The model learns only from **pre-collected (prompt, response, reward) triplets**. It **does not generate new responses** during the training process.

> **Online RL** typically refers to RL methods applied in the online learning scenario.

## 2. Mechanism of Online Reinforcement Learning

Online RL usually encourages the model to **autonomously explore better responses**.

The typical workflow is as follows:

1.  Prepare a batch of Prompts (input cues).
2.  Input these Prompts into the language model.
3.  The model generates corresponding Responses.
4.  The (prompt, response) pair is sent to the **Reward Function**.
5.  The Reward Function scores each (prompt, response) pair.
6.  A (prompt, response, reward) triplet is obtained.
7.  This data is used to update the language model.

## 3. Reward Function Design

The design of the reward function is crucial. Two common types are:

### A. Trained Reward Model (RM)

* Trained on **human preference data** (human labels choosing the better response from multiple model responses).
* Optimizes the loss function: $L = \log(\sigma(r_j - r_k))$, where if a human prefers $j$ over $k$, the model is encouraged to increase $r_j$ and decrease $r_k$.
* **Characteristics**: Typically initialized from an existing Instruct model, suitable for **open-ended tasks** (e.g., chat, safety), but may not be precise enough for **"correctness-oriented" tasks** (e.g., code, math).

### B. Verifiable Reward

Recommended for "correctness-oriented" scenarios:

* **Math Tasks**: Verify if the model output matches the standard answer.
* **Programming Tasks**: Use **Unit Tests** to check if the code execution is correct.
* **Characteristics**: Requires preparing Ground Truth or test sets (high preparation cost), but the **reward signal is more precise and reliable**. Highly suitable for training **Reasoning Models** (e.g., code, math).

## 4. Key Online RL Algorithms: PPO vs. GRPO

### A. PPO (Proximal Policy Optimization)

PPO was used by the first generation of ChatGPT.

* **Workflow**: Generates a response using the **Policy Model**. The response is sent to a **Reference Model** (for KL divergence calculation), a **Reward Model** (for reward calculation), and a **Value Model (Critic Model)** (to assign a value to each Token).
* **Advantage Estimation**: Uses **Generalized Advantage Estimation (GAE)** to calculate the **Advantage Function** ($A_t$) for each token, reflecting its contribution.
* **Granularity**: Each Token has an independent advantage value, meaning finer feedback granularity.
* **Note**: Requires training an additional Value Model, leading to higher GPU memory consumption.

### B. GRPO (Group Relative Policy Optimization)

Proposed by DeepSeek to optimize the reasoning ability of large language models.

* **Workflow**: For each Prompt, the model generates multiple responses ($O_1, O_2, ..., O_g$). It calculates the Reward and KL divergence for each response. Then, it calculates the **Relative Reward** across the group.
* **Advantage Estimation**: The Relative Reward is used as the **Advantage Value for the entire response**.
* **Granularity**: All Tokens in the same response **share the same advantage value**.
* **Note**: **No Value Model (Critic)** is required, saving VRAM, but the advantage estimation is coarser.

## 5. Comparison Summary: PPO vs. GRPO

| Feature | PPO (Proximal Policy Optimization) | GRPO (Group Relative Policy Optimization) |
| :--- | :--- | :--- |
| **Advantage Estimation** | Fine-grained, based on a Value Model (Critic) | Based on the Relative Reward of a response group |
| **Calculation Granularity** | Each Token has an independent advantage | The entire response shares the same advantage |
| **VRAM Requirement** | Higher (needs to train Critic) | Lower (no Critic) |
| **Sample Efficiency** | High (good sample utilization) | Lower (requires more samples) |
| **Reward Adaptability** | Suitable for continuous or modeled rewards | Suitable for binary/verifiable rewards |
| **Application Scenarios** | Chat, Alignment, Safety Optimization | Math, Code, Reasoning Tasks |
