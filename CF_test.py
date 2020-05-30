# -*- coding: utf-8 -*-
"""
用来测试涉及函数的正确性
"""
import numpy as np
import CF_functions as f

def main():
    user_list = [3,8,7,5]
    item_list = [46,34,54]
    user_list = sorted(user_list)
    item_list = sorted(item_list)
    user_item_matrix = np.matrix([[3,0,3],[5,4,0],[1,2,4],[2,2,0]])
    user_similarity_matrix = f.get_similarity(user_item_matrix)
    print('用户相似性矩阵如下：')
    print(user_similarity_matrix)
    Recommender = f.get_recommender(user_item_matrix, user_similarity_matrix, 2)
    print('根据相似性得到的推荐矩阵如下：')
    print(Recommender)
    f.recommend(5, user_list, item_list, Recommender, 2)
    
    
if __name__ == '__main__':
    main()
