# SOLOMON Training API Usage

This repository contains a small example script demonstrating how to interact with the SOLOMON training server REST API.

## Requirements
- Python 3
- [`requests`](https://pypi.org/project/requests/) (`pip install requests`)

## Running `example_api.py`
1. Install the requirements: `pip install requests`.
2. Open `example_api.py` and set the following variables if needed:
   - `BASE_URL` – URL of your training server. Default is `http://dmg.local`.
   - `user` and `pwd` – credentials used for login at the bottom of the script.
3. Execute the script:
   ```bash
   python3 example_api.py
   ```
   It will log in, create a dataset and trigger a training job using the API.

## Key Endpoints
Based on `openapi.json` the API exposes these relevant endpoints:

- **`POST /api/v1/login`** – obtain an access token and refresh token.
- **`POST /api/v1/dataset`** – create a dataset. Body fields include `dataset_name`, `tool_name`, `train_box`, and `train_mask`.
- **`POST /api/v1/training`** – start training for a dataset by providing `dataset_id`.

Consult `openapi.json` for the full specification of optional headers and response formats.

