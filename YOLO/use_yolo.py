#test code

import torch
import cv2
model = torch.hub.load('YOLO/yolov5', 'custom', path='YOLO/YOLO_weight/best.pt', source="local")

cap=cv2.VideoCapture(0)
#cap=cv2.VideoCapture('C:/Users/CSI/Desktop/으악기타/datasetcreate/videos/WIN_20220904_17_13_59_Pro.mp4')
while cap.isOpened():
    ret,img=cap.read()
    result=model(img,)
    area=result.xyxy[0][0].tolist()
    x1=int(area[0])
    y1=int(area[1])
    x2=int(area[2])
    y2=int(area[3])
    
    percent=area[4] # 예측 확신도
    print(percent)
    
    #자르지 않고 사각형을 그려서 보이기
    #img=cv2.rectangle(img,(int(area[0]),int(area[1])),(int(area[2]),int(area[3])),(255,0,0),3)
    #cv2.imshow('asdf',img)


    #잘라서 보여주기
    cv2.imshow('asdf',img[y1:y2,x1:x2])
    cv2.waitKey(1)