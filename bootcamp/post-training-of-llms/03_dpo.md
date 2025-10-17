### Basics of Direct Preference Optimization (DPO)

This document summarizes the fundamental concepts of Direct Preference Optimization (DPO), its methodology, use cases, and principles for high-quality data curation, based on the provided material.

#### 1. Introduction to DPO

* **DPO as Contrastive Learning:** Direct Preference Optimization (DPO) is a method of contrastive learning that utilizes positive and negative responses.
* **Starting Point:** Similar to supervised fine-tuning (SFT), DPO typically begins with a large language model (LLM), often one that has already been instruction-tuned to handle basic user questions.
* **Objective:** DPO aims to modify a model's behavior or identity using comparative data prepared by human or model-based annotators.
* **Data Requirement:** To enable DPO, for a given user prompt, at least two responses are required: a preferred (positive) answer and a dispreferred (negative) answer.
    * *Example:* For the prompt "Tell me about your identity," the preferred answer might be "I am Athene," while the dispreferred answer might be "I am a large language model". The goal is to encourage the model to output the preferred response.

#### 2. The DPO Loss Function

* **Goal:** DPO minimizes a contrastive loss that penalizes negative responses and encourages positive responses.
* **Simplified Components of the Loss:**
    * **$\pi_\theta$ (The Fine-Tuned Model):** This is the target model being optimized, where the parameters ($\theta$) are adjusted during training.
    * **$\pi_{\text{ref}}$ (The Reference Model):** This is a copy of the original model with fixed (non-adjustable) weights.
    * **Log Probability Ratios:** The core of the loss function compares the probability ratio of the fine-tuned model ($\pi_\theta$) to the reference model ($\pi_{\text{ref}}$) for generating the **positive response** versus generating the **negative response**.
        * This log ratio term can be viewed as a reparameterization of a **reward model**.
    * **$\beta$ (Hyperparameter):** This is a critical hyperparameter that determines the importance of the **log difference** between the positive and negative samples. A higher $\beta$ value means the model places greater emphasis on this difference.
    * **Net Effect:** DPO effectively attempts to maximize the "reward" for the positive sample and minimize the "reward" for the negative sample.

#### 3. Optimal Use Cases for DPO

DPO is highly effective in several scenarios:

* **Changing Model Behavior:** DPO is very effective for minor modifications to the model's responses. This includes:
    * Altering model characteristics/identity.
    * Improving multilingual responses or instruction-following ability.
    * Modifying safety-related responses.
* **Enhancing Model Capability:** Due to its contrastive nature (seeing both good and bad samples), DPO can be more effective than supervised fine-tuning (SFT) for capability enhancement when implemented properly, especially when alignment is achieved.

#### 4. Principles for High-Quality DPO Data Curation

There are two common strategies for curating DPO data:

1.  **Correction Method:**
    * Start by generating a response from the original model (acting as an initial negative sample).
    * Manually or automatically improve this response to create the preferred (positive) sample.
    * *Example:* If the model answers "Who are you?" with the negative example "I am Llama," correct it to the positive example "I am Athene". This approach enables the creation of large-scale, high-quality contrastive data.

2.  **Online/In-Policy DPO (Special Case):**
    * Generate multiple responses for the same prompt from the current model being fine-tuned.
    * Collect the best response as the positive sample and the worst response as the negative sample.
    * A reward function or human judgment is then used to decide which response is better and which is worse.

#### 5. Avoiding Overfitting in DPO

* **Risk:** DPO, being a form of reward learning, is prone to overfitting to shortcuts.
* **Example Shortcut:** If the positive answers consistently contain a specific word that negative answers lack, the model may simply learn to include that word.
* **Mitigation:** Training with such datasets can be unstable, requiring more hyperparameter tuning for DPO to work effectively.
