

import os
import shutil
import random
from globals import dataset, pre_dataset, pre_dataset

input = pre_dataset
output = dataset


def group_dataset():
    os.makedirs(output, exist_ok=True)

    for subdir in os.listdir(input):
        subdir_path = os.path.join(input, subdir)
        if os.path.isdir(subdir_path):
            output_subdir_path = os.path.join(output, subdir)
            os.makedirs(output_subdir_path, exist_ok=True)

            image_files = [f for f in os.listdir(
                subdir_path) if f.endswith('.png')]

            random.shuffle(image_files)

            train_files = image_files[:10]
            validation_files = image_files[10:20]
            test_files = image_files[20:]

            train_dir = os.path.join(output_subdir_path, 'train')
            os.makedirs(train_dir, exist_ok=True)
            validation_dir = os.path.join(output_subdir_path, 'validation')
            os.makedirs(validation_dir, exist_ok=True)
            test_dir = os.path.join(output_subdir_path, 'test')
            os.makedirs(test_dir, exist_ok=True)

            for file in train_files:
                shutil.copy(os.path.join(subdir_path, file), train_dir)
            for file in validation_files:
                shutil.copy(os.path.join(subdir_path, file), validation_dir)
            for file in test_files:
                shutil.copy(os.path.join(subdir_path, file), test_dir)
