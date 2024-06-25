import os
import json
import tensorflow as tf
assert tf.__version__.startswith('2')

from mediapipe_model_maker import object_detector

# Download and unzip the dataset
dataset_url = "https://storage.googleapis.com/mediapipe-tasks/object_detector/android_figurine.zip"
dataset_dir = "/home/tolasing/main_ws/ml_ws/robber.v9i.voc"
"""
if not os.path.exists(dataset_dir):
    os.makedirs(dataset_dir)
    tf.keras.utils.get_file(dataset_dir, dataset_url, extract=True)
"""

train_dataset_path = os.path.join(dataset_dir, "train")
validation_dataset_path = os.path.join(dataset_dir, "valid")

train_data = object_detector.Dataset.from_pascal_voc_folder('/home/tolasing/main_ws/ml_ws/robber.v7i.voc/train', cache_dir="/tmp/od_data/train")

validation_data = object_detector.Dataset.from_pascal_voc_folder('/home/tolasing/main_ws/ml_ws/robber.v7i.voc/validation',cache_dir="/tmp/od_data/validation")
print("train_data size: ", train_data.size)
print("validation_data size: ", validation_data.size)

spec = object_detector.SupportedModels.MOBILENET_MULTI_AVG_I384
hparams = object_detector.HParams(export_dir='exported_model')
options = object_detector.ObjectDetectorOptions(
    supported_model=spec,
    hparams=hparams
)

model = object_detector.ObjectDetector.create(
    train_data=train_data,
    validation_data=validation_data,
    options=options)

loss, coco_metrics = model.evaluate(validation_data, batch_size=4)
print(f"Validation loss: {loss}")
print(f"Validation coco metrics: {coco_metrics}")

model.export_model()
print("Exported model saved to:", hparams.export_dir)
