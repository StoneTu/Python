import cv2
import mediapipe as mp
import time
import numpy as np
from tensorflow import keras
import sys
from fpsClass import runWithFPS
'''
Fatigue :0 == normal
Fatigue :1 == abnormal
'''
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
FACEMESH_SIZE = 468
def visualFacemesh(data):
    SIZE = 100
    newImg = np.zeros((SIZE,SIZE))
    for i in range(int(len(data))):
        y = int(data[i][1]*SIZE)-1
        x = int(data[i][0]*SIZE)-1
        newImg[y][x] = 255
    # cv2.imwrite("visual.jpg",newImg)
    newImg = np.asarray(newImg, dtype="uint8")
    return newImg

def processFacemesh(image, drawImageFlag=False):
    with mp_face_mesh.FaceMesh(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as face_mesh:
        image.flags.writeable = False
        results = face_mesh.process(image)
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        tmpRow = []
        if results.multi_face_landmarks:
            for n,j in enumerate(results.multi_face_landmarks[0].landmark):
                # tmpRow.extend([j.x, j.y])
                tmpRow.append([j.x, j.y])
            if drawImageFlag:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=image,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACE_CONNECTIONS,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec=drawing_spec)
        return tmpRow
def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img
def MinMaxNormalize(row):
    # newArr = []
    # for row in npArr:
    #     newArr.append([(x-row.min())/(row.max()+row.min()) for x in row])
    # return np.array(newArr)
    row = np.array(row)
    rowx = row[:,0]
    rowy = row[:,1]
    rowx = np.array([(x-rowx.min())/(rowx.max()-rowx.min()) for x in rowx])
    rowy = np.array([(x-rowy.min())/(rowy.max()-rowy.min()) for x in rowy])
    x = rowx.reshape((-1,1))
    y = rowy.reshape((-1,1))
    row = np.concatenate([x, y], axis=1)
    return row
def dataProcessCNN(data):
    tmpRow = MinMaxNormalize(data)
    visImg = visualFacemesh(tmpRow)
    return visImg

def main():
    inputName = sys.argv[1]
    mp_face_mesh = mp.solutions.face_mesh
    CNN_model = keras.models.load_model('./model/faceFatigueCNN.h5')
    if inputName=="0":
        inputName = 0
    cap = cv2.VideoCapture(inputName)
    # cap = cv2.VideoCapture("./video/normal/normal_car.mov")
    # cap = cv2.VideoCapture("./video/abnormal/abnormal.mov")
    thisFPS = runWithFPS()
    while cap.isOpened():
        thisFPS.start()
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            break
        # image = increase_brightness(image)
        tmpRow = processFacemesh(image)
        if (len(tmpRow)== FACEMESH_SIZE): ### prevent facemesh fail
            tmpRow = dataProcessCNN(tmpRow)
            tmpRow = tmpRow / 255.0
            X_test = np.reshape(tmpRow, (-1, 100, 100, 1 ))
            y_pred = CNN_model.predict(X_test)
            if y_pred[0][1] >0.5:
                print(1)
            else :
                print(0)
            cv2.putText(image, f"Fatigue: {y_pred[0][1]:.2f}", (30, 60), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)
        thisFPS.end(image)
        cv2.imshow("Driver View", image)
        keyin = cv2.waitKey(1)
        if keyin == 27 or keyin==ord("q"):
            break

if __name__=="__main__":
    main()