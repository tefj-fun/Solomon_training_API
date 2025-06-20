import requests
import time
import config

def login(username: str, password: str):
    url = f"{config.BASE_URL}{config.LOGIN_ENDPOINT}"
    response = requests.post(url, json={"username": username, "password": password})
    response.raise_for_status()
    data = response.json()
    return data['token'], data['refresh_token']

def create_dataset(token: str, dataset_name: str, tool_name: str, train_box=True, train_mask=False):
    url = f"{config.BASE_URL}{config.DATASET_ENDPOINT}"
    headers = {"x-refresh-token": f"Bearer {token}"}
    payload = {
        "dataset_name": dataset_name,
        "tool_name": tool_name,
        "train_box": train_box,
        "train_mask": train_mask,
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def upload_dataset_config(token: str, dataset_id: int, config_path: str):
    url = f"{config.BASE_URL}{config.DATASET_CONFIG_UPLOAD_ENDPOINT.format(id=dataset_id)}"
    headers = {"x-refresh-token": f"Bearer {token}"}
    with open(config_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files, headers=headers)
    response.raise_for_status()
    return response.json()

def upload_dataset_image(token: str, dataset_id: int, image_path: str):
    url = f"{config.BASE_URL}{config.DATASET_IMAGE_UPLOAD_ENDPOINT.format(id=dataset_id)}"
    headers = {"x-refresh-token": f"Bearer {token}"}
    with open(image_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, files=files, headers=headers)
    response.raise_for_status()
    return response.json()

def trigger_training(token: str, dataset_id: int):
    url = f"{config.BASE_URL}{config.TRAINING_ENDPOINT}"
    headers = {"x-refresh-token": f"Bearer {token}"}
    payload = {"dataset_id": dataset_id}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

def get_training_info(token: str, training_id: int):
    url = f"{config.BASE_URL}{config.TRAINING_INFO_ENDPOINT.format(id=training_id)}"
    headers = {"x-refresh-token": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def download_model(token: str, dataset_id: int, model_name: str, output_path: str):
    url = f"{config.BASE_URL}{config.MODEL_DOWNLOAD_ENDPOINT.format(id=dataset_id, model_name=model_name)}"
    headers = {"x-refresh-token": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)

def list_models(token: str, dataset_id: int):
    url = f"{config.BASE_URL}{config.MODEL_LIST_ENDPOINT.format(id=dataset_id)}"
    headers = {"x-refresh-token": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json().get("data", [])

if __name__ == "__main__":
    user = "testuser"
    pwd = "solomontest"
    token, refresh_token = login(user, pwd)
    print("token:", token)
    dataset = create_dataset(token, "DatasetTest0616", "ObjectDetectionV1")
    print("dataset:", dataset)
    # Upload configuration and a single image as an example
    upload_dataset_config(token, dataset["id"], "sol_project/voc_config.json")
    upload_dataset_image(token, dataset["id"], "sol_project/images/image1.jpg")
    train_resp = trigger_training(token, dataset["id"])
    training_id = train_resp.get("id") or train_resp.get("training_id")
    print("training started with id", training_id)

    # Poll training status until finished
    while True:
        info = get_training_info(token, training_id)
        status = info["data"]["training_info"]["info"].get("status")
        progress = info["data"]["training_info"]["data"]["metrics"].get("progress")
        print(f"status: {status}, progress: {progress}")
        if status == "FINISHED":
            models = list_models(token, dataset["id"])
            if models:
                model_name = models[-1]["model_name"]
                download_model(token, dataset["id"], model_name, model_name)
                print("model downloaded to", model_name)
            break
        time.sleep(10)
