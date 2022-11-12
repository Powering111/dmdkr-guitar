import torch
model = torch.hub.load('YOLO/yolov5','custom',path='YOLO/YOLO_weight/best.pt',source="local")

# return : 이미지(opencv img), 확신도(float). 확신도가 0이면 기타 인식 실패로 간주
def get_cropped_guitar(img):
    try:
        result=model(img,)
        area=result.xyxy[0][0].tolist()
        x1=int(area[0])
        y1=int(area[1])
        x2=int(area[2])
        y2=int(area[3])
        percent=area[4]
        
        img=img[y1:y2,x1:x2]
        return img,percent
    except Exception as e:
        return img,0

import cv2
def draw_rect(img):
    result=model(img,)
    area=result.xyxy[0][0].tolist()
    x1=int(area[0])
    y1=int(area[1])
    x2=int(area[2])
    y2=int(area[3])
    
    percent=area[4] # 예측 확신도
    #print(percent)
    
    #자르지 않고 사각형을 그려서 보이기
    img=cv2.rectangle(img,(int(area[0]),int(area[1])),(int(area[2]),int(area[3])),(255,0,0),3)
    return img