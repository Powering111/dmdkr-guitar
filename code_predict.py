# 시연용 프로그램

import cv2
import numpy as np
from keras.models import load_model
from YOLO.yolo import get_cropped_guitar,draw_rect

# Load the model
model = load_model('TeachableMachine/model/keras_model.h5')

# CAMERA can be 0 or 1 based on default camera of your computer.
camera = cv2.VideoCapture(0)
#camera  =cv2.VideoCapture('시연용/LSTM_test.mp4')

# Grab the labels from the labels.txt file. This will be used later.
labels = open('TeachableMachine/model/labels.txt', 'r').readlines()

while True:
    # Grab the webcameras image.
    ret, raw_image = camera.read()
    # Resize the raw image into (224-height,224-width) pixels.
    # Show the image in a window
    try:
        raw_image=draw_rect(raw_image)
        cropped_image,percent = get_cropped_guitar(raw_image)
        if percent>0:
            image = cv2.resize(cropped_image, (224, 224), interpolation=cv2.INTER_AREA)
            # Make the image a numpy array and reshape it to the models input shape.
            image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
            # Normalize the image array
            image = (image / 127.5) - 1
            # Have the model predict what the current image is. Model.predict
            # returns an array of percentages. Example:[0.2,0.8] meaning its 20% sure
            # it is the first label and 80% sure its the second label.
            probabilities = model.predict(image,verbose=0)
            # Print what the highest value probabilitie label
            cv2.putText(raw_image, f'{labels[np.argmax(probabilities)]}', org=(50,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
            #print(labels[np.argmax(probabilities)])
    except Exception:
        pass
    finally:
        cv2.imshow("predicting",raw_image)
        # Listen to the keyboard for presses.
        keyboard_input = cv2.waitKey(1)
        # 27 is the ASCII for the esc key on your keyboard.
        if keyboard_input == 27:
            break

camera.release()
cv2.destroyAllWindows()