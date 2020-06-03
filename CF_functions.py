# -*- coding: utf-8 -*-

"""
    get_matrix用来整合数据，构建user-item评价矩阵，并将得到的矩阵进行输出
    get_similarity用来求解用户之间的余弦相似度，并以矩阵形式返回
    get_recommender基于用户间的相似性，构建推荐矩阵，其中元素（i，j）为用户i对歌曲j的预测评分
    recommend用来给输入的用户推荐K首歌曲
"""

import numpy as np
import math

def get_matrix(user_list,item_list,recent_listen_dict,list_music_dict):
    n = len(user_list)
    m = len(item_list)
    #行向量为某用户对所有歌曲评价，列向量为某歌曲收到所有用户的评价
    user_item_matrix = np.zeros((n,m))   
    #若该音乐最近被该用户听过，则将该用户对该音乐的评价设置为5
    #若该音乐被该用户收藏，则将该用户对该音乐的评价再加2
    for user in user_list:
        items1 = recent_listen_dict[user]
        items2 = list_music_dict[user]
        for item in items1:
            user_item_matrix[user_list.index(user)][item_list.index(item)] = 5
        for item in items2:
            user_item_matrix[user_list.index(user)][item_list.index(item)] += 2
    return user_item_matrix


def get_similarity(user_item_martix):
    n = len(user_item_martix)
    user_similarity_matrix = np.zeros((n,n))
    #显然该矩阵一定为对称矩阵，我们只需算一半，来降低计算复杂度。且计算时不考虑自身与自身相似度
    for i in range(n):
        for j in range(i + 1,n):
            x = user_item_martix[i]
            y = user_item_martix[j].T
            user_similarity_matrix[i][j] = np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))
    user_similarity_matrix +=  user_similarity_matrix.T
    return  user_similarity_matrix
 

def get_recommender(user_item_martix,user_similarity_matrix,K):
    R = user_item_martix #'Rank'矩阵，用户与项目之间的评价
    S = user_similarity_matrix #'Similarity'矩阵，用户间的相似性度量
    n = len(user_item_martix)
    m = len(user_item_martix.T)
    Recommender = np.zeros((n,m))
    for i in range(n):
        a = user_similarity_matrix[i]
        b = sorted(enumerate(a), key=lambda x:x[1],reverse = True)[:K]
        index_list = [b[m][0] for m in range(len(b))]
        temp = np.zeros((1,m))
        for j in range(K):
            temp = S[i][index_list[j]]*R[index_list[j]]
        one_norm = math.sqrt(sum([S[i][index_list[k]] for k in range(K)]))
        Recommender[i] = temp/one_norm
    return Recommender


def recommend(user_id,user_list,item_list_dict,Recommender,K):
    item_list = list(item_list_dict)
    user_index = user_list.index(user_id)
    a = Recommender[user_index]
    b = sorted(enumerate(a), key=lambda x:x[1],reverse = True)[:K]
    index_list = [b[m][0] for m in range(len(b))]
    print('推荐给用户%d的前%d首歌曲为：' %(user_id,K))
    for j in range(K):
        print('%d:%s' %(j + 1,item_list_dict[item_list[index_list[j]]]))














