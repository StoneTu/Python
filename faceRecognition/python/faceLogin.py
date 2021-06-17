import dlib
import io, os, glob, base64
import numpy as np
import cv2
import logging


logging.basicConfig(level=logging.DEBUG)

# 人臉對齊
detector = dlib.get_frontal_face_detector()
# 人臉關鍵點模型
predictor = dlib.shape_predictor( '/Users/stonetu/Learning/PYTHON/face_dataset/GazeTracking-master/gaze_tracking/trained_models/shape_predictor_68_face_landmarks.dat')
# 128維向量嵌入模型
face_rec_model_path = "/Users/stonetu/Learning/PYTHON/face_dataset/GazeTracking-master/gaze_tracking/trained_models/dlib_face_recognition_resnet_model_v1.dat"
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
FACE_THRESHOLD = 0.4
def solveFaceImg():
    # 比對人臉描述子列表
    descriptors = []
    lines = input() ### This's for multiple input from node
    lines = [line.rstrip() for line in lines]
    lines = ''.join(lines)
    lines = base64.b64decode(lines)
    lines = np.frombuffer(lines, dtype="uint8").reshape(-1,1)
    # # reconstruct image as an numpy array
    img = cv2.imdecode(lines, cv2.IMREAD_UNCHANGED)
    # 1.人臉偵測
    dets = detector(img, 0)
    for k, d in enumerate(dets):
    # 2.特徵點偵測
        shape = predictor(img, d)
    # 3.取得描述子，128維特徵向量
        face_descriptor = facerec.compute_face_descriptor(img, shape)    
    # 轉換numpy array格式
        v = np.array(face_descriptor)
        descriptors.append(list(v))
    descriptors = np.reshape(np.array(descriptors), (-1,))
    logging.debug("Solve face shape:"+str(descriptors.dtype))
    return descriptors

def readAllFaceArray():
    lines = input() ### This's for multiple input from node
    lines = [line.rstrip() for line in lines]
    lines = ''.join(lines)
    nameList = lines.split(",")
    logging.debug("Read name:"+str(nameList))
    # lines = base64.b64decode(lines)
    # logging.debug("Read All:"+str(lines))
    # lines = np.frombuffer(lines, dtype="uint8").reshape(-1,1)
    # logging.debug("Read All:"+str(lines))
    lines = input() ### This's for multiple input from node
    lines = [line.rstrip() for line in lines]
    lines = ''.join(lines)
    faceArrayList = lines.split(",")
    faceArrayList = np.array(faceArrayList, dtype='float64')
    faceArrayList = np.reshape(faceArrayList, (len(nameList),-1))
    logging.debug("Read face shape:"+str(faceArrayList.dtype))
    return nameList, faceArrayList

def main():
    logging.debug("Face login python start.")
    inputFacrArray = solveFaceImg()
    logging.debug("Read face from node")
    nameList, faceArrayList = readAllFaceArray()
    # 計算歐式距離
    dist = []
    for i in faceArrayList:
        dist_ = np.linalg.norm(i - inputFacrArray)
        dist.append(dist_)
    # 將比對人名和比對出來的歐式距離組成一個dict
    cd = dict( zip(nameList,dist))
    cd_sorted = sorted(cd.items(), key = lambda d:d[1])
    logging.debug(cd_sorted)
    if (cd_sorted[0][1]< FACE_THRESHOLD):
        code = 0
    else:
        code = 1
    outMsg = f'"code":{code}, "result":"{cd_sorted[0][0]}"'
    outMsg = "{"+outMsg+"}"
    print(outMsg)
main()