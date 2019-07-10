from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
from keras.backend.tensorflow_backend import set_session
import tensorflow as tf
import numpy as np
from time import perf_counter # performance

'''
    Simple program that uses the pretrained resnet model from keras to
    predict the object in /data/image.jpg of the container
'''


config = tf.ConfigProto()
config.intra_op_parallelism_threads = 1
config.inter_op_parallelism_threads = 1

model = ResNet50(weights='imagenet')

image_path = "/data/image.jpg"
img = image.load_img(image_path, target_size=(224, 224))
x = image.img_to_array(img)
x = np.expand_dims(x, axis=0)
x = preprocess_input(x)


start = perf_counter()
res = model.predict(x)
print('prediction time: {}'.format(perf_counter() - start))
print('Prediction: {}'.format(decode_predictions(res, top=3)))

