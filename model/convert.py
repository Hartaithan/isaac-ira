from keras.models import load_model
from tensorflowjs.converters import save_keras_model
from globals import root

model = load_model(f'{root}/model/v2.keras')
save_keras_model(model, './export')
