import cv2
from keras.models import load_model
import numpy as np

model = load_model('Teachablemachine/model/keras_model.h5')
labels = open('Teachablemachine/model/labels.txt', 'r').readlines()

# 
def predict_code(image):
    image=cv2.cvtColor(image,cv2.COLOR_GRAY2BGR)
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224,3)
    image = (image / 127.5) - 1
    probabilities = model.predict(image,verbose=0)
    return labels[np.argmax(probabilities)]