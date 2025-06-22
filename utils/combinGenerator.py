from itertools import combinations
import random


def generate_all_combinations(population, size):
    """Generate all unique combinations of a given size from a population.
    Args:
        population (list): The population from which to generate combinations.
        size (int): The size of each combination.
    """
    return list(combinations(population, size))


def generate_random_combinations(population, size, amount=1):
    """Generate multiple random combinations (with possible duplicates) of a given size from a population.
    Args:
        population (list): The population from which to generate combinations.
        size (int): The size of each combination.
        amount (int): The number of combinations to generate.
    Returns:
        list: A list of tuples, each representing a random combination.
    """
    return [tuple(sorted(random.sample(population, size))) for _ in range(amount)]


def generate_random_unique_combinations(population, size, amount=1):
    """Generate multiple unique random combinations of a given size from a population.
    Args:
        population (list): The population from which to generate combinations.
        size (int): The size of each combination.
        amount (int): The number of unique combinations to generate.
    """
    comb_set = set()
    while len(comb_set) < amount:
        comb = tuple(sorted(random.sample(population, size)))
        comb_set.add(comb)
    return list(comb_set)
