## 利用Mediapipe facemesh取得特徵點，進行人臉疲勞度判定

Google Mediapipe facemesh一共會抓取人臉特徵點468點，每點有(x,y,z)三個數值，嘗試取出(x,y)後拉平向量為(936,)維度，或是採用(468,2)維度丟入CNN神經網路訓練，結果都非常不理想，個人推測原因可能是如此處理資料無法建立點與點之間的相對關係，例如上眼皮點與下眼皮點靠近時應該要有特別意義，所以將這些特徵點再轉成(100,100) binary陣列，若輸出成圖示如下：
<br><img src="visual.jpg"><br>
將這陣列輸入到CNN神經網路訓練，終於得到比較收斂的成果
<br>建立日期06/17/2021<br>
1. 
    資料準備：
    如上所述，將訓練圖片或影片利用opencv讀入，用Mediapiep facemesh輸出特徵點資料，將這些資料儲存為文字型態檔案，方便後續讀取，亦可上傳到colab利用GPU train CNN model
2. 
    因筆者電腦沒有GPU，所以選擇上傳到colab train
```
import pandas as pd
import numpy as np
from tensorflow.keras import layers
from tensorflow import keras
from tensorflow.keras.utils import to_categorical, plot_model

dfObj1 = pd.read_csv('/fatigue_train/normalCNN.csv', header=None)
dfObj2 = pd.read_csv('/fatigue_train/abnormalCNN.csv', header=None)
label1 = pd.DataFrame(np.zeros(dfObj1.shape[0]))
label2 = pd.DataFrame(np.ones(dfObj2.shape[0]))
X_train = pd.concat([dfObj1,dfObj2], ignore_index=True)
y_train = pd.concat([label1,label2], ignore_index=True)
X_train = np.asarray(X_train)
y_train = np.asarray(y_train)
y_train = to_categorical(y_train)
y_train = y_train.reshape((-1, 2))

X_train = np.reshape(X_train, (X_train.shape[0], 100, 100, 1))
X_train = X_train / 255.0
indices = np.arange(X_train.shape[0])
np.random.shuffle(indices)
X_train = X_train[indices]
y_train = y_train[indices]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.1, random_state=10)

model = keras.Sequential()
model.add(layers.Conv2D(1000, (3, 3), activation='relu', input_shape=(100, 100, 1)))
model.add(layers.MaxPooling2D((3, 3)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((3, 3)))
model.add(layers.Dropout(.2))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(2, activation='softmax'))

model.compile(loss='categorical_crossentropy',
              optimizer='Adam',
              metrics=['accuracy'])
print(model.summary())
train_history = model.fit(
  x=X_train,
  y=y_train,
  validation_split=0.1,
  epochs=300,
  batch_size=100,
)
model.save('/fatigue_train/faceFatigueCNN.h5')
```
3.
    經過一段時間訓練，得到如下結果
```
Epoch 295/300
21/21 [==============================] - 9s 423ms/step - loss: 8.9864e-05 - accuracy: 1.0000 - val_loss: 0.6941 - val_accuracy: 0.9058
Epoch 296/300
21/21 [==============================] - 9s 423ms/step - loss: 2.8819e-04 - accuracy: 1.0000 - val_loss: 0.7336 - val_accuracy: 0.9193
Epoch 297/300
21/21 [==============================] - 9s 424ms/step - loss: 2.0778e-04 - accuracy: 1.0000 - val_loss: 0.7166 - val_accuracy: 0.9193
Epoch 298/300
21/21 [==============================] - 9s 423ms/step - loss: 6.6501e-05 - accuracy: 1.0000 - val_loss: 0.7184 - val_accuracy: 0.9193
Epoch 299/300
21/21 [==============================] - 9s 425ms/step - loss: 1.3606e-05 - accuracy: 1.0000 - val_loss: 0.7206 - val_accuracy: 0.9193
Epoch 300/300
21/21 [==============================] - 9s 423ms/step - loss: 2.3677e-05 - accuracy: 1.0000 - val_loss: 0.7194 - val_accuracy: 0.9193
Test accuracy: 83.9%
```

