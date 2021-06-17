## 臉部識別的登入服務

製作駕駛監測系統專案時，其中有一項臉部登入功能，利用dlib 68點人臉特徵點比對出資料庫最相似的特徵，這裡將這功能獨立呈現出來
<br>建立日期06/12/2021<br>
1. 
    載入dlib模型：
```
# 人臉對齊
detector = dlib.get_frontal_face_detector()
# 人臉關鍵點模型
predictor = dlib.shape_predictor( 'yourPath/shape_predictor_68_face_landmarks.dat')
# 128維向量嵌入模型
face_rec_model_path = "yourPath/dlib_face_recognition_resnet_model_v1.dat"
facerec = dlib.face_recognition_model_v1(face_rec_model_path)
descriptors = []
```
2. 
    將特徵點轉為numpy array格式，以便後續存入資料庫中
```
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
```
3.
    比對資料庫中所有的臉部特徵資料，找出最相近的，再設定一個threshold來判斷是否為同一人<br>
    faceArrayList為去讀取資料庫中所有臉部資料的list<br>
    nameList為其相對應的姓名<br>
    FACE_THRESHOLD為最後的判斷閥值，小於此值才判斷為同一人
```
# 計算歐式距離
dist = []
for i in faceArrayList:
    dist_ = np.linalg.norm(i - inputFacrArray)
    dist.append(dist_)
# 將比對人名和比對出來的歐式距離組成一個dict
cd = dict( zip(nameList,dist))
cd_sorted = sorted(cd.items(), key = lambda d:d[1])
if (cd_sorted[0][1]< FACE_THRESHOLD):
    code = 0
else:
    code = 1
outMsg = f'"code":{code}, "result":"{cd_sorted[0][0]}"'
outMsg = "{"+outMsg+"}"
```