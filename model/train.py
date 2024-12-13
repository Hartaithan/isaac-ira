from keras.applications import MobileNetV2
from keras.layers import Dense, GlobalAveragePooling2D
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from tensorflowjs.converters import save_keras_model
from globals import dataset, assets_classes

img_size = (224, 224)
batch_size = 32
num_classes = 1003
num_epochs = 20

train_dir = f'{dataset}/train'
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical'
)

validation_dir = f'{dataset}/validation'
validation_datagen = ImageDataGenerator(rescale=1./255)
validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=img_size,
    batch_size=batch_size,
    class_mode='categorical'
)

base_model = MobileNetV2(
    weights='imagenet', include_top=False, input_shape=(224, 224, 3))

for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dense(1024, activation='relu')(x)
predictions = Dense(num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])

class_labels = {v: k for k, v in train_generator.class_indices.items()}
content = "export const classes: Record<number, string> = {\n"
content += ",\n".join([f"  {key}: \"{value}\"" for key,
                      value in class_labels.items()])
content += "\n};\n"
with open(assets_classes, 'w', encoding='utf-8') as ts_file:
    ts_file.write(content)

history = model.fit(
    train_generator,
    steps_per_epoch=len(train_generator),
    epochs=num_epochs,
    validation_data=validation_generator,
    validation_steps=len(validation_generator)
)

model.save('model.h5')
save_keras_model(model, "export")
