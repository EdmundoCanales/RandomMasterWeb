from utils.combinPropertiesFunctions import (
    level_key,
    level_members,
    sequence_key,
    prime_count,
)


def handle_request(data):
    """Receives http reques body to fill up parameters needed
    evaluates the function to call and returns the result.
    """
    func_name = data.get("functionName")
    sample = data.get("sample")
    size = data.get("combinationSize")
    amount = data.get("amount", 1)
    prop_functions = [level_key, level_members, sequence_key, prime_count]

    if not all([func_name, sample, size]):
        return {"error": "Missing required parameters."}, 400

    # Map function names to acctual generator functions
    function_map = {
        "generateAllPossibleCombinations": "generate_all_combinations",
        "generateRandomCombinations": "generate_random_combinations",
        "generateRandomUniqueCombinations": "generate_random_unique_combinations",
    }

    generator_func_name = function_map.get(func_name)
    if not generator_func_name:
        return {"error": "Invalid function name."}, 400

    from utils import combinGenerator

    generator_func = getattr(combinGenerator, generator_func_name)

    # Call the generator function with appropriate arguments
    try:
        if generator_func_name == "generate_all_combinations":
            combinations = generator_func(sample, size)
        else:
            combinations = generator_func(sample, size, amount)
    except Exception as e:
        return {"error generating combinations model": str(e)}, 500

    # Import CombinationModel class
    from utils.combinationModel import CombinationModel

    models = []

    try:
        for index, combination in enumerate(combinations, start=1):
            model = CombinationModel(combination, index)
            model.calculate_properties(prop_functions)
            models.append(model.to_dict())

    except Exception as e:
        return {"error generating combinations model": str(e)}, 500

    return {"combinations": models}, 200
