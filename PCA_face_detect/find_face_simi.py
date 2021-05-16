from pca_face_example import *
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def collectFaceTrans(number):
    faces = []
    pcas = []
    transList = []
    for i in range(number):
        face, pca, trans = decompositeFace(i)
        faces.append(face)
        pcas.append(pca)
        transList.append(trans[0])
    return faces, pcas, transList
def calSimilarity(users, rating_matrix):
    cos_sims = cosine_similarity(rating_matrix)
    sims_df = pd.DataFrame(cos_sims, columns = users, index = users)
    sortedIdxSims = []
    for user in cos_sims:
        tmpList = sorted(range(len(user)), key=lambda k: user[k], reverse=True)
        sortedIdxSims.append(tmpList)
    # print(sims_df)
    # print(sortedIdxSims)
    return cos_sims, sortedIdxSims

# 尋找相似度最高的圖片
number = 400
highNumber = 5
print("decompositing faces...")
faces, pcas, transList = collectFaceTrans(number)
print("calculating similarity...")
cos_sims, sortedIdxSims = calSimilarity(range(number), transList)
# random pick faces
print("random picking up some faces and generating images...")
from random import sample
l = range(number) 
randList = (sample(l, 10))
for i in randList:
    fTitle = []
    pFaces = []
    for j in range(highNumber):
        fTitle.append(cos_sims[i][sortedIdxSims[i][j]])
        pFaces.append(faces[sortedIdxSims[i][j]])
    printAFace(pFaces, fTitle)