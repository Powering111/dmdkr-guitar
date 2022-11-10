import glob

import cv2
import mediapipe as mp
import numpy as np
import time
import os

actions = ['stroke','stop']
seq_length = 5
secs_for_action = 30

# MediaPipe hands model
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
created_time = int(time.time())
os.makedirs('LSTM/processed_data', exist_ok=True)
# Create sequence data
last_seq=0
for idx, action in enumerate(actions):
    video_list = glob.glob(f'LSTM/database/{action}/*.mp4')
    full_seq_data = []

    i=0
    cap = cv2.VideoCapture(video_list[i])
    data = []
    start_time = time.time()
    while True:
        ret, img = cap.read()
        if not ret:
            i = i + 1
            if(len(data)>0):
                data = np.array(data)
                
                #print(data.shape)
                if len(data)>=seq_length:
                    for seq in range(len(data) - seq_length):
                        full_seq_data.append(data[seq:seq+seq_length])

                data=[]
                print(i)
            if i < len(video_list):
                cap = cv2.VideoCapture(video_list[i])
                continue
            else:
                break
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        if result.multi_hand_landmarks is not None:
            for res in result.multi_hand_landmarks:
                joint = np.zeros((21, 4))
                lefthand = True
                for j, lm in enumerate(res.landmark):
                    joint[j] = [lm.x, lm.y, lm.z, lm.visibility]
                    if lm.x > 0.5:
                        lefthand=False
                        break
                if not lefthand:
                    continue

                # START
                
                # Compute angles between joints
                v1 = joint[[0,1,2,3,0,5,6,7,0,9,10,11,0,13,14,15,0,17,18,19], :3] # Parent joint
                v2 = joint[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20], :3] # Child joint
                v = v2 - v1 # [20, 3]
                # Normalize v
                v = v / np.linalg.norm(v, axis=1)[:, np.newaxis]

                # Get angle using arcos of dot product
                angle = np.arccos(np.einsum('nt,nt->n',
                    v[[0,1,2,4,5,6,8,9,10,12,13,14,16,17,18],:],
                    v[[1,2,3,5,6,7,9,10,11,13,14,15,17,18,19],:])) # [15,]

                angle = np.degrees(angle) # Convert radian to degree

                angle_label = np.array([angle], dtype=np.float32)
                angle_label = np.append(angle_label, idx)
                
                d = np.concatenate([joint.flatten(), angle_label])
                #print(d)
                # END

                data.append(d)
                #print(len(data))
                #mp_drawing.draw_landmarks(img, res, mp_hands.HAND_CONNECTIONS)

        #cv2.imshow('img', img)
    #input()

    #for seq in range(len(data) - seq_length):
        #full_seq_data.append(data[seq:seq + seq_length])

    full_seq_data = np.array(full_seq_data)
    print(action, full_seq_data.shape)
    #print(full_seq_data)
    np.save(os.path.join('LSTM/processed_data', f'seq_{action}'), full_seq_data)
