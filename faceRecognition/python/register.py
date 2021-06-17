import dlib
import io, os, glob, base64
import numpy as np
import cv2

# 人臉對齊
detector = dlib.get_frontal_face_detector()
# 人臉關鍵點模型
predictor = dlib.shape_predictor( '/Users/stonetu/Learning/PYTHON/face_dataset/GazeTracking-master/gaze_tracking/trained_models/shape_predictor_68_face_landmarks.dat')
# predictor = dlib.shape_predictor( 'dlib/shape_predictor_68_face_landmarks.dat')
# 128維向量嵌入模型
face_rec_model_path = "/Users/stonetu/Learning/PYTHON/face_dataset/GazeTracking-master/gaze_tracking/trained_models/dlib_face_recognition_resnet_model_v1.dat"
# face_rec_model_path = "dlib/dlib_face_recognition_resnet_model_v1.dat"
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
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
print((descriptors))
