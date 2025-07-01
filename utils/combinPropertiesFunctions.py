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


def sequence_key(combination):
    """Calculate the sequence key for a given combination of numbers.
    The sequence key is a string that represents the count of consecutive sequences in the combination.
    Args:
        combination (list): A list of numbers representing the combination.
    Returns:
        tuple: A tuple containing the key name and the sequence key as a string.
    """
    sorted_combination = sorted(combination)
    groups = []
    count = 1

    for i in range(1, len(sorted_combination)):
        if sorted_combination[i] == sorted_combination[i - 1] + 1:
            count += 1
        else:
            groups.append(count)
            count = 1
    groups.append(count)
    return "sequence_key", "-".join(map(str, groups))


def prime_count(combination):
    """Calculate the count of prime numbers in a given combination of numbers.
    Args:
        combination (list): A list of numbers representing the combination.
    Returns:
        tuple: A tuple containing the key name and the count of prime numbers as a string.
    """

    def is_prime(n):
        return n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))

    prime_count = sum(1 for n in combination if is_prime(n))
    return "prime_count", str(prime_count)


def generate_boxes(combination, cIndex):
    box_configs = [
        {"size": 10, "id": 100},
        {"size": 100, "id": 10},
        {"size": 1000, "id": 1},
    ]

    boxes = []
    for config in box_configs:
        size = config["size"]
        box_number = (cIndex - 1) // size + 1
        position_in_box = (cIndex - 1) % size + 1

        boxes.append(
            {
                "id": box_number,
                "index": position_in_box,
                "size": size,
            }
        )
    return "boxes", boxes
