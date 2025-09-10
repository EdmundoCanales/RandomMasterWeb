import os
import json
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


def getJson(filename, path=None):
    """
    Reads a JSON file from the specified path or from the current file's directory if path is None.
    Args:
        filename (str): The name of the JSON file.
        path (str, optional): The directory path. Defaults to the current file's directory.
    Returns:
        object: The loaded JSON data.
    """
    if path is None:
        path = os.path.dirname(__file__)
    file_path = os.path.join(path, filename)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File {filename} not found in path {path}.")


def calc_deltas(indexes):
    return [j - i for i, j in zip(indexes[:-1], indexes[1:])]


def test_is_prime(n):
    return n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))


def test_apply_filter(combination, filter_string):
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


def test_filter(combinations, key_members):
    member = int(key_members[3])
    filtered_by_members = [c for c in combinations if member in c["numbers"]]
    filtered_by_members.sort(key=lambda x: x["index"])

    return filtered_by_members


def test_refresh_analytics(combinations, key_members, filters_list):

    # initialize results
    resuts: list[dict[str, Any]] = []

    for filter_index, filter_str in enumerate(filters_list):

        # appy filter
        filtered_combs = [c for c in combinations if test_apply_filter(c, filter_str)]

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


def test_print(combinations):
    for c in combinations:
        print(
            f"{c['index']} | {c['numbers']} | "
            f"{c['level_key']} | {c['sequence_key']} | "
            f"{c['prime_count']} | \n "
            # f"{c['level_members']} |  \n"
            # f"{c['boxes']}"
        )


if __name__ == "__main__":
    # Example usage
    # combination = [1, 8, 11, 14, 22, 54]
    jsonData = getJson("combinationsSample.json", path="utils/tests")

    # print(level_key(combination))  # Output: ('level_key', '2-2-1')
    # print(
    #    level_members(combination)
    # )  # Output: ('level_members', [{'LkM01': '1-8'}, {'LkM02': '11-14'}, {'LkM06': '22'}, {'LkM06': '54'}])

    # Test with a different population size
    # print(
    #    level_key(combination, population_size=56)
    # )  # Output: ('level_key', '2-2-1-0-0-1')
    # print(
    #    level_members(combination, population_size=56)
    # )  # Output: ('level_members', [{'LkM01': '1-8'}, {'LkM02': '11-14'}, {'LkM03': '22'}, {'LkM06': '54'}])

    # Test with 39
    # print(
    #    level_key(combination, population_size=39)
    # )  # Output: ('level_key', '2-2-1-0')
    # print(
    #    level_members(combination, population_size=39)
    # )  # Output: ('level_members', [{'LkM01': '1-8'}, {'LkM02': '11-14'}, {'LkM03': '22'}, {'LkM06': '54'}])

    # print("\n ------ \n")
    # test_print(jsonData["combinations"])  # Load the JSON file

    print("\n ------ \n")
    # Example of filtering combinations based on a key member
    filtered_combin = test_filter(jsonData["combinations"], ["1", "2", "3", "4"])
    test_print(filtered_combin)  # Print the filtered combinations

    print("\n ------ \n")
    # Example of refreshing analytics with filters
    member_list = [str(m) for m in range(1, 29)]
    print(
        test_refresh_analytics(
            jsonData["combinations"],
            member_list,
            ["all", "level_key=2-2-1", "level_key=2-1-2&sequence_key=1-1-1-1-1"],
        )
    )
    # Example of prime test
    print(f"Is number '1' prime? {test_is_prime(1)}")  # True
    print(f"Is number '3' prime? {test_is_prime(3)}")  # True
    print(f"Is number '13' prime? {test_is_prime(13)}")  # False
    print(f"Is number '18' prime? {test_is_prime(18)}")  # False
    print(f"Is number '26' prime? {test_is_prime(26)}")  # False
