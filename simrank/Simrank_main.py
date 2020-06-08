from database_demo import db_cls
from Simrank_readin import user_song_relation
from tqdm import tqdm as tqdm
import numpy as np
import heapq

# 数据库文件
db_filename = "pj_data.db"

# decay factor of Simrank
c = 0.8

# 迭代次数
iter_num = 20

# 作为样本的歌曲，用于观察迭代后得到的相似歌曲结果
sample_songs = [29947420, 461347998, 31356499, 1313354324, 436514312, 483671599]    # 用于我们自己爬的数据
#sample_songs = [139764, 144619, 408055928, 180280]    # 用于老师给的数据


if __name__ == "__main__":
    # 从数据库中载入数据
    song_pos2id, song_id2pos, song_num, user_pos2id, user_id2pos, user_num, R_song, R_user = user_song_relation(db_filename)
    db = db_cls(db_filename)

    # 分别构建歌曲及用户相似度矩阵，初始为单位阵
    S_song = np.eye(song_num)
    S_user = np.eye(user_num)

    # Simrank 迭代
    for iter in range(iter_num):
        print("Iteration: " + str(iter+1))

        # 遍历歌曲相似矩阵，通过用户相似度来计算歌曲相似度
        for x in tqdm(range(song_num), unit='rows'):
            for y in range(song_num):
                if x<y:
                    S_val = 0
                    # 分别连接歌曲x和y的用户列表
                    x_in = R_song[x]
                    y_in = R_song[y]
                    # 两两比较列表中的用户，累加用户相似度
                    for i in x_in:
                        for j in y_in:
                            S_val += S_user[i,j]
                    # 写入歌曲x和y的最终相似度
                    if len(x_in)*len(y_in)>0:
                        S_val *= c/(len(x_in)*len(y_in))
                    S_song[x,y] = S_val
                    S_song[y,x] = S_val

        # 遍历用户相似矩阵，通过用户相似度来计算歌曲相似度
        for x in tqdm(range(user_num), unit='rows'):
            for y in range(user_num):
                if x < y:
                    S_val = 0
                    # 分别连接用户x和y的歌曲列表
                    x_in = R_user[x]
                    y_in = R_user[y]
                    # 两两比较列表中的歌曲，累加歌曲相似度
                    for i in x_in:
                        for j in y_in:
                            S_val += S_song[i, j]
                    # 写入用户x和y的最终相似度
                    if len(x_in) * len(y_in) > 0:
                        S_val *= c / (len(x_in) * len(y_in))
                    S_user[x, y] = S_val
                    S_user[y, x] = S_val

        # 通过样本歌曲观察本次迭代后得到的相似歌曲结果
        print("本次迭代后相似歌曲：")
        for song_id in sample_songs:
            # 对样本歌曲读取其歌名
            x = song_id2pos[song_id]
            x_name = db.read_Data(sql_query="SELECT song_name FROM Song WHERE id=" + str(song_id))[0][0]
            # 保存所有歌曲与该歌曲的相似度
            song_Sim = []
            for y in range(song_num):
                if x != y:
                    song_Sim.append((song_pos2id[y], S_song[x, y]))
            # 选出相似度最高的5首歌曲
            Top_Sim = heapq.nlargest(5, song_Sim, key=lambda x: x[1])
            Top_Sim = [(each[0],
                        db.read_Data(sql_query="SELECT song_name FROM Song WHERE id=" + str(each[0])))
                       for each in Top_Sim]
            # 打印结果
            print(x_name, ':')
            for song in Top_Sim:
                print("\t", song)

    db.close_db()

