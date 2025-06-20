import requests

BASE_URL = 'http://dmg.local'
LOGIN_ENDPOINT = '/api/v1/login'
DATASET_ENDPOINT = '/api/v1/dataset'
TRAINING_ENDPOINT = '/api/v1/training'

def login(username: str, password: str):
    url = f"{BASE_URL}{LOGIN_ENDPOINT}"
    response = requests.post(url, json={"username": username, "password": password})
    response.raise_for_status()
    data = response.json()
    return data['token'], data['refresh_token']

def create_dataset(token: str, dataset_name: str, tool_name: str, train_box=True, train_mask=False):
    url = f"{BASE_URL}{DATASET_ENDPOINT}"
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

def trigger_training(token: str, dataset_id: int):
    url = f"{BASE_URL}{TRAINING_ENDPOINT}"
    headers = {"x-refresh-token": f"Bearer {token}"}
    payload = {"dataset_id": dataset_id}
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    user = "testuser"
    pwd = "solomontest"
    token, refresh_token = login(user, pwd)
    print("token:", token)
    dataset = create_dataset(token, "DatasetTest0616", "ObjectDetectionV1")
    print("dataset:", dataset)
    train_resp = trigger_training(token, dataset['id'])
    print("training:", train_resp)
