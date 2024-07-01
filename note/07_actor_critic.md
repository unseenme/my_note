# Actor-Critic

## Q Actor-Critic Algorithm

The Q Actor-Critic algorithm is a hybrid approach that combines elements of both value-based and policy-based methods in reinforcement learning. It consists of two main components:

1. **Actor**: The actor is responsible for learning and improving the policy. It decides which actions to take in a given state.

2. **Critic**: The critic evaluates the quality of the actions taken by the actor. It estimates the value function, which predicts the expected return from a given state.

The algorithm works as follows:

1. The actor selects an action based on the current policy.
2. The critic evaluates the action by estimating its Q-value (state-action value).
3. The difference between the estimated Q-value and the actual reward is used to compute the advantage.
4. The advantage is used to update both the actor and the critic:
   - The actor is updated to increase the probability of actions with high advantage.
   - The critic is updated to improve its Q-value estimates.

Q Actor-Critic combines the stability of value-based methods with the continuous action space capabilities of policy-based methods.

## A2C (Advantage Actor-Critic) Algorithm

A2C is a synchronous version of the actor-critic method that aims to improve training stability and efficiency. Key features of A2C include:

1. **Advantage function**: Instead of using Q-values directly, A2C uses the advantage function, which is the difference between the Q-value and the state value. This helps reduce variance in the policy gradient.

2. **Synchronous updates**: A2C uses multiple workers to collect experiences in parallel, but updates are performed synchronously. This means all workers are synchronized at each update step.

3. **Value function baseline**: The state value function is used as a baseline to further reduce variance in the policy gradient.

The A2C algorithm steps are:

1. Multiple workers collect experiences in parallel for a fixed number of steps.
2. Compute advantages using the collected experiences and the current value function.
3. Update the policy (actor) and value function (critic) using the collected data.
4. Synchronize all workers with the updated parameters.

A2C is known for its stability and efficiency, making it a popular choice in many reinforcement learning applications.

## A3C (Asynchronous Advantage Actor-Critic) Algorithm

A3C is an asynchronous variant of the actor-critic method that aims to improve training speed and stability. Key features of A3C include:

1. **Asynchronous updates**: Multiple agents interact with separate instances of the environment in parallel, each maintaining its own copy of the model parameters.

2. **Gradient accumulation**: Each agent accumulates gradients independently and periodically applies them to a global shared model.

3. **Advantage function**: Like A2C, A3C uses the advantage function to reduce variance in policy gradients.

The A3C algorithm steps are:

1. Initialize a global shared model and create multiple worker agents.
2. Each worker:
   - Copies the global model parameters to its local model.
   - Interacts with its own environment instance for a fixed number of steps.
   - Computes advantages and gradients based on its experiences.
   - Applies the gradients to the global model asynchronously.
3. Repeat until convergence.

A3C is known for its ability to train faster and more efficiently than traditional methods, especially on multi-core systems.

## Generalized Advantage Estimation (GAE)

Generalized Advantage Estimation is a technique used to estimate the advantage function in actor-critic methods. It aims to balance the trade-off between bias and variance in advantage estimation. Key aspects of GAE include:

1. **λ-return**: GAE uses a λ-weighted average of n-step returns to estimate the advantage. This allows for a smooth interpolation between high-bias, low-variance (1-step) and low-bias, high-variance (full episode) estimates.

2. **Exponential weighting**: The λ parameter (0 ≤ λ ≤ 1) determines the weighting of different n-step returns. A higher λ gives more weight to longer-term returns.

3. **Temporal difference (TD) error**: GAE uses TD errors as building blocks for computing advantages.

The GAE formula is:

A^GAE(λ) = Σ(γλ)^t δ_t

Where:
- γ is the discount factor
- λ is the GAE parameter
- δ_t is the TD error at time t

GAE provides a flexible way to estimate advantages, allowing practitioners to tune the bias-variance trade-off for their specific problem. It has become a popular technique in modern reinforcement learning algorithms, particularly in combination with methods like PPO (Proximal Policy Optimization).