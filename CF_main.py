# -*- coding: utf-8 -*-
"""
    基于用户的协同过滤算法
"""
from database_demo import db_cls
import CF_functions as cf

def main():
    #从数据库中读取所需信息,并做格式化预处理
    db = db_cls(db_filename="pj_data.db")
    user_list = db.read_Data(sql_query="Select id FROM User_Table")
    user_list = [ite[0] for ite in user_list]
    #item_list_dict = dict(db.read_Data(sql_query="Select id,song_name FROM Song"))
    #item_list = list(item_list_dict)
    item_list1 = db.read_Data(sql_query="Select song_id FROM User2Song")
    item_list2 = db.read_Data(sql_query="Select song_id FROM SongList2Song")
    item_list = list(set(item_list1 + item_list2))
    item_list = [ite[0] for ite in item_list]
    user_list = sorted(user_list)
    item_list = sorted(item_list)
    item_list_dict = dict(db.read_Data(sql_query="Select id,song_name FROM Song"))
    for item in item_list:
        item_list_dict[item] = item_list_dict.get(item,"歌名未知")
    #创建“最近听歌”字典,key为user_id,value为该用户最近听歌的歌曲id组成的列表
    recent_listen = db.read_Data(sql_query="Select * FROM User2Song")
    recent_listen_dict = dict()
    for it in recent_listen:
        recent_listen_dict[it[0]] = recent_listen_dict.get(it[0],[]) + [it[1]]
    for it in user_list:
        recent_listen_dict[it] = recent_listen_dict.get(it,[])
    #创建“歌单音乐”字典,key为user_id,value为该用户收藏歌单中歌曲id组成的列表
    list_music = db.read_Data(sql_query="Select a.user_id,b.song_id \
                                         FROM User2SongList a INNER JOIN SongList2Song b\
                                         ON a.songlist_id = b.songlist_id")
    list_music_dict = dict()
    for it in list_music:
        list_music_dict[it[0]] = list_music_dict.get(it[0],[]) + [it[1]]
    for it in user_list:
        list_music_dict[it] = list_music_dict.get(it,[])
        
    
    #获取用户-音乐评价矩阵
    user_item_matrix = cf.get_matrix(user_list,item_list,recent_listen_dict,list_music_dict)
    
    #获取用户相似度矩阵
    user_similarity_matrix = cf.get_similarity(user_item_matrix)
    
    #获取基于用户相似性得到的推荐矩阵
    Recommender = cf.get_recommender(user_item_matrix, user_similarity_matrix, 5)
    
    #为id为393718733的用户推荐5首歌曲
    #cf.recommend(393718733, user_list, item_list_dict, Recommender, 20)
    cf.recommend(2141581764, user_list, item_list_dict, Recommender, 10)

if __name__ == '__main__':
    main()
    
