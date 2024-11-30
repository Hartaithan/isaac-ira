import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing import image  # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # type: ignore

model = keras.models.load_model('model/v1.h5')

train_dir = 'dataset/train'
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    train_dir, target_size=(224, 224), batch_size=32, class_mode='categorical')
class_labels = {v: k for k, v in train_generator.class_indices.items()}

img_dir = 'pre-dataset/itemid-128/original.png'
img = image.load_img(img_dir, target_size=(224, 224))
img_array = image.img_to_array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

predictions = model.predict(img_array)
top_indices = np.argsort(-predictions[0])[:5]
top_classes = [class_labels.get(idx, "Unknown") for idx in top_indices]
top_probabilities = [predictions[0][idx] for idx in top_indices]

for i, (class_name, probability) in enumerate(zip(top_classes, top_probabilities), start=1):
    print(f"{i}. {class_name} - {probability:.2f}")
