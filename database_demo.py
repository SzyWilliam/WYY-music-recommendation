#!/usr/bin/env python
# coding: utf-8

# # Data Base Demo
# 
# 以类封装数据库操作，具体用法见Part 2各个类函数的详细说明。

# In[363]:


import sqlite3
# 自定义的函数，代码文件位于同目录下
import create_db


# ## Part 1 Class Definition
# 
# 抽象类的定义，可以略过，如何调用类函数在Part 2中。

# In[364]:


# 将数据库抽象为一个类，方便读写调用
class db_cls():

    # 初始化数据库，如果当前目录下不存在，则创建一个
    def __init__(self,db_filename):
        create_db.create_db(db_filename)
        self.db_connection = sqlite3.connect(db_filename)
        self.db_cursor = self.db_connection.cursor()

    # 写入歌曲播放页爬取到的数据
    def write_Song_infos(self, song_infos_list, song2singer_list):
        # 歌曲9项基本信息
        self.db_cursor.executemany('INSERT INTO Song VALUES (?,?,?,?,?,?,?,?,?)', song_infos_list)
        # 歌曲与歌手的多对多关系
        self.db_cursor.executemany('INSERT INTO Song2Singer VALUES (?,?)', song2singer_list)
        # 提交插入更改请求
        self.db_connection.commit()
        
    # 写入专辑信息
    def write_Album_info(self, albums_list):
        # 专辑id及其名字
        self.db_cursor.executemany('INSERT INTO Album VALUES (?,?)', albums_list)
        # 提交插入更改请求
        self.db_connection.commit()
        
    # 写入歌手信息
    def write_Singer_info(self, singers_list):
        # 专辑id及其名字
        self.db_cursor.executemany('INSERT INTO Singer VALUES (?,?)', singers_list)
        # 提交插入更改请求
        self.db_connection.commit()
        
    # 写入歌单页爬取到的数据
    def write_SongList_infos(self, songlist_infos_list, songlist2tag_list, songlist2song_list):
        # 歌单7项基本信息
        self.db_cursor.executemany('INSERT INTO SongList VALUES (?,?,?,?,?,?,?)', songlist_infos_list)
        # 歌单与歌单标签的多对多关系
        self.db_cursor.executemany('INSERT INTO SongList2Tag VALUES (?,?)', songlist2tag_list)
        # 歌单与歌曲的多对多关系
        self.db_cursor.executemany('INSERT INTO SongList2Song VALUES (?,?)', songlist2song_list)
        # 提交插入更改请求
        self.db_connection.commit()
        
    # 写入歌单标签信息
    def write_Tag_info(self, tags_list):
        # 歌单标签id及其名字
        self.db_cursor.executemany('INSERT INTO Tag VALUES (?,?)', tags_list)
        # 提交插入更改请求
        self.db_connection.commit()

    # 写入用户页爬取到的数据
    def write_User_infos(self, user_infos_list, user2song_list, user2songlist_list, follow_list):
        # 用户3项基本信息
        self.db_cursor.executemany('INSERT INTO User_Table VALUES (?,?,?)', user_infos_list)
        # 用户与歌曲的多对多关系（最近听的歌）
        self.db_cursor.executemany('INSERT INTO User2Song VALUES (?,?)', user2song_list)
        # 用户与歌单的多对多关系（用户收藏的歌单）
        self.db_cursor.executemany('INSERT INTO User2SongList VALUES (?,?)', user2songlist_list)
        # 用户之间的多对多关系（关注or被关注）
        self.db_cursor.executemany('INSERT INTO Follow VALUES (?,?)', follow_list)
        # 提交插入更改请求
        self.db_connection.commit()
    
    # 对每个表创建索引以提升查询速度
    def create_index(self):
        self.db_cursor.execute('CREATE INDEX Song2Singer_idx1 ON Song2Singer(song_id)')
        self.db_cursor.execute('CREATE INDEX Song2Singer_idx2 on Song2Singer(singer_id)')
        self.db_cursor.execute('CREATE INDEX SongList2Song_idx1 on SongList2Song(song_id)')
        self.db_cursor.execute('CREATE INDEX SongList2Song_idx2 on SongList2Song(songlist_id)')
        self.db_cursor.execute('CREATE INDEX SongList2Tag_idx1 on SongList2Tag(tag_id)')
        self.db_cursor.execute('CREATE INDEX SongList2Tag_idx2 on SongList2Tag(songlist_id)')
        self.db_cursor.execute('CREATE INDEX User2Song_idx1 on User2Song(song_id)')
        self.db_cursor.execute('CREATE INDEX User2Song_idx2 on User2Song(user_id)')
        self.db_cursor.execute('CREATE INDEX User2SongList_idx1 on User2SongList(user_id)')
        self.db_cursor.execute('CREATE INDEX User2SongList_idx2 on User2SongList(songlist_id)')
        self.db_cursor.execute('CREATE INDEX Follow_idx1 on Follow(user_id)')
        self.db_cursor.execute('CREATE INDEX Follow_idx2 on Follow(follow_id)')
        # 提交更改请求
        self.db_connection.commit()        
    
    # 读取符合要求的歌曲的具体列信息
    def read_Song_infos(self, requirement, result_col):
        return list(self.db_cursor.execute("SELECT "+result_col+" FROM Song WHERE "+requirement))

    # 通用数据库查询操作
    def read_Data(self, sql_query):
        return list(self.db_cursor.execute(sql_query))

    # 删除某个表中所有记录
    def delete_table(self, table_name):
        self.db_cursor.execute("DELETE FROM " + table_name)
        # 提交删除更改请求
        self.db_connection.commit()
        
    # 删除所有索引
    def drop_index(self):
        self.db_cursor.execute("DROP INDEX  Song2Singer_idx1    ")
        self.db_cursor.execute("DROP INDEX  Song2Singer_idx2    ")
        self.db_cursor.execute("DROP INDEX  SongList2Song_idx1  ")
        self.db_cursor.execute("DROP INDEX  SongList2Song_idx2  ")
        self.db_cursor.execute("DROP INDEX  SongList2Tag_idx1   ")
        self.db_cursor.execute("DROP INDEX  SongList2Tag_idx2   ")
        self.db_cursor.execute("DROP INDEX  User2Song_idx1      ")
        self.db_cursor.execute("DROP INDEX  User2Song_idx2      ")
        self.db_cursor.execute("DROP INDEX  User2SongList_idx1  ")
        self.db_cursor.execute("DROP INDEX  User2SongList_idx2  ")
        self.db_cursor.execute("DROP INDEX  Follow_idx1         ")
        self.db_cursor.execute("DROP INDEX  Follow_idx2         ")
        # 提交更改请求
        self.db_connection.commit()

    # 关闭数据库，否则可能没有保存信息
    def close_db(self):
        self.db_connection.close()


# ## Part 2 Usage
# 
# 如何写入/读取数据库信息。

# ### 1、初始化载入数据库文件
# 
# 如果当前目录下不存在该数据库文件，则自动创建一个

# In[365]:


db = db_cls(db_filename="pj_data.db")


# ### 2、歌曲播放页爬取的数据写入数据库
# 
# #### （1）db.write_Song_infos(song_infos_list, song2singer_list)函数用法
# 
# - song_infos_list是一个列表，列表里的每一个元组代指一首歌的信息。
# 一首歌的元组由下列9个变量按顺序组成：

# In[366]:


# id：            歌曲url截取出来的，必须转为整数形式输入，最大21亿
# song_name：     歌名
# album_id：      专辑url截取出来的，必须转为整数形式输入，最大21亿
# comments_num：  歌曲评论数量，整数形式，最大800w
# similar_songid1, similar_songid2, similar_songid3, similar_songid4, similar_songid5:   5首相似歌曲的id，通过各自的url截取出来，整数形式，最大21亿
# 
# 比如一首歌的元组可以是     (1,"test song name",1,1000,2,3,4,5,6)
# 而song_infos_list可以是   [ (1,"test song name1",1,1000,2,3,4,5,6), (2,"test song name2",4,10000,1,3,4,5,6) ]，包含了两首不同的歌


# - song2singer_list也是一个列表，列表里每个元组代表一对（歌曲，歌手）关系。

# In[367]:


# 比如一个元组是（1,3），指的是id为1的歌曲，其歌手的id是3
# 一首歌可能有多个歌手，所以song2singer_list可能是 [(1,1),(1,3),(2,1)]


# - db.write_Song_infos(song_infos_list, song2singer_list)调用注意事项
# 
# 为了提高数据库写入性能，建议同时写入多首歌信息（比如每爬取100首写入一次）
# 
# ！ 注意：请务必保证将写入的歌曲信息不在数据库里，否则会报错 ！
# 
# 建议通过集合，先判断每个歌曲id是否之前已经执行写入数据库的命令，
# 如果都没被写入过，再调用下方函数。

# In[368]:


# 同时写入2首歌曲信息
db.write_Song_infos(    song_infos_list=[(1,"test song name1",1,1000,2,3,4,5,6),
                                     (2,"test song name2",4,10000,1,3,4,5,6)],
                        song2singer_list=[(1,1),(1,3),(2,1)]                         )


# #### (2)db.write_Album_infos(albums_list)函数用法
# 
# - albums_list也是一个列表，列表里每个元组代表一对（专辑id，专辑名称）关系。
# 
# - 调用注意事项
# 
# 为了提高数据库写入性能，建议同时写入多个专辑信息
# 
# ！ 注意：请务必保证将写入的专辑信息不在数据库里，否则会报错 ！
# 
# 建议通过集合，先判断每个专辑id是否之前已经执行写入数据库的命令，
# 如果都没被写入过，再调用下方函数。

# In[369]:


# 比如一个元组是（1,"album name 1"），指的是id为1的专辑名称是"album name 1"
# albums_list可能是 [(1,"album name 1"),(2,"album name 2")]
db.write_Album_info(albums_list=[(1,"album name 1"),(2,"album name 2")])


# #### (3)db.write_Singer_infos(singers_list)函数用法
# 
# - singers_list也是一个列表，列表里每个元组代表一对（歌手id，歌手名称）关系。
# 
# - 调用注意事项
# 
# 为了提高数据库写入性能，建议同时写入多个歌手信息
# 
# ！ 注意：请务必保证将写入的歌手信息不在数据库里，否则会报错 ！
# 
# 建议通过集合，先判断每个歌手id是否之前已经执行写入数据库的命令，
# 如果都没被写入过，再调用下方函数。

# In[370]:


# 比如一个元组是（1,"singer name 1"），指的是id为1的专辑名称是"singer name 1"
# singers_list可能是 [(1,"singer name 1"),(2,"singer name 2")]
db.write_Singer_info(singers_list=[(1,"singer name 1"),(2,"singer name 2")])


# ### 3、歌单页爬取的数据写入数据库
# 
# #### （1）db.write_SongList_infos(songlist_infos_list, songlist2tag_list, songlist2song_list)函数用法
# 
# - songlist_infos_list是一个列表，列表里的每一个元组代指一个歌单的信息。
# 一个歌单的元组由下列7个变量按顺序组成：

# In[371]:


# id：               歌单url截取出来的，必须转为整数形式输入，最大支持21亿的数字
# songlist_name：    歌单名
# userid：           创建者id
# play_num：         播放数，整数形式，最大21亿
# fav_num：          收藏数，整数形式，最大21亿
# share_num：        转发数，整数形式，最大21亿
# comments_num：     歌曲评论数量，整数形式，最大800w
# 
# 比如一个歌单的元组可以是     (1,"songlist name 1",1,10000,100,10,1000)
# 而songlist_infos_list可以是   [ (1,"songlist name 1",1,10000,100,10,1000), (2,"songlist name 2",1,1000,10,1,100) ]，包含了两个不同的歌单


# - songlist2tag_list也是一个列表，列表里每个元组代表一对（歌单，歌单标签）关系。

# In[372]:


# 比如一个元组是（1,3），指的是id为1的歌单，它的一个歌单标签的id是3
# 一个歌单可能有多个歌单标签，所以songlist2tag_list可能是 [(1,1),(1,3),(2,1)]


# - songlist2song_list也是一个列表，列表里每个元组代表一对（歌单，歌曲）关系。

# In[373]:


# 比如一个元组是（1,3），指的是id为1的歌单，其中的一首歌id是3
# 一个歌单可能有多首歌曲，所以songlist2song_list可能是 [(1,1),(1,3),(2,1)]


# - db.write_SongList_infos(songlist_infos_list, songlist2tag_list, songlist2song_list)调用注意事项
# 
# 为了提高数据库写入性能，建议同时写入多个歌单信息
# 
# ！ 注意：请务必保证将写入的歌单信息不在数据库里，否则会报错 ！
# 
# 建议通过集合，先判断每个歌单id是否之前已经执行写入数据库的命令，
# 如果都没被写入过，再调用下方函数。

# In[374]:


# 同时写入2个歌单信息
db.write_SongList_infos(    songlist_infos_list=[ (1,"songlist name 1",1,10000,100,10,1000), 
                                                  (2,"songlist name 2",1,1000,10,1,100) ],
                            songlist2tag_list=[(1,1),(1,3),(2,1)],
                            songlist2song_list=[(1,1),(1,3),(2,1)])


# #### (2)db.write_Tag_infos(tags_list)函数用法
# 
# - tags_list也是一个列表，列表里每个元组代表一对（歌单标签id，标签名称）关系。
# 
# - 调用注意事项
# 
# 为了提高数据库写入性能，建议同时写入多个标签信息
# 
# ！ 注意：请务必保证将写入的标签信息不在数据库里，否则会报错 ！
# 
# 建议通过集合，先判断每个标签id是否之前已经执行写入数据库的命令，
# 如果都没被写入过，再调用下方函数。

# In[375]:


# 比如一个元组是（1,"tag name 1"），指的是id为1的标签名称是"tag name 1"
# tags_list可能是 [(1,"tag name 1"),(2,"tag name 2")]
db.write_Tag_info(tags_list=[(1,"tag name 1"),(2,"tag name 2")])


# ### 4、用户页爬取的数据写入数据库
# 
# #### （1）db.write_User_infos(user_infos_list, user2song_list, user2songlist_list, follow_list)函数用法
# 
# - user_infos_list是一个列表，列表里的每一个元组代指一个用户的信息。
# 一个用户的元组由下列3个变量按顺序组成：

# In[376]:


# id：       用户url截取出来的，必须转为整数形式输入，最大支持21亿的数字
# lv：       用户等级，0-10整数者id
# gender：   用户性别（0未知，1男，2女） 
# 
# 比如一个用户的元组可以是     (1,1,1)
# 而user_infos_list可以是   [ (1,1,1), (2,10,2) ]，包含了两个不同的用户


# - user2song_list也是一个列表，列表里每个元组代表一对（用户，歌曲）关系。

# In[377]:


# 比如一个元组是（1,3），指的是id为1的用户，TA最近听过的一首歌id是3
# 一个用户可能有多首最近听过的歌曲，所以user2song_list可能是 [(1,1),(1,3),(2,1)]


# - user2songlist_list也是一个列表，列表里每个元组代表一对（用户，歌单）关系。

# In[378]:


# 比如一个元组是（1,3），指的是id为1的用户，TA收藏的一个歌单id是3
# 一个用户可能有多个收藏的歌单，所以user2songlist_list可能是 [(1,1),(1,3),(2,1)]


# - follow_list也是一个列表，列表里每个元组代表一对（A，B）关系，表示A关注了B。
# 注意：此处只需爬取每个用户的关注列表，不需要其粉丝列表，就能得到关注与被关注关系！

# In[379]:


# 比如一个元组是（1,3），指的是id为1的用户关注了id为3的用户
# 一个用户可能关注了多个用户，所以follow_list可能是 [(1,1),(1,3),(2,1)]


# - db.write_User_infos(user_infos_list, user2song_list, user2songlist_list, follow_list)调用注意事项
# 
# 为了提高数据库写入性能，建议同时写入多个用户信息
# 
# ！ 注意：请务必保证将写入的用户信息不在数据库里，否则会报错 ！
# 
# 建议通过集合，先判断每个用户id是否之前已经执行写入数据库的命令，
# 如果都没被写入过，再调用下方函数。

# In[380]:


# 同时写入2个用户信息
db.write_User_infos(    user_infos_list=[ (1,1,1), (2,10,2) ],
                        user2song_list=[(1,1),(1,3),(2,1)],
                        user2songlist_list=[(1,1),(1,3),(2,1)],
                        follow_list=[(1,1),(1,3),(2,1)])


# ### 5、所有写入完成后请执行db.create_index()函数
# 创建索引，以加速查询操作
# 
# ！注意，如果之后仍有大量写入操作，请不要创建索引，
# 必须是所有数据爬取完成后，再创建索引以提高读取速度

# In[381]:


db.create_index()


# ### 6、通用读取数据函数db.read_Data(sql_query)
# 可以自定义任何读取请求，以列表形式返回所有符合要求的记录

# In[382]:


print(db.read_Data(sql_query="Select * FROM SongList"))


# ### 7、读取歌曲基础信息read_Song_infos(requirement, result_col)（示例，可以根据到时候模型的要求，写任何查询函数）
# 
# - requirement是筛选数据的要求，如requirement="id>0"即是返回id为正的歌曲信息列表
# - result_col是需要返回的列名，如result_col=“*”即返回所有列信息的元组

# In[383]:


# 读取id为1的歌曲名字与评论数
print(db.read_Song_infos(requirement="id=1",result_col="song_name,comments_num"))


# ### 8、删除表delete_table(table_name)函数用法
# 
# - table_name是想要清空数据的表名

# In[384]:


# 此处只是想把刚刚样例函数写入过的所有记录清除掉。
db.delete_table(table_name="Song")
db.delete_table(table_name="SongList")
db.delete_table(table_name="User_Table")
db.delete_table(table_name="Song2Singer")
db.delete_table(table_name="SongList2Song")
db.delete_table(table_name="SongList2Tag")
db.delete_table(table_name="User2Song")
db.delete_table(table_name="User2SongList")
db.delete_table(table_name="Follow")
db.delete_table(table_name="Album")
db.delete_table(table_name="Singer")
db.delete_table(table_name="Tag")

# 此处想把刚刚创建的索引删掉，实际应用中不用删哈
db.drop_index()


# ### 9、关闭数据库
# 最后务必关闭数据库，否则可能有些更改并不会保存至硬盘

# In[385]:


db.close_db()

