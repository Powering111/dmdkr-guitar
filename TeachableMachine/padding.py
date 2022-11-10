import cv2
import numpy as np

# img를 받아서 padding 해서 return
def padding(img):
  img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
  h,w = img.shape
  if(h>w):
    percent = 500/h
  else:
    percent = 500/w

  resize_img = cv2.resize(img,dsize=(0,0),fx=percent,fy=percent)
  #print(resize_img.shape)


  h,w = resize_img.shape
  margin = [np.abs(h - w) // 2, np.abs(h - w) // 2]
  if np.abs(h - w) % 2 != 0:
    margin[0] += 1
  if h < w:
    margin_list = [margin, [0, 0]]
  else:
    margin_list = [[0, 0], margin]

  pd_img = np.pad(resize_img, margin_list, mode='constant',constant_values=0)

  return pd_img