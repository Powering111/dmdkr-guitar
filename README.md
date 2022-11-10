# 으악 기타
> 영상을 통한 기타 악보 자동 생성 프로그램

**전국 고등학교 동아리 소프트웨어 경진대회** 참가 작품

경남과학고등학교 동아리 '*으악구아노*'



## 간략한 설명

server.py : 웹 서버. 엔트리 포인트

backend.py : 기타 영상 처리의 모든 것을 담당

sheet.py : 악보 생성 모듈

processed 폴더와 uploads 폴더 필요

### LSTM
오른손 스트로크 여부를 판단. LSTM 폴더에서 처리함.

database : database/stroke, database/stop 폴더에 스트로크/정지 영상을 넣어 놓음

processed_data : 손 인식 및 시퀀싱된 데이터들을 numpy 바이너리 형태로 저장

models : keras 모델을 저장

*lstm.py*가 참조됨.

*process_dataset.py*에서 database 폴더를 읽어 전처리를 거친 후 processed_data에 저장.

*train.py*에서 processed_data를 읽어 keras 모델을 학습시켜 models 폴더에 저장.

*test.py*는 카메라(코드 수정 시 동영상 파일도 가능)에서 실시간으로 손가락을 인식하고 stroke/stop 분류

### YOLO
기타 목 부분을 인식하여 자르기. YOLO 폴더에서 처리함.

YOLO_weight : YOLO로 학습된 pyTorch 모델이 저장됨.

dataset : YOLO를 학습시키기 위해 사용된 데이터셋을 저장해 놓음.

*yolo.py*가 참조됨.

*use_yolo.py*에서 카메라를 이용하여 테스트해 볼 수 있음.

*neck_train.ipynb*(Google Colab)에서 기타 목 인식 데이터를 학습

*neck_detect.ipynb*(Google Colab)에서 기타 목 인식을 테스트할 수 있음(이미지로 저장)

### TeachableMachine
잘린 기타 사진을 통해 왼손 코드를 분류. TeachableMachine 폴더에서 처리함.

model : keras 모델이 들어 있음.

*tm.py*가 참조됨.

*padding.py* : 이미지에 대하여 padding 작업을 실행하는 모듈

*predict.py*에서 실시간으로 카메라를 이용하여 테스트할 수 있음.


### music21
연속적인 코드 배열을 입력받아 악보를 생성, 저장. sheet.py에서 처리함


## 사용방법

Python 3.10 (또는 유사 버전)

```pip install -r python-requirements.txt``` 실행

[yolov5 필요.](https://github.com/ultralytics/yolov5) 최신 커밋을 다운로드하여 YOLO/yolov5 폴더에 넣기

## music21 설정.

MuseScore 설치
```
from music21 import *
configure.run()
```
실행 후 질문에 응답해야 함.