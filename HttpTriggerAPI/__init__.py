import logging
import azure.functions as func
import json
from utils.logic import generate_combination, insert_combination_to_db


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing request...")

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    func_name = data.get("functionName")

    if func_name == "generateCombination":
        sample = data.get("sample")
        size = data.get("combinationSize")
        if not sample or not size:
            return func.HttpResponse(
                "Missing sample or combinationSize", status_code=400
            )

        result = generate_combination(sample, size)
        return func.HttpResponse(
            json.dumps({"combination": result}), mimetype="application/json"
        )

    elif func_name == "insertCombination":
        combo = data.get("newCombin")
        if not combo:
            return func.HttpResponse("Missing newCombin", status_code=400)

        success = insert_combination_to_db(combo)
        return func.HttpResponse(
            json.dumps({"inserted": success}), mimetype="application/json"
        )

    else:
        return func.HttpResponse("Unknown functionName", status_code=400)
