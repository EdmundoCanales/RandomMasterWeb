def level_key(combination):
    """Calculate the level key for a given combination of numbers.
        The level key is a string that represents the count of numbers in three ranges:
    Args:
        combination (list): A list of numbers representing the combination.
    Returns:
        tuple: A tuple containing the key name and the level key as a string.
    """

    levels = [0, 0, 0]
    for n in combination:
        if n <= 10:
            levels[0] += 1
        elif 11 <= n <= 20:
            levels[1] += 1
        elif 21 <= n <= 30:
            levels[2] += 1

    return "level_key", "-".join(map(str, levels))


def level_members(combination):

    levels = {"LkM01": [], "LkM02": [], "LkM03": []}
    for n in combination:
        if n <= 10:
            levels["LkM01"].append(str(n))
        elif 11 <= n <= 20:
            levels["LkM02"].append(str(n))
        elif 21 <= n <= 30:
            levels["LkM03"].append(str(n))

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
