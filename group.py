

import os
import shutil
import random
from globals import dataset, pre_dataset, pre_dataset

input = pre_dataset
output = dataset


def group_dataset():
    train_dir = os.path.join(output, 'train')
    validation_dir = os.path.join(output, 'validation')
    test_dir = os.path.join(output, 'test')
    os.makedirs(train_dir, exist_ok=True)
    os.makedirs(validation_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    for subdir in os.listdir(input):
        subdir_path = os.path.join(input, subdir)
        if os.path.isdir(subdir_path):
            image_files = [f for f in os.listdir(
                subdir_path) if f.endswith('.jpg') or f.endswith('.png')]

            random.shuffle(image_files)

            train_files = image_files[:10]
            validation_files = image_files[10:20]
            test_files = image_files[20:]

            train_subdir = os.path.join(train_dir, subdir)
            validation_subdir = os.path.join(validation_dir, subdir)
            test_subdir = os.path.join(test_dir, subdir)
            os.makedirs(train_subdir, exist_ok=True)
            os.makedirs(validation_subdir, exist_ok=True)
            os.makedirs(test_subdir, exist_ok=True)

            for file in train_files:
                shutil.copy(os.path.join(subdir_path, file), train_subdir)
            for file in validation_files:
                shutil.copy(os.path.join(subdir_path, file), validation_subdir)
            for file in test_files:
                shutil.copy(os.path.join(subdir_path, file), test_subdir)
