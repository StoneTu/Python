import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn import preprocessing
import numpy as np
from tensorflow.keras import layers
from tensorflow import keras
from tensorflow.keras.utils import to_categorical, plot_model

dfObj1 = pd.read_csv("./csv/normalCNN.csv", header=None)
dfObj2 = pd.read_csv("./csv/abnormalCNN.csv", header=None)
label1 = pd.DataFrame(np.zeros(dfObj1.shape[0]))
label2 = pd.DataFrame(np.ones(dfObj2.shape[0]))
X_train = pd.concat([dfObj1,dfObj2], ignore_index=True)
y_train = pd.concat([label1,label2], ignore_index=True)
X_train = np.asarray(X_train)
y_train = np.asarray(y_train)

# from sklearn import preprocessing
# scaler = preprocessing.StandardScaler().fit(X_train)
# # scaler = preprocessing.MinMaxScaler().fit(X_train)
# X_train = scaler.transform(X_train)
def MinMaxNormalize(npArr):
    newArr = []
    for row in npArr:
        newArr.append([(x-row.min())/(row.max()+row.min()) for x in row])
    return np.array(newArr)
def MinMaxNormalizeLast3(npArr):
    print(npArr[-3:])
    for i in range(-1,-4,-1):
        thisColumn = npArr[:,i]
        thisColumn = np.array([(x-thisColumn.min())/(thisColumn.max()-thisColumn.min()) for x in thisColumn])
        npArr[:,i] = thisColumn
    print(npArr[-3:])
    # return np.array(newArr)

# X_train = X_train.reshape((-1, 936 ))
# X_train = MinMaxNormalizeLast3(X_train)
y_train = to_categorical(y_train)
y_train = y_train.reshape((-1, 2))
print(X_train.shape)
print(y_train.shape)

X_train = np.reshape(X_train, (X_train.shape[0], 100, 100, 1))
X_train = X_train / 255.0
indices = np.arange(X_train.shape[0])
np.random.shuffle(indices)
X_train = X_train[indices]
y_train = y_train[indices]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.1, random_state=1)

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
            #   optimizer='rmsprop',
              metrics=['accuracy'])
print(model.summary())
train_history = model.fit(
  x=X_train,
  y=y_train,
  validation_split=0.1,
  epochs=100,
  batch_size=100,
)
model.save("./model/faceFatigueCNN.h5")
# y_pred = model.predict(X_test)
new_model = keras.models.load_model('./model/faceFatigueCNN.h5')
_, acc = model.evaluate(X_test,
                        y_test,
                        batch_size=100,
                        verbose=0)
print("\nTest accuracy: %.1f%%" % (100.0 * acc))
# print("y_test: ", y_test)
# print("y_pred: ", y_pred)
'''
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
'''