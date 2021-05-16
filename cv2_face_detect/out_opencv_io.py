import cv2
import base64
# from gaze_tracking import GazeTracking
# 載入分類器
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye_tree_eyeglasses.xml')
img = cv2.imread(cv2.samples.findFile("./public/a.jpeg"))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 偵測臉部
faces = face_cascade.detectMultiScale(gray, 1.1, 4)
#detectMultiScale参数（图像，每次缩小图像的比例，匹配成功所需要的周围矩形框的数目，检测的类型，匹配物体的大小范围）
# 繪製人臉部份的方框
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    h1=int(float(h/1.5))
    gray_facehalf = gray[y:(y+h1), x:x+w]
    eyes = eye_cascade.detectMultiScale(gray_facehalf, 1.1, 4)
    # 繪製眼睛方框
    for (ex, ey, ew, eh) in eyes:
        cv2.rectangle(img, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (255, 0, 0), 2)
ret, jpeg = cv2.imencode('.jpg', img)
# show image in window
cv2.imshow("Display window", img)
k = cv2.waitKey(0)
if k == ord("q"):
    cv2.destroyAllWindows()
# print(jpeg[:10])
rJpeg = jpeg.tobytes()
# print("jpeg.tobytes()",rJpeg[:10])
# print("base64.b64encode(rJpeg)",base64.b64encode(rJpeg)[:10])
rJpeg = base64.b64encode(rJpeg).decode('utf-8')
# print("decode('utf-8')",rJpeg[:10])
# rStr = rJpeg
print(rJpeg)
### following save to base64 and jpg ###
# with open('bytesImgBase64.txt', 'w') as f:
#     f.write(rStr)
# print(rStr[:100])
# base64_img_bytes = rStr.encode('utf-8')
# with open('decoded_image.jpg', 'wb') as file_to_save:
#     decoded_image_data = base64.decodebytes(base64_img_bytes)
#     file_to_save.write(decoded_image_data)