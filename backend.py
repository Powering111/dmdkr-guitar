# Main backend code

import cv2
from LSTM.lstm import get_status
from YOLO.yolo import get_cropped_guitar
from TeachableMachine.padding import padding
from TeachableMachine.tm import predict_code
from sheet import make_sheet
from tqdm import tqdm

# filePath의 파일을 읽어서 코드를 생성. 리스트로 반환
def analyse_code(filePath,show=False):
    cap = cv2.VideoCapture(filePath)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frame_count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    now_frame_count=0
    progressbar = tqdm(total=total_frame_count)
    result=[]
    while cap.isOpened():
        now_frame_count+=1
        if now_frame_count>500:
            break
        progressbar.update(1)
        ret,img=cap.read()
        if not ret:
            break
        status,img=get_status(img,False)
        if status:
            #stroke 중이라면
            cropped_img,percent=get_cropped_guitar(img)
            if percent>0:
                # 기타가 인식되었다면
                #cv2.imshow('a',cropped_img)
                #cv2.waitKey(0)
                pd_img = padding(cropped_img)
                
                code = predict_code(pd_img).split()[1]

                #result.append({'time':now_frame_count/fps,'code':code})
                result.append(code)

                if show:
                    #test용
                    cv2.putText(pd_img, code, org=(0,50), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1, color=(255, 255, 255), thickness=2)
                    
                    cv2.imshow('jjj',img)
                    cv2.imshow('a',pd_img)
                    cv2.waitKey(1)
            else:
                result.append(0)
                #print('no guitar')
                if show:
                    cv2.imshow('jjj',img)
                    cv2.waitKey(1)
        else:
            result.append(0)
            #print('no stroke')
            if show:
                cv2.imshow('jjj',img)
                cv2.waitKey(1)
    progressbar.close()
    print('now frame count : ',now_frame_count)
    return result

# create sheet as image
def create_sheet(code,title,destinationPath):
    make_sheet(title,code,destinationPath)
    return code


# process 함수를 import 하여 사용하라.
# process video file and save sheet image
def process(filePath,title):
    code=analyse_code("uploads/"+filePath)
    create_sheet(code,title,'processed/'+filePath+'.musicxml')
    print("finished processing",filePath)
    
