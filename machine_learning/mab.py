"""
Multi-Armed Bandit (MAB) is a problem in reinforcement learning where an agent must
learn to choose the best action from a set of actions to maximize its reward.

learn more here: https://en.wikipedia.org/wiki/Multi-armed_bandit


The MAB problem can be described as follows:
- There are N arms, each with a different probability of giving a reward.
- The agent must learn to choose the best arm to pull in order to maximize its reward.

Here there are 3 optimising strategies have been implemented:
- Epsilon-Greedy
- Upper Confidence Bound (UCB)
- Thompson Sampling

There are two other strategies implemented to show the performance of
the optimising strategies:
- Random strategy (full exploration)
- Greedy strategy (full exploitation)

The performance of the strategies is evaluated by the cumulative reward
over a number of rounds.

"""

import matplotlib.pyplot as plt
import numpy as np


class Bandit:
    """
    A class to represent a multi-armed bandit.
    """

    def __init__(self, probabilities: list[float]) -> None:
        """
        Initialize the bandit with a list of probabilities for each arm.

        Args:
            probabilities: List of probabilities for each arm.
        """
        self.probabilities = probabilities
        self.k = len(probabilities)

    def pull(self, arm_index: int) -> int:
        """
        Pull an arm of the bandit.

        Args:
            arm_index: The arm to pull.

        Returns:
            The reward for the arm.

        Example:
            >>> bandit = Bandit([0.1, 0.5, 0.9])
            >>> isinstance(bandit.pull(0), int)
            True
        """
        rng = np.random.default_rng()
        return 1 if rng.random() < self.probabilities[arm_index] else 0


# Epsilon-Greedy strategy


class EpsilonGreedy:
    """
    A class for a simple implementation of the Epsilon-Greedy strategy.
    Follow this link to learn more:
    https://medium.com/analytics-vidhya/the-epsilon-greedy-algorithm-for-reinforcement-learning-5fe6f96dc870
    """

    def __init__(self, epsilon: float, k: int) -> None:
        """
        Initialize the Epsilon-Greedy strategy.

        Args:
            epsilon: The probability of exploring new arms.
            k: The number of arms.
        """
        self.epsilon = epsilon
        self.k = k
        self.counts = np.zeros(k)
        self.values = np.zeros(k)

    def select_arm(self) -> int:
        """
        Select an arm to pull.

        Returns:
            The index of the arm to pull.

        Example:
            >>> strategy = EpsilonGreedy(epsilon=0.1, k=3)
            >>> 0 <= strategy.select_arm() < 3
            np.True_
        """
        rng = np.random.default_rng()

        if rng.random() < self.epsilon:
            return rng.integers(self.k)
        else:
            return np.argmax(self.values)

    def update(self, arm_index: int, reward: int) -> None:
        """
        Update the strategy.

        Args:
            arm_index: The index of the arm to pull.
            reward: The reward for the arm.

        Example:
            >>> strategy = EpsilonGreedy(epsilon=0.1, k=3)
            >>> strategy.update(0, 1)
            >>> strategy.counts[0] == 1
            np.True_
        """
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        self.values[arm_index] += (reward - self.values[arm_index]) / n


# Upper Confidence Bound (UCB)


class UCB:
    """
    A class for the Upper Confidence Bound (UCB) strategy.
    Follow this link to learn more:
    https://people.maths.bris.ac.uk/~maajg/teaching/stochopt/ucb.pdf
    """

    def __init__(self, k: int) -> None:
        """
        Initialize the UCB strategy.

        Args:
            k: The number of arms.
        """
        self.k = k
        self.counts = np.zeros(k)
        self.values = np.zeros(k)
        self.total_counts = 0

    def select_arm(self) -> int:
        """
        Select an arm to pull.

        Returns:
            The index of the arm to pull.

        Example:
            >>> strategy = UCB(k=3)
            >>> 0 <= strategy.select_arm() < 3
            True
        """
        if self.total_counts < self.k:
            return self.total_counts
        ucb_values = self.values + \
            np.sqrt(2 * np.log(self.total_counts) / self.counts)
        return np.argmax(ucb_values)

    def update(self, arm_index: int, reward: int) -> None:
        """
        Update the strategy.

        Args:
            arm_index: The index of the arm to pull.
            reward: The reward for the arm.

        Example:
            >>> strategy = UCB(k=3)
            >>> strategy.update(0, 1)
            >>> strategy.counts[0] == 1
            np.True_
        """
        self.counts[arm_index] += 1
        self.total_counts += 1
        n = self.counts[arm_index]
        self.values[arm_index] += (reward - self.values[arm_index]) / n


# Thompson Sampling


class ThompsonSampling:
    """
    A class for the Thompson Sampling strategy.
    Follow this link to learn more:
    https://en.wikipedia.org/wiki/Thompson_sampling
    """

    def __init__(self, k: int) -> None:
        """
        Initialize the Thompson Sampling strategy.

        Args:
            k: The number of arms.
        """
        self.k = k
        self.successes = np.zeros(k)
        self.failures = np.zeros(k)

    def select_arm(self) -> int:
        """
        Select an arm to pull.

        Returns:
            The index of the arm to pull based on the Thompson Sampling strategy
            which relies on the Beta distribution.

        Example:
            >>> strategy = ThompsonSampling(k=3)
            >>> 0 <= strategy.select_arm() < 3
            np.True_
        """
        rng = np.random.default_rng()

        samples = [
            rng.beta(self.successes[i] + 1, self.failures[i] + 1) for i in range(self.k)
        ]
        return np.argmax(samples)

    def update(self, arm_index: int, reward: int) -> None:
        """
        Update the strategy.

        Args:
            arm_index: The index of the arm to pull.
            reward: The reward for the arm.

        Example:
            >>> strategy = ThompsonSampling(k=3)
            >>> strategy.update(0, 1)
            >>> strategy.successes[0] == 1
            np.True_
        """
        if reward == 1:
            self.successes[arm_index] += 1
        else:
            self.failures[arm_index] += 1


# Random strategy (full exploration)
class RandomStrategy:
    """
    A class for choosing totally random at each round to give
    a better comparison with the other optimised strategies.
    """

    def __init__(self, k: int):
        """
        Initialize the Random strategy.

        Args:
            k: The number of arms.
        """
        self.k = k

    def select_arm(self) -> int:
        """
        Select an arm to pull.

        Returns:
            The index of the arm to pull.

        Example:
            >>> strategy = RandomStrategy(k=3)
            >>> 0 <= strategy.select_arm() < 3
            np.True_
        """
        rng = np.random.default_rng()
        return rng.integers(self.k)

    def update(self, arm_index: int, reward: int) -> None:
        """
        Update the strategy.

        Args:
            arm_index: The index of the arm to pull.
            reward: The reward for the arm.

        Example:
            >>> strategy = RandomStrategy(k=3)
            >>> strategy.update(0, 1)
        """


# Greedy strategy (full exploitation)


class GreedyStrategy:
    """
    A class for the Greedy strategy to show how full exploitation can be
    detrimental to the performance of the strategy.
    """

    def __init__(self, k: int):
        """
        Initialize the Greedy strategy.

        Args:
            k: The number of arms.
        """
        self.k = k
        self.counts = np.zeros(k)
        self.values = np.zeros(k)

    def select_arm(self) -> int:
        """
        Select an arm to pull.

        Returns:
            The index of the arm to pull.

        Example:
            >>> strategy = GreedyStrategy(k=3)
            >>> 0 <= strategy.select_arm() < 3
            np.True_
        """
        return np.argmax(self.values)

    def update(self, arm_index: int, reward: int) -> None:
        """
        Update the strategy.

        Args:
            arm_index: The index of the arm to pull.
            reward: The reward for the arm.

        Example:
            >>> strategy = GreedyStrategy(k=3)
            >>> strategy.update(0, 1)
            >>> strategy.counts[0] == 1
            np.True_
        """
        self.counts[arm_index] += 1
        n = self.counts[arm_index]
        self.values[arm_index] += (reward - self.values[arm_index]) / n


def test_mab_strategies():
    """
    Test the MAB strategies.
    """
    # Simulation
    k = 4
    arms_probabilities = [0.1, 0.3, 0.5, 0.8]  # True probabilities

    bandit = Bandit(arms_probabilities)
    strategies = {
        "Epsilon-Greedy": EpsilonGreedy(epsilon=0.1, k=k),
        "UCB": UCB(k=k),
        "Thompson Sampling": ThompsonSampling(k=k),
        "Full Exploration(Random)": RandomStrategy(k=k),
        "Full Exploitation(Greedy)": GreedyStrategy(k=k),
    }

    num_rounds = 1000
    results = {}

    for name, strategy in strategies.items():
        rewards = []
        total_reward = 0
        for _ in range(num_rounds):
            arm = strategy.select_arm()
            current_reward = bandit.pull(arm)
            strategy.update(arm, current_reward)
            total_reward += current_reward
            rewards.append(total_reward)
        results[name] = rewards

    # Plotting results
    plt.figure(figsize=(12, 6))
    for name, rewards in results.items():
        plt.plot(rewards, label=name)

    plt.title("Cumulative Reward of Multi-Armed Bandit Strategies")
    plt.xlabel("Round")
    plt.ylabel("Cumulative Reward")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    test_mab_strategies()
