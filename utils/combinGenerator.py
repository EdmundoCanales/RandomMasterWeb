from utils.combinPropertiesFunctions import (
    level_key,
    level_members,
    sequence_key,
    prime_count,
)
from itertools import combinations
from utils.combinationModel import CombinationModel
import random


def generate_all_combinations(population, size):
    """Generate all unique combinations of a given size from a population.
    Args:
        population (list): The population from which to generate combinations.
        size (int): The size of each combination.
    """
    try:
        result = build_combination_models(list(combinations(population, size)))
    except Exception as e:
        raise RuntimeError(f"Error generating all combinations: {e}")
    finally:
        return result


def generate_random_combinations(population, size, amount=1, start_index=1):
    """Generate multiple random combinations (with possible duplicates) of a given size from a population.
    Args:
        population (list): The population from which to generate combinations.
        size (int): The size of each combination.
        amount (int): The number of combinations to generate.
    Returns:
        list: A list of tuples, each representing a random combination.
    """
    try:
        result = build_combination_models(
            [tuple(sorted(random.sample(population, size))) for _ in range(amount)],
            start_index=start_index,
        )
    except Exception as e:
        raise RuntimeError(f"Error generating random combinations: {e}")
    finally:
        return result


def generate_random_unique_combinations(population, size, amount=1, start_index=1):
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
    try:
        comb_set = build_combination_models(comb_set, start_index=start_index)
    except Exception as e:
        raise RuntimeError(f"Error serializing unique random combinations: {e}")
    finally:
        return list(comb_set)


def build_combination_models(combinations, start_index=1):
    """
    Converts raw combinations into CombinationModel instances with calculated properties.

    Args:
    combinations (Iterable[tuple]): The list or set of raw combinations.

    Returns:
    list[dict]: List of dictionaries representing enriched CombinationModels.
    """
    prop_functions = [level_key, level_members, sequence_key, prime_count]
    models = []
    try:
        for index, combination in enumerate(combinations, start=start_index):
            model = CombinationModel(combination, index)
            model.calculate_properties(prop_functions)
            models.append(model.to_dict())
    except Exception as e:
        # Handle serialization errors
        raise RuntimeError(f"Error serializing combination models: {e}")
    return models
