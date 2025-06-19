import random


class CombinationGenerator:
    """Class to generate all unique combinations of a given size from a population.
    Args:
        population (list): The population from which to generate combinations.
        size (int): The size of each combination.
    """

    def __init__(self, population, size):
        self.population = population
        self.size = size
        self.combinations = []
        self.combin_members = [0] * size

    def generate(self, next_member=0, next_item=0):
        """Generate all unique combinations of the specified size."""
        for i in range(next_item, len(self.population)):
            self.combin_members[next_member] = i
            if next_member < self.size - 1:
                self.generate(next_member + 1, i + 1)
            else:
                comb = "-".join(str(self.population[j]) for j in self.combin_members)
                self.combinations.append(comb)


def generate_all_combinations(population, size):
    """Generate all unique combinations of a given size from a population.
    Args:
        population (list): The population from which to generate combinations.
        size (int): The size of each combination.
    """
    generator = CombinationGenerator(population, size)
    generator.generate()
    return generator.combinations


def generate_random_combination(population, K):
    return random.sample(population, K)


def generate_multiple_random_combinations(population, K, size):
    """Generate multiple unique combinations of a given size from a population.
    Args:
        population (list): The population from which to generate combinations.
        K (int): The number of unique combinations to generate.
        size (int): The size of each combination.
    """
    comb_set = set()
    while len(comb_set) < size:
        comb = tuple(sorted(generate_random_combination(population, K)))
        comb_set.add(comb)
    return list(comb_set)


def generate_population(size):
    """Generate a population of integers from 0 to size-1.
    Args:
        size (int): The size of the population.
    """
    return list(range(size))


def insert_combination_to_db(combination):
    # Simulate DB logic (e.g., later use pyodbc or SQLAlchemy)
    print(f"Inserting combination into DB: {combination}")
    return True


def handle_request(data):
    """Handle the request data and call the appropriate function."""

    func_name = data.get("functionName")
    sample = data.get("sample")
    size = data.get("combinationSize")
    amount = data.get("amount", 1)

    if not all([func_name, sample, size]):
        return {"error": "Missing required parameters"}, 400

    if func_name == "generateAllPossibleCombinations":
        result = generate_all_combinations(sample, size)
        return {"combinations": result}, 200

    elif func_name == "generateRandomCombination":
        result = generate_random_combination(sample, size)
        return {"combination": result}, 200

    elif func_name == "generateMultipleRandomCombinations":
        result = generate_multiple_random_combinations(sample, size, amount)
        return {"combinations": result}, 200

    elif func_name == "generatePopulation":
        result = generate_population(size)
        return {"population": result}, 200

    elif func_name == "insertCombination":
        combo = data.get("newCombin")
        if not combo:
            return {"error": "Missing newCombin"}, 400

        success = insert_combination_to_db(combo)
        return {"inserted": success}, 200

    else:
        return {"error": "Unknown functionName"}, 400
