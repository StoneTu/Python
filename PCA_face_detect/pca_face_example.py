import numpy as np
from sklearn.datasets import fetch_olivetti_faces
faces, _ = fetch_olivetti_faces(data_home = '~/learning/PYTHON/scikit_learn_data', return_X_y=True,shuffle=True, random_state=0)

# print(faces.mean(axis=0))
from sklearn.decomposition import PCA


def getFileName(dirPath):
    from os import walk
    from os.path import isfile, isdir, join
    import math
    tmpNum = '000'
    for root, dirs, files in walk(dirPath):
        for f in files :
            fullpath = join(root, f)
            if isfile(fullpath):
                fileNum = fullpath[-7:-4]
                if fileNum.isnumeric():
                    tmpNum = fileNum if int(fileNum) > int(tmpNum) else tmpNum
    tmpNum = int(tmpNum)+1
    dig = math.floor(math.log10(int(tmpNum)))
    if dig == 0:
        tmpNum = f'00{tmpNum}'
    elif dig == 1:
        tmpNum = f'0{tmpNum}'
    return tmpNum
                    

def printAFace(fdataList, fTitle=None, saveFlag=True):
    # fdataList = [ row0_col0, row0_col1, row1_col0, row1_col1 ]
    import matplotlib.pyplot as plt
    if (fTitle==None):
        fTitle = [''] * len(fdataList)
    image_shape = (64, 64)
    col_max = 4
    n_col = len(fdataList) if len(fdataList)<col_max else col_max
    n_row = int(len(fdataList)/col_max)+1
    fig = plt.figure(figsize=(2. * n_col, 2.26 * n_row))
    plt.suptitle("Face image", size=16)
    for i, comp in enumerate(fdataList):
        plt.subplot(n_row, n_col, i + 1)
        plt.gca().title.set_text(fTitle[i])
        plt.axis("off")
        plt.imshow(comp.reshape(image_shape),
                cmap=plt.cm.gray,
                interpolation="nearest")
    if saveFlag:
        fileNum = getFileName("./savePNG")
        outPNG = "./savePNG/img-out-face"+ str(fileNum) +".png"
        plt.savefig(outPNG)
        plt.close(fig)
    else :
        plt.show()
def decompositeFace(number):
    face = faces[number]
    pca = PCA()
    pca.fit(faces)
    trans = pca.transform(face.reshape(1, -1))
    return face, pca, trans
def main():
    face, pca, trans = decompositeFace(1)
    print(len(pca.components_[0]))
    print(pca.components_)
    # printAFace([face]) # this is origin face
    # pca.components_[0] # this is eigenface
    # printAFace([pca.mean_])  # this is mean face
    # printAFace(np.concatenate((faces[:4], pca.components_[:4]))) # this is print 4 faces
    approxFace = [face]
    restoreNumAr = [1,40,80,160,240,320,399]
    for k in restoreNumAr:
        rankKApprox = trans[:, :k].dot(pca.components_[:k]) + pca.mean_
        approxFace.append(rankKApprox)

    inputTitle = ['origin']+restoreNumAr
    printAFace(approxFace, inputTitle)

if __name__ == '__main__':
    main()
    # printAFace([faces[0], faces[11]])