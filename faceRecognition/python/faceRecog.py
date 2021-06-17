import dlib
import io, os, glob
import numpy as np
import cv2



faces_folder_path = "face"
# 人臉對齊
detector = dlib.get_frontal_face_detector()

# 人臉關鍵點模型
predictor = dlib.shape_predictor( '/Users/stonetu/Learning/PYTHON/face_dataset/GazeTracking-master/gaze_tracking/trained_models/shape_predictor_68_face_landmarks.dat')

# 128維向量嵌入模型
face_rec_model_path = "/Users/stonetu/Learning/PYTHON/face_dataset/GazeTracking-master/gaze_tracking/trained_models/dlib_face_recognition_resnet_model_v1.dat"
facerec = dlib.face_recognition_model_v1(face_rec_model_path)


# 比對人臉描述子列表
descriptors = []
# 欲比對人臉名稱列表
candidate = []

# 針對比對資料夾裡每張圖片做比對:
for f in glob.glob(os.path.join(faces_folder_path, "*.jpg")):
    base = os.path.basename(f)
# 依序取得圖片檔案人名
    candidate.append(os.path.splitext(base)[ 0])
    img = cv2.imread(f)
    # 1.人臉偵測
    dets = detector(img, 0)
    for k, d in enumerate(dets):
    # 2.特徵點偵測
        shape = predictor(img, d)
    # 3.取得描述子，128維特徵向量
        face_descriptor = facerec.compute_face_descriptor(img, shape)    
    # 轉換numpy array格式
        v = np.array(face_descriptor)
        descriptors.append(v)


cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# 使用 XVID 編碼
fourcc = cv2.VideoWriter_fourcc(*'XVID')
# 建立 VideoWriter 物件，輸出影片至 output.avi
# FPS 值為 20.0，解析度為 640x360
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))
while True:
    ret, frame = cap.read()
    # 1.人臉偵測
    dets = detector(frame, 0)
    if len(dets)!=0:
        for k, d in enumerate(dets):
        # 2.特徵點偵測
            shape = predictor(frame, d)
        # 3.取得描述子，128維特徵向量
            face_descriptor = facerec.compute_face_descriptor(frame, shape)    
        # 轉換numpy array格式
            d_test = np.array(face_descriptor)
        # 計算歐式距離
        dist = []
        for i in descriptors:
            dist_ = np.linalg.norm(i - d_test)
            dist.append(dist_)
        # 將比對人名和比對出來的歐式距離組成一個dict
        cd = dict( zip(candidate,dist))
        cd_sorted = sorted(cd.items(), key = lambda d:d[1])
        print(cd_sorted)
        cv2.putText(frame, f'{cd_sorted[0][0]}:{cd_sorted[0][1]}', (30, 30), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 1)
    cv2.imshow(f"Face Recognition", frame)
    out.write(frame)
    k = cv2.waitKey(1)
    if k==27 or k==ord('q'):
        break
