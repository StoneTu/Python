import sys
import numpy as np
import pandas as pd
import ast
from sklearn.metrics.pairwise import cosine_similarity

args1 = sys.argv[1]
args2 = sys.argv[2]

def mod(vec):
    x = np.sum(vec**2)
    return x**0.5

def sim(vec1, vec2):
    s = np.dot(vec1, vec2) / mod(vec1) / mod(vec2)
    return s

try:
    users = ast.literal_eval(args1)
    rating_matrix = np.array( ast.literal_eval(args2) )

    # 計算樣本兩兩間的相似度
    cos_sims = cosine_similarity(rating_matrix)
    sims_df = pd.DataFrame(cos_sims, columns = users, index = users)
    print(sims_df)
except Exception as e:
    print(e)