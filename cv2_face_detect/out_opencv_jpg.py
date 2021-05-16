import cv2
import base64
# from gaze_tracking import GazeTracking
# 載入分類器
# face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
# 從視訊盡頭擷取影片
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture("http://10.0.104.202:8000")
# 或者....
# 使用現有影片
i = 0
while i<50:
    i+=1
    # Read the frame
    _, img = cap.read()
# 轉成灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 偵測臉部
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
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
    ret, jpeg = cv2.imencode('.jpg', img)
    cv2.imwrite("./public/image/image.jpg", img)
    # rJpeg = jpeg.tobytes()
    # rJpeg = base64.b64encode(rJpeg).decode('utf-8')
    # print(rJpeg)
# Release the VideoCapture object
cap.release()