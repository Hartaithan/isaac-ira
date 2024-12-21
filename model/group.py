import os
import shutil
import random
from globals import dataset, pre_dataset
from progress import Progress

input_dir = pre_dataset
output_dir = dataset


def group_dataset():
    dirs = [
        os.path.join(output_dir, 'train'),
        os.path.join(output_dir, 'validation'),
        os.path.join(output_dir, 'test'),
    ]

    os.makedirs(dirs[0], exist_ok=True)
    os.makedirs(dirs[1], exist_ok=True)
    os.makedirs(dirs[2], exist_ok=True)

    progress = Progress("Group dataset")
    progress.start()

    folders = os.listdir(input_dir)
    for i, subdir in enumerate(folders):
        if subdir == '.DS_Store':
            continue
        subdir_path = os.path.join(input_dir, subdir)
        if os.path.isdir(subdir_path):
            progress.update(subdir_path, i, len(folders))

            image_files = [f for f in os.listdir(
                subdir_path) if f.endswith('.jpg') or f.endswith('.png')]

            random.shuffle(image_files)

            num_files = len(image_files)
            train_size = int(num_files * 0.7)
            validation_size = int(num_files * 0.15)

            train_files = image_files[:train_size]
            validation_files = image_files[train_size:train_size+validation_size]
            test_files = image_files[train_size+validation_size:]

            train_subdir = os.path.join(dirs[0], subdir)
            os.makedirs(train_subdir, exist_ok=True)
            validation_subdir = os.path.join(dirs[1], subdir)
            os.makedirs(validation_subdir, exist_ok=True)
            test_subdir = os.path.join(dirs[2], subdir)
            os.makedirs(test_subdir, exist_ok=True)

            for file in train_files:
                shutil.copy(os.path.join(subdir_path, file), train_subdir)
            for file in validation_files:
                shutil.copy(os.path.join(subdir_path, file), validation_subdir)
            for file in test_files:
                shutil.copy(os.path.join(subdir_path, file), test_subdir)

    progress.complete()
