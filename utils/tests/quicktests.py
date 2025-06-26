def level_key(combination, population_size=28):
    """Calculate the level key for a given combination of numbers.
    The level key is a string that represents the count of numbers in each level based on the
    population size.
    Args:
        combination (list): A list of numbers representing the combination.
        population_size (int): The maximum number of population used to build combinations.
    Returns:
        tuple: A tuple containing the key name and the level key as a string.
    """

    levels = [0] * ((population_size // 10) + 1)
    for n in combination:
        if 1 <= n <= population_size:
            levels[(n - 1) // 10] += 1

    return "level_key", "-".join(map(str, levels))


def level_members(combination, population_size=28):
    """Calculate the level members for a given combination of numbers.
    The level members are grouped by their levels based on the population size.
    Args:
        combination (list): A list of numbers representing the combination.
        population_size (int): The maximum  number of population used to build combinations.
    Returns:
        tuple: A tuple containing the key name and a list of dictionaries with level members.
    """

    levels = {f"LkM{str(i+1).zfill(2)}": [] for i in range((population_size // 10) + 1)}
    for n in combination:
        if 1 <= n <= population_size:
            levels[f"LkM{(n - 1) // 10 + 1:02}"].append(str(n))

    result = [{k: "-".join(v)} for k, v in levels.items() if v]
    return "level_members", result


if __name__ == "__main__":
    # Example usage
    combination = [1, 8, 11, 14, 22, 54]
    print(level_key(combination))  # Output: ('level_key', '2-2-1')
    print(
        level_members(combination)
    )  # Output: ('level_members', [{'LkM01': '1-8'}, {'LkM02': '11-14'}, {'LkM06': '22'}, {'LkM06': '54'}])

    # Test with a different population size
    print(
        level_key(combination, population_size=56)
    )  # Output: ('level_key', '2-2-1-0-0-1')
    print(
        level_members(combination, population_size=56)
    )  # Output: ('level_members', [{'LkM01': '1-8'}, {'LkM02': '11-14'}, {'LkM03': '22'}, {'LkM06': '54'}])

    # Test with 39
    print(
        level_key(combination, population_size=39)
    )  # Output: ('level_key', '2-2-1-0')
    print(
        level_members(combination, population_size=39)
    )  # Output: ('level_members', [{'LkM01': '1-8'}, {'LkM02': '11-14'}, {'LkM03': '22'}, {'LkM06': '54'}])
