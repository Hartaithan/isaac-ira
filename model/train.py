from keras.applications import MobileNetV2
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from globals import dataset, assets_classes

base_model = MobileNetV2(
    weights='imagenet', include_top=False, input_shape=(224, 224, 3))

for layer in base_model.layers:
    layer.trainable = False

x = base_model.output
x = Conv2D(128, (3, 3), activation='relu')(x)
x = MaxPooling2D((2, 2))(x)
x = Flatten()(x)
x = Dense(128, activation='relu')(x)
x = Dense(1003, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=x)

model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])

train_dir = f'{dataset}/train'
validation_dir = f'{dataset}/validation'

train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir, target_size=(224, 224), batch_size=32, class_mode='categorical')
validation_generator = validation_datagen.flow_from_directory(
    validation_dir, target_size=(224, 224), batch_size=32, class_mode='categorical')

class_labels = {v: k for k, v in train_generator.class_indices.items()}
content = "export const classes: Record<number, string> = {\n"
content += ",\n".join([f"  {key}: \"{value}\"" for key,
                      value in class_labels.items()])
content += "\n};\n"
with open(assets_classes, 'w', encoding='utf-8') as ts_file:
    ts_file.write(content)


history = model.fit(train_generator, epochs=10,
                    validation_data=validation_generator)

model.save('model.keras')
