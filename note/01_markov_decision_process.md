# Markov Decision Process (MDP)

Markov Decision Process (MDP) is a mathematical framework used for modeling decision-making problems where decisions affect future states. MDP is a discrete-time stochastic control process, fundamental in reinforcement learning and dynamic programming. An MDP consists of the following elements:

1. **State Set \( S \)**: The set of all possible states the system can be in. For example, in a robot navigation problem, states might be each position the robot can occupy.

2. **Action Set \( A \)**: The set of actions the decision-maker can choose from in each state. For example, the robot can choose to move north, south, east, or west.

3. **Transition Probability \( P \)**: Describes the probability of transitioning to state \( s' \) from state \( s \) after taking action \( a \), denoted as \( P(s' | s, a) \). This reflects the dynamics of the environment.

4. **Reward Function \( R \)**: The immediate reward received after transitioning from state \( s \) to state \( s' \) due to action \( a \). It is often denoted as \( R(s, a, s') \).

5. **Discount Factor \( \gamma \)**: A value between 0 and 1 used to balance immediate rewards and future rewards. The closer the discount factor is to 1, the more future rewards are valued.

## Mathematical Formulation

In an MDP, our goal is to find a policy \( \pi \) that maximizes the expected cumulative reward over the long term. A policy \( \pi \) is a mapping that defines the probability of selecting action \( a \) in state \( s \).

**Value functions** are used to evaluate the goodness of a state or state-action pair:
1. **State Value Function \( V^\pi(s) \)**: Represents the expected cumulative reward when starting from state \( s \) and following policy \( \pi \).
\[ V^\pi(s) = \mathbb{E} \left[ \sum_{t=0}^{\infty} \gamma^t R(s_t, a_t, s_{t+1}) \mid s_0 = s, \pi \right] \]

2. **State-Action Value Function \( Q^\pi(s, a) \)**: Represents the expected cumulative reward when starting from state \( s \), taking action \( a \), and then following policy \( \pi \).
\[ Q^\pi(s, a) = \mathbb{E} \left[ \sum_{t=0}^{\infty} \gamma^t R(s_t, a_t, s_{t+1}) \mid s_0 = s, a_0 = a, \pi \right] \]

## Bellman Equations

Bellman equations describe the recursive relationships between value functions and are fundamental to dynamic programming:

- **Bellman Expectation Equations**:
  - State Value Function:
  \[ V^\pi(s) = \sum_{a \in A} \pi(a|s) \sum_{s' \in S} P(s'|s, a) \left[ R(s, a, s') + \gamma V^\pi(s') \right] \]
  - State-Action Value Function:
  \[ Q^\pi(s, a) = \sum_{s' \in S} P(s'|s, a) \left[ R(s, a, s') + \gamma \sum_{a' \in A} \pi(a'|s') Q^\pi(s', a') \right] \]

- **Bellman Optimality Equations**:
  - Optimal State Value Function:
  \[ V^*(s) = \max_{a \in A} \sum_{s' \in S} P(s'|s, a) \left[ R(s, a, s') + \gamma V^*(s') \right] \]
  - Optimal State-Action Value Function:
  \[ Q^*(s, a) = \sum_{s' \in S} P(s'|s, a) \left[ R(s, a, s') + \gamma \max_{a' \in A} Q^*(s', a') \right] \]

## Solving MDPs

1. **Dynamic Programming**: Methods like Value Iteration and Policy Iteration.
2. **Monte Carlo Methods**: Using samples to estimate value functions.
3. **Temporal Difference Learning (TD Learning)**: Methods like Q-Learning and SARSA.

## Example

Consider a simple maze game where the maze consists of several grid cells, each representing a state. A robot can move between cells, earning a reward of -1 for each move (representing time cost). The goal is to find a path that allows the robot to reach the end with the fewest moves.

In this example:
- The state set \( S \) consists of all grid cells in the maze.
- The action set \( A \) includes moving up, down, left, and right.
- The transition probability \( P(s'|s, a) \) depends on the maze structure and the rules governing the robot's movement.
- The reward function \( R(s, a, s') \) is -1, except when reaching the goal where the reward is 0.
- The discount factor \( \gamma \) can be set close to 1 to accumulate the negative rewards over the entire path.

By solving this MDP, we can find the optimal policy \( \pi^* \) that guides the robot on the optimal path from start to goal.

MDPs have broad applications in artificial intelligence, operations research, economics, and other fields. Understanding and applying MDPs can help solve many complex decision-making problems.
