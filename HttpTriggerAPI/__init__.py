import azure.functions as func
import logging
import json
from utils.responseHandler import handle_request


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Python HTTP trigger function processed a request.")

    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON format."}),
            status_code=400,
            mimetype="application/json",
        )

    response = handle_request(req_body)

    if isinstance(response, tuple):
        return func.HttpResponse(
            json.dumps(response[0]),
            status_code=response[1],
            mimetype="application/json",
        )

    return func.HttpResponse(
        json.dumps(response), status_code=200, mimetype="application/json"
    )
