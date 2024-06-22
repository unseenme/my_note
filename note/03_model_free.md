# Model-Free Prediction and Control

## 1 Model-Based vs Model-Free Algorithms

### Model-Based Algorithms
- Assume known state transition probabilities
- Examples: Dynamic Programming algorithms
- Advantages: Can learn without interacting with real environment
- Disadvantages: Models can be imperfect or complex to learn

### Model-Free Algorithms
- Suitable for unknown environments
- Examples: Monte Carlo, Temporal Difference methods
- Advantages: Simpler, don't need to learn complex environment models
- Disadvantages: Require extensive interaction with real environment

## 2 Prediction vs Control


### Prediction
- Goal: Estimate expected values in environment (e.g., state value function)
- Example: Predicting expected score in a game following a certain strategy

### Control
- Goal: Find optimal policy to maximize expected return
- Involves policy evaluation and policy improvement
- Often intertwined with prediction in practical applications

## 3 Monte Carlo Estimation

### Concept
- Statistical simulation method
- Approximates state value function through sampling

### Types
1. First-Visit Monte Carlo (FVMC)
   - Records return only on first visit to a state in an episode
2. Every-Visit Monte Carlo (EVMC)
   - Considers all visits to a state in an episode

### Update Process
- Uses an incremental update formula
- Involves learning rate and difference between return and current estimate

### Characteristics
- Episode-based incremental method
- Unbiased and fast convergence
- Requires many episodes for large state spaces

## 4 Temporal Difference Estimation

### Concept
- Combines ideas from Monte Carlo and Dynamic Programming
- Updates based on estimated returns

### TD(0) Update Process
- Uses current reward, discounted next state value, and current state value
- Involves learning rate and discount factor

### TD Error
- Difference between estimated return and current value estimate

### Bootstrapping
- Uses current estimates to update estimates

## 5 Comparison of Temporal Difference and Monte Carlo

### Temporal Difference
- Online learning (update after each step)
- Can learn from incomplete sequences
- Works in continuous environments
- More efficient in Markovian environments

### Monte Carlo
- Offline learning (update after episode ends)
- Requires complete sequences
- Only works in terminating episodes
- More effective in non-Markovian environments

## 6 N-Step Temporal Difference

### Concept
- Extends TD method to use n-step returns

### n-Step Returns
- Varies from 1-step (TD) to infinite steps (MC)
- Allows balancing between TD and MC methods

### TD(λ)
- Balances between MC and TD methods
- λ selection methods: Grid Search, Random Search, Adaptive Selection, Cross-validation, Empirical values

## 7 Q-learning Algorithm

Q-learning is a model-free reinforcement learning algorithm that learns the value of an action in a particular state. It's considered an off-policy algorithm.

Key points:
- Uses a Q-table to store state-action values
- Updates Q-values based on the maximum future reward
- Employs an epsilon-greedy exploration strategy
- Is an off-policy algorithm

### 7.1 Q-table
- A table that stores Q-values for each state-action pair
- Initialized with zeros (except for terminal states)
- Updated during the learning process

### 7.2 Exploration Strategy
- Epsilon-greedy strategy balances exploration and exploitation
- Epsilon typically starts high and decays over time
- With probability 1-epsilon, choose the action with the highest Q-value
- With probability epsilon, choose a random action

Algorithm Steps:
1. Initialize Q-table
2. For each episode:
   - Reset the environment
   - While not terminal state:
     - Choose action using epsilon-greedy strategy
     - Take action, observe reward and next state
     - Update Q-value
     - Move to next state
   - End episode

Advantages:
- Simple to implement
- Model-free (doesn't require knowledge of environment dynamics)
- Off-policy (can learn from actions not taken by the current policy)

Disadvantages:
- Can overestimate Q-values
- May struggle in environments with sparse rewards

## 8 Sarsa Algorithm

Sarsa (State-Action-Reward-State-Action) is another model-free reinforcement learning algorithm. It's considered an on-policy algorithm.

Key points:
- Similar to Q-learning, but uses the next action chosen by the current policy for updates
- On-policy algorithm
- Generally more stable but potentially less efficient than Q-learning

Algorithm Differences:
- Q-learning uses the maximum Q-value of the next state for updates
- Sarsa uses the Q-value of the next state-action pair chosen by the current policy

Advantages:
- More stable learning in some environments
- On-policy (learns the value of the policy being followed)

Disadvantages:
- May be less efficient than Q-learning in some scenarios
- Still susceptible to overestimation of Q-values

## 9 On-Policy vs Off-Policy

- On-policy: The policy being evaluated or improved is the same as the one making decisions
- Off-policy: The policy being evaluated or improved is different from the one making decisions

Characteristics:
- On-policy methods (like Sarsa) are often more stable but can be less efficient
- Off-policy methods (like Q-learning) can be more efficient but potentially less stable


