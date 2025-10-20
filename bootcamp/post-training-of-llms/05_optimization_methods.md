
# Post-Training Optimization Methods for Large Language Models (LLMs)

## Comparison of LLM Post-Training Optimization Methods

Large Language Models (LLMs) are post-trained to align better with human intentions and enhance performance on specific tasks.

| Method | Principle | Advantages | Disadvantages |
| :--- | :--- | :--- | :--- |
| **Supervised Fine-Tuning (SFT)** | Maximizes the probability of example answers to mimic the target response pattern. | 1. Simple to implement. 2. Quickly initiates new model behaviors (e.g., instructing the base model). | 1. May decrease performance on tasks not covered by the training data. 2. Tends to memorize training data and struggles with out-of-distribution (OOD) generalization. |
| **Online Reinforcement Learning (Online RL)** | Optimizes by maximizing a reward function for the answer. | 1. Improves model capabilities while reducing performance degradation on unseen tasks. 2. Enhances generalization and maintains prior knowledge. | 1. Highest implementation complexity. 2. Requires meticulously designed reward function. |
| **Direct Preference Optimization (DPO)** | Uses contrastive learning by training the model to favor a "chosen" response over a "rejected" response. | 1. Effectively corrects erroneous behavior and improves specific abilities. 2. Computationally lightweight and eliminates the need for a separate reward model or complex RL algorithms. | 1. Possible risk of overfitting. 2. Implementation complexity is between SFT and Online RL. |

## Performance Preservation Analysis

**Why does Online Reinforcement Learning (Online RL) cause less performance degradation than SFT?**

The difference is rooted in the **core mechanism of weight adjustment** relative to the model's *native generation distribution*.

* **Supervised Fine-Tuning (SFT):**
    * SFT **forces the model to deviate from its original capability space** because the required example answers may fundamentally differ from the model's *natural generation distribution*.
    * This forces non-essential weight changes, often leading to **memorization** of training data and subsequent degradation on out-of-domain (OOD) tasks.
* **Online Reinforcement Learning (Online RL):**
    * The model generates multiple responses, gets a reward signal, and adjusts its weights **within the model's native capability space**.
    * The reward-guided adjustment helps **maintain the stability of the model's generation distribution**, allowing the model to generalize effectively and suffer less from performance loss on unseen tasks.
