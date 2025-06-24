import os
import json
from azure.storage.blob import BlobServiceClient
from utils.combinGenerator import (
    generate_all_combinations,
    generate_random_combinations,
)

# Get the connection string from the environment variable
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME", "default-container")

# Check if the connection string  and container name are set
if not BLOB_CONNECTION_STRING:
    raise ValueError("BLOB_CONNECTION_STRING environment variable is not set.")

if not BLOB_CONTAINER_NAME:
    raise ValueError("BLOB_CONTAINER_NAME environment variable is not set.")

# Initialize the BlobServiceClient
blob_service_client = BlobServiceClient.from_connection_string(BLOB_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)


# function to resolve data from request body.
def resolve_data_from_request(
    data=None, population=None, size=None, amount=None, full_model=False
):
    if data:
        return data
    if population and size and amount:
        if full_model:
            return generate_all_combinations(population, size)
        elif amount:
            return generate_random_combinations(population, size, amount)
    raise ValueError("Insufficient parameters provided to resolve data.")


def upload_model(model_type, model_name, data=None, population=None, size=None):
    resolved_data = resolve_data_from_request(data, population, size, full_model=True)
    path = f"{model_type}/{model_name}.json"
    blob_client = container_client.get_blob_client(path)
    blob_client.upload_blob(json.dumps(resolved_data, indent=2), overwrite=True)
    return {
        "status": "success",
        "message": f"Model {model_name} of type {model_type} uploaded successfully to {path}.",
    }


def overwrite_model(model_type, model_name, data=None, population=None, size=None):
    return upload_model(model_type, model_name, data, population, size)


def append_to_model(model_name, data=None, population=None, size=None, amount=None):
    resolved_data = resolve_data_from_request(data, population, size, amount)
    path = f"actualModels/{model_name}.json"
    blob_client = container_client.get_blob_client(path)

    try:
        existing_data = json.loads(blob_client.download_blob().readall())
    except Exception as e:
        existing_data = []

    if isinstance(resolved_data, list):
        existing_data.extend(resolved_data)
    else:
        existing_data.append(resolved_data)

    # Upload the updated data back to the blob
    blob_client.upload_blob(json.dumps(existing_data, indent=2), overwrite=True)

    return {
        "status": "success",
        "message": f"Data appended to model {model_name} successfully.",
    }
