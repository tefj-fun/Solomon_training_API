import os
def upload_dataset_images(token: str, dataset_id: int, images_dir: str):
    for img in os.listdir(images_dir):
        if img.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            upload_dataset_image(token, dataset_id, os.path.join(images_dir, img))

    # Upload dataset configuration (train.json, val.json, voc_config.json)
    upload_dataset_config(token, dataset["id"], "dataset_config.zip")
    # Upload all images in the dataset directory
    upload_dataset_images(token, dataset["id"], "sol_project/images")
