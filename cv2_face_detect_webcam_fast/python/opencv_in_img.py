import cv2
import base64
import sys
import io
import numpy as np
import time

# beginTime = time.time()
# 載入分類器
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
# loadFaceCas = time.time()
# print("Load face cascade: ", loadFaceCas- beginTime)
### code for test existing image
# img = cv2.imread(cv2.samples.findFile("./a.jpeg"))
# ret, jpeg = cv2.imencode('.jpg', img)
# # print("shape", jpeg.shape, "type", jpeg.dtype)
# # rJpeg = jpeg.tobytes()
# # lines = base64.b64encode(rJpeg).decode('utf-8')
# loadImg = time.time()
# print("load image: ", loadImg - loadFaceCas)

### code for receive string image from user 
num = 0
while num !="-1":
    lines = input() ### This's for multiple input from node
    # lines = sys.stdin.readline()  ### not work for multiple input
    # lines = sys.stdin.readlines() ### not work for multiple input
    lines = [line.rstrip() for line in lines]
    # print("org:",lines[:10])
    lines = ''.join(lines)
    lineL = lines.split(",")
    num = lineL[0]
    lines = lineL[1]
    # print("join:",lines[:10])
    lines = lines.encode('utf-8')
    # print("encode:",lines[:10])
    lines = base64.b64decode(lines)
    # print("b64decode:",lines[:10])
    lines = np.frombuffer(lines, dtype="uint8").reshape(-1,1)
    # print("np array shape:",lines.shape)
    # reconstruct image as an numpy array
    img = cv2.imdecode(lines, cv2.IMREAD_UNCHANGED)

    # 轉成灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 偵測臉部
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # detectFace = time.time()
    # print("detect face: ", detectFace - loadImg)
    # 繪製人臉部份的方框
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        h1=int(float(h/1.5))
        gray_facehalf = gray[y:(y+h1), x:x+w]
        eyes = eye_cascade.detectMultiScale(gray_facehalf, 1.1, 4)
        # 繪製眼睛方框
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(img, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (255, 0, 0), 2)
        # 顯示成果
        # time.sleep(1)
    ret, jpeg = cv2.imencode('.jpg', img)
    rJpeg = jpeg.tobytes()
    rJpeg = base64.b64encode(rJpeg).decode('utf-8')


    # PaintFace = time.time()
    # print("Paint face: ", PaintFace - detectFace)

    print(f"{num},{rJpeg}")
    # print(rJpeg)
    # cv2.imwrite( "result.jpg", img)