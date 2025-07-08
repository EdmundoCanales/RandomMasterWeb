from collections import defaultdict, Counter
from typing import Any, Optional
import statistics


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


def calc_deltas(indexes):
    return [j - i for i, j in zip(indexes[:-1], indexes[1:])]


def apply_filter(combination, filter_string):
    if filter_string == "all":
        return True
    for clause in filter_string.split("&"):
        if "=" not in clause:
            raise ValueError(
                f"Invalid filter clause: {clause}. Expected format 'key=value'."
            )
        k, v = clause.split("=")
        if str(combination.get(k)) != v:
            return False
    return True


def top3_frequent_deltas(deltas):
    """Returns the top 3 most frequent deltas."""
    if not deltas:
        return []
    freq = Counter(deltas)
    # sort by frequency descending, then by value ascending
    most_common = sorted(freq.items(), key=lambda x: (-x[1], x[0]))
    return [val for val, _ in most_common[:3]]


def refresh_analytics(combinations, key_members, filters_list):

    # initialize results
    resuts: list[dict[str, Any]] = []

    for filter_index, filter_str in enumerate(filters_list):

        # appy filter
        filtered_combs = [c for c in combinations if apply_filter(c, filter_str)]

        # assing dynamic inndex to filtered combinations
        for i, c in enumerate(filtered_combs):
            c["_dyn_index"] = i + 1

        # find matching combos for each key member
        for key_member in key_members:
            member = int(
                key_member
            )  # note: make this flexible to accept both int and str
            matching_combos = [
                c for c in filtered_combs if member in c.get("numbers", [])
            ]  # note: use get to avoid KeyError
            dyn_index = [c["_dyn_index"] for c in matching_combos]
            deltas = calc_deltas(dyn_index)

            # find or create result entry for this key member
            key_result: Optional[dict[str, Any]] = next(
                (r for r in resuts if r["key"] == str(key_member)), None
            )
            if not key_result:
                key_result: Optional[dict[str, Any]] = {"key": str(key_member)}
                resuts.append(key_result)

            metric_key = (
                "general" if filter_str == "all" else f"filter_{filter_index:02d}"
            )

            key_result[metric_key] = {
                "filter": filter_str,
                "speed(avg)": round(statistics.mean(deltas), 2) if deltas else 0,
                "speed(min)": min(deltas) if deltas else 0,
                "speed(max)": max(deltas) if deltas else 0,
                "speed(stddev)": (
                    round(statistics.stdev(deltas), 2) if len(deltas) > 1 else 0
                ),
                "speed(top3)": top3_frequent_deltas(deltas),
            }
    return resuts
