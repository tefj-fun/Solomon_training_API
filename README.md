# Solomon_training_API

This repository contains a simple example showing how to call the Solomon training server API.

Update `config.py` with the server address and any endpoint overrides before running `example_api.py`.

## Dataset Location

The training server expects each dataset to follow this directory structure:

```
sol_project/
├── images/
│   ├── image1.jpg
│   └── ...
├── train.json
├── val.json  # required even if empty
└── voc_config.json
```

Place this folder anywhere on your local machine. When uploading you will
compress the entire `sol_project` directory and send it to the dataset upload
endpoint. The `val.json` file **must** exist even if it is empty.

The annotation files (`train.json` and `val.json`) use a COCO-like format. The
`categories` section must match between both files. An example of a single
category entry is:

```json
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
```

The `voc_config.json` file defines training parameters. Below is a shortened
example showing a few important fields:

```json
{
  "min_dimension": "800",
  "max_dimension": "1333",
  "image_height": "640",
  "image_width": "640",
  "max_iter": "2000",
  "max_detections": "100",
  "test_score_thresh": "0.5",
  "class_names": "box",
  "class_colors": "#FCFF8A"
}
```

## Training Status and Model Download

`example_api.py` demonstrates how to:

1. Authenticate and create a dataset entry
2. Trigger training
3. Poll the `/api/v1/training/{id}` endpoint until the `status` field becomes
   `FINISHED`
4. Download the resulting model from
   `/api/v1/dataset/{id}/model/{model_name}`

Multiple users can trigger training simultaneously. Each request must include a
valid token in the `x-refresh-token` header so the server can associate the
operation with the correct user.
