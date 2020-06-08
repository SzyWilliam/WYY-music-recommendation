from database_demo import db_cls

# 歌曲与用户二元关系，读入歌曲
def song2user_load_songs(db):
    song_ids = set([each[0] for each in db.read_Data(sql_query="Select song_id from User2Song")])
    song_id2pos = {}    # 歌曲id到其矩阵位置的映射字典
    song_pos2id = {}    # 歌曲矩阵位置到其id的映射字典
    current_pos = 0     # 当前矩阵位置
    for song_id in song_ids:
        song_id2pos[song_id] = current_pos
        song_pos2id[current_pos] = song_id
        current_pos += 1

    # 返回歌曲的矩阵位置与其id的对应关系字典，以及歌曲数目
    return song_pos2id, song_id2pos, current_pos


# 歌曲与用户二元关系，读入用户
def song2user_load_users(db):
    user_ids = set([each[0] for each in db.read_Data(sql_query="Select user_id from User2Song")])
    user_id2pos = {}    # 用户id到其矩阵位置的映射字典
    user_pos2id = {}    # 用户矩阵位置到其id的映射字典
    current_pos = 0     # 当前矩阵位置
    for user_id in user_ids:
        user_id2pos[user_id] = current_pos
        user_pos2id[current_pos] = user_id
        current_pos += 1

    # 返回用户的矩阵位置与其id的对应关系字典，以及歌曲数目
    return user_pos2id, user_id2pos, current_pos


# 构建只有用户-歌曲的关系邻接表
def user_song_relation(db_filename):

    # 载入数据库
    db = db_cls(db_filename)
    # 第一次使用可创建索引，加快数据库查询速度
    # db.create_index()

    # 分别载入歌曲与用户的数据
    song_pos2id, song_id2pos, song_num = song2user_load_songs(db)
    user_pos2id, user_id2pos, user_num = song2user_load_users(db)

    # 构建歌曲-用户关系邻接表
    R_song = [[] for i in range(song_num)]
    R_user = [[] for i in range(user_num)]
    song_user_relation = db.read_Data(sql_query="Select * from User2Song")
    for user_id, song_id in song_user_relation:
        user_pos = user_id2pos[user_id]
        song_pos = song_id2pos[song_id]
        R_song[song_pos].append(user_pos)
        R_user[user_pos].append(song_pos)

    db.close_db()
    return song_pos2id, song_id2pos, song_num, user_pos2id, user_id2pos, user_num, R_song, R_user
