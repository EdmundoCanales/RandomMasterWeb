from utils import combinGenerator
from utils import blobHandler


def handle_request(data):
    """Receives http reques body to fill up parameters needed
    evaluates the function to call and returns the result.
    """
    func_name = data.get("functionName")
    sample = data.get("sample")
    size = data.get("combinationSize", data.get("size"))
    amount = data.get("amount", 1)
    model_name = data.get("model")
    model_type = data.get("modelType")
    provided_data = data.get("data")

    if func_name in [
        "generateAllPossibleCombinations",
        "generateRandomCombinations",
        "generateRandomUniqueCombinations",
    ]:

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

        generator_func = getattr(combinGenerator, generator_func_name)

        # Call the generator function with appropriate arguments
        try:
            if generator_func_name == "generate_all_combinations":
                combinations = generator_func(sample, size)
            else:
                combinations = generator_func(sample, size, amount)
        except Exception as e:
            return {"error generating combinations model": str(e)}, 500

        return {"combinations": combinations}, 200  # models

    elif func_name == "UploadModel":
        try:
            result = blobHandler.upload_model(
                model_type=model_type,
                model_name=model_name,
                population=sample,
                size=size,
                amount=amount,
                data=provided_data,
            )
            return {"message": "Model uploaded successfully", "result": result}, 200
        except Exception as e:
            return {"error uploading model": str(e)}, 500

    elif func_name == "OverwriteModel":
        try:
            result = blobHandler.overwrite_model(
                model_type=model_type,
                model_name=model_name,
                population=sample,
                size=size,
                amount=amount,
                data=provided_data,
            )
            return {"message": "Model overwritten successfully", "result": result}, 200
        except Exception as e:
            return {"error overwriting model": str(e)}, 500

    elif func_name == "AddCombin":
        try:
            result = blobHandler.append_to_model(
                model_name=model_name,
                population=sample,
                size=size,
                amount=amount,
                data=provided_data,
            )
            return {
                "message": "Combination(s) added successfully",
                "result": result,
            }, 200
        except Exception as e:
            return {"error adding combination": str(e)}, 500

    else:
        return {"error": "Invalid function name."}, 400
