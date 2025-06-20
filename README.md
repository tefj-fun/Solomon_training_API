# Solomon Training API

This repository contains example code and documentation for interacting with a Solomon training server.

## Repository Contents

| File | Description |
| ---- | ----------- |
| `openapi.json` | OpenAPI specification describing all REST endpoints. |
| `training-server-api-20250619.html` | HTML version of the API docs generated from `openapi.json`. |
| `config.py` | Python module with the base URL and endpoint constants. |
| `example_api.ipynb` | Jupyter notebook demonstrating how to call the API using `requests`. |
| `example_api.py` | (empty placeholder) |
| `Dataset Structure and Config File.pdf` | PDF outlining dataset organization and configuration parameters. |

## Required Files for Training

To run the training API you need a dataset folder structured as follows:

```
sol_project/
├── images/
│   ├── <image1>
│   ├── <image2>
│   └── ...
├── train.json
└── val.json
└── voc_config.json
```

The PDF emphasises that `val.json` **must exist** even if it contains no annotations, and its `categories` field must match `train.json`.

### Annotation Format

An example minimal `val.json` structure looks like:

```
{
  "info": {"keypoints": []},
  "categories": [
    {
      "box": true,
      "mask": true,
      "angle": false,
      "keypoint": false,
      "id": 1,
      "name": "person",
      "supercategory": "person",
      "color": [252, 255, 138],
      "keypoints": [],
      "keypoint_colors": []
    }
  ],
  "images": [],
  "annotations": []
}
```

Configuration parameters reside in `voc_config.json`. Important fields include image dimensions, iteration counts, and thresholds:

```
{
  "min_dimension": "800",
  "max_dimension": "1333",
  "image_height": "640",
  "image_width": "640",
  "eval_iou": "0.5",
  "max_iter": "2000",
  "max_detections": "100",
  "test_score_thresh": "0.5",
  "class_names": "box",
  ...
}
```
These values come directly from the PDF specification.

## Using the Training API

The `example_api.ipynb` notebook demonstrates how to:
1. Obtain a token from `/api/v1/login`.
2. Create a dataset via `/api/v1/dataset`.
3. Trigger training with `/api/v1/training`.

A minimal Python snippet looks like:

```python
import requests
BASE_URL = 'http://dmg.local'
LOGIN_ENDPOINT = '/api/v1/login'
DATASET_ENDPOINT = '/api/v1/dataset'
TRAINING_ENDPOINT = '/api/v1/training'

# token, refresh_token = login(user, password)
# dataset = create_dataset(token, 'DatasetName', 'ObjectDetectionV1')
# training = trigger_training(token, dataset['id'])
```

API endpoints for uploading configuration and images are also defined in `openapi.json`:
- `/api/v1/dataset/{id}/config` – Upload dataset config.
- `/api/v1/dataset/{id}/image` – Upload images to a dataset.
- `/api/v1/dataset/{id}/model` – List trained models.

The base URL and endpoints are provided in `config.py`.

## Dataset Upload and Training Workflow

1. **Login** to obtain an access token.
2. **Create Dataset** (`POST /api/v1/dataset`) specifying name, tool and training options.
3. **Upload Files**:
   - POST dataset configuration (`voc_config.json`) to `/api/v1/dataset/{id}/config`.
   - POST images to `/api/v1/dataset/{id}/image`.
4. **Trigger Training** by calling `/api/v1/training` with the dataset ID.
5. **Query Models** using `/api/v1/dataset/{id}/model` or download a model via `/api/v1/dataset/{id}/model/{model_name}`.

Consult the HTML or JSON API documentation for detailed request/response bodies.

