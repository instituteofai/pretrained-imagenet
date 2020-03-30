print('loading model...')

import efficientnet.keras as efn
from keras.applications.imagenet_utils import decode_predictions
from efficientnet.keras import center_crop_and_resize, preprocess_input
import numpy as np

import keras.backend.tensorflow_backend as tb

model = efn.EfficientNetB0(weights='noisy-student')

image_size = model.input_shape[1]

print('model loading complete!')

def predict(image):

  x = center_crop_and_resize(image, image_size=image_size)
  image_modified = x
  x = preprocess_input(x)
  x = np.expand_dims(x, 0)

  # make prediction and decode
  tb._SYMBOLIC_SCOPE.value = True
  y = model.predict(x)
  res = decode_predictions(y)
  # collect result and the modified image
  data = { 'res': res[0][0], 'new_image': image_modified }
  return data
  