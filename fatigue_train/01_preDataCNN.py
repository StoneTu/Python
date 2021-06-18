import cv2
import mediapipe as mp
import time
import numpy as np
import os
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)

videoSource1 = "./video/normal"
outFile1 = "./csv/normalCNN.csv"
videoSource2 = "./video/abnormal"
imageSource2 = "./video/abnormal/img"
outFile2 = "./csv/abnormalCNN.csv"

# FACEMESH_SIZE = 936
FACEMESH_SIZE = 468
LEFT_EYE_POINTS = [33, 246,161,160,159,158,157,173,133,155,154,153,145,144,163,7]
RIGHT_EYE_POINTS = [362,398,384,385,386,387,388,466,263,249,390,373,374,380,381,382]
MOUTH_POINTS = [78,183,42,41,82,13,312,271,272,308,324,318,402,317,14,87,178,88,95]
def getVideoNameList(path):
    vnameList = []
    inameList = []
    for videoName in os.listdir(path):
        appName =  videoName[-3:]
        if appName == 'mov' or appName == 'mp4':
            vnameList.append(os.path.join(path,videoName))
        elif appName == 'jpg' or appName == 'png':
            inameList.append(os.path.join(path,videoName))
    return vnameList, inameList
def getFaceArea(points):
    leftEye = []
    rightEye = []
    mouth = []
    for i in LEFT_EYE_POINTS:
        leftEye.append(points[i])
    for i in RIGHT_EYE_POINTS:
        rightEye.append(points[i])
    for i in MOUTH_POINTS:
        mouth.append(points[i])
    leftEye = np.asarray(np.array(leftEye)*100,dtype="int64")
    lEyeArea = cv2.contourArea(leftEye)
    rightEye = np.asarray(np.array(rightEye)*100,dtype="int64")
    rEyeArea = cv2.contourArea(np.array(rightEye))
    mouth = np.asarray(np.array(mouth)*100,dtype="int64")
    mouthArea = cv2.contourArea(np.array(mouth))
    return lEyeArea, rEyeArea, mouthArea
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
def dataProcess(data):
    tmpRow = MinMaxNormalize(data)
    visImg = visualFacemesh(tmpRow)
    a,b,c = getFaceArea(tmpRow)
    tmpRow = np.array(tmpRow).reshape((-1,))
    tmpRow = np.append(tmpRow,np.array([a,b,c]))
    return tmpRow
def dataProcessCNN(data):
    tmpRow = MinMaxNormalize(data)
    visImg = visualFacemesh(tmpRow)
    return visImg
    
def getFacemeshInfoImg(imgSource):
    dataList = []
    imageTmp = cv2.imread(imgSource)
    tmpRow = processFacemesh(imageTmp)
    if (len(tmpRow)== FACEMESH_SIZE): ### prevent facemesh fail
        tmpRow = dataProcessCNN(tmpRow)
        dataList.append(tmpRow)
        # visImg = cv2.resize(visImg,(imageTmp.shape[0], imageTmp.shape[0]))
        # gray = cv2.cvtColor(imageTmp, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("gray",cv2.hconcat([gray,visImg]))
        # cv2.waitKey(0)
    imageFlip = cv2.flip(imageTmp, 1)
    tmpRow = processFacemesh(imageFlip)
    if (len(tmpRow)== FACEMESH_SIZE): ### prevent facemesh fail
        tmpRow = dataProcessCNN(tmpRow)
        dataList.append(tmpRow)
    dataList = np.asarray(dataList)
    print(f"{imgSource} collected data shape: ",dataList.shape)
    return dataList
def getFacemeshInfoVdo(videoSource):
    cap = cv2.VideoCapture(videoSource)
    videoFps = cap.get(cv2.CAP_PROP_FPS)
    print(" FPS: ", videoFps)
    dataList = []
    frameSelect = 0
    while cap.isOpened():
        success, image = cap.read()
        frameSelect += 1
        if not success:
            print("Ignoring empty camera frame.")
            break
        ### analysis frame per 5 frames
        elif frameSelect%5 != 0:
            continue
        tmpRow = processFacemesh(image)
        if (len(tmpRow)== FACEMESH_SIZE): ### prevent facemesh fail
            tmpRow = dataProcessCNN(tmpRow)
            dataList.append(tmpRow)
            # visualFacemesh(tmpRow)
    dataList = np.asarray(dataList)
    print(f"{videoSource} collected data shape: ",dataList.shape)
    return dataList
def main():
    video2Names, _ = getVideoNameList(videoSource2)
    _, image2Names = getVideoNameList(imageSource2)
    video2NpArrays = np.array([])
    for name in video2Names:
        print(f"Opening {name} and get facemesh data...")
        # newNpArr = getFacemeshInfo(name)
        newNpArr = getFacemeshInfoVdo(name)
        if video2NpArrays.size == 0:
            video2NpArrays = newNpArr
        elif newNpArr.size > 0:
            video2NpArrays = np.concatenate((video2NpArrays, newNpArr))
    for name in image2Names:
        print(f"Opening {name} and get facemesh data...")
        newNpArr = getFacemeshInfoImg(name)
        if video2NpArrays.size == 0:
            video2NpArrays = newNpArr
        elif newNpArr.size > 0:
            video2NpArrays = np.concatenate((video2NpArrays, newNpArr))
    video2NpArrays = np.reshape(video2NpArrays, (video2NpArrays.shape[0],10000))
    np.savetxt(outFile2, video2NpArrays, delimiter=",")

    video1Names, _ = getVideoNameList(videoSource1)
    video1NpArrays = np.array([])
    for name in video1Names:
        print(f"Opening {name} and get facemesh data...")
        # newNpArr = getFacemeshInfo(name)
        newNpArr = getFacemeshInfoVdo(name)
        if video1NpArrays.size == 0:
            video1NpArrays = newNpArr
        elif newNpArr.size > 0:
            video1NpArrays = np.concatenate((video1NpArrays, newNpArr))
    video1NpArrays = np.reshape(video1NpArrays, (video1NpArrays.shape[0],10000))
    np.savetxt(outFile1, video1NpArrays, delimiter=",")

if __name__=="__main__":
    main()