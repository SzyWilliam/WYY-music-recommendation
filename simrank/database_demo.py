#!/usr/bin/env python
# coding: utf-8

# # Data Base Demo
# 
# 以类封装数据库操作，具体用法见HTML的Part 2中各个类函数的详细说明。

import sqlite3
# 自定义的函数，代码文件位于同目录下
import create_db


# 将数据库抽象为一个类，方便读写调用
class db_cls():

    # 初始化数据库，如果当前目录下不存在，则创建一个
    def __init__(self, db_filename):
        create_db.create_db(db_filename)
        self.db_connection = sqlite3.connect(db_filename)
        self.db_cursor = self.db_connection.cursor()

    # 写入歌曲播放页爬取到的数据
    def write_Song_infos(self, song_infos_list, song2singer_list):
        # 检查是否歌曲id已存在
        exist_songs = set([song[0] for song in self.db_cursor.execute("SELECT id FROM Song")])
        input_songs = set([song[0] for song in song_infos_list])
        new_songs = input_songs - exist_songs

        # 歌曲9项基本信息
        self.db_cursor.executemany('INSERT OR IGNORE INTO Song VALUES (?,?,?,?,?,?,?,?,?)',
                                   [song for song in song_infos_list if song[0] in new_songs])
        # 歌曲与歌手的多对多关系
        self.db_cursor.executemany('INSERT INTO Song2Singer VALUES (?,?)',
                                   list(set([song for song in song2singer_list if song[0] in new_songs])))
        # 提交插入更改请求
        self.db_connection.commit()

    # 写入专辑信息
    def write_Album_info(self, albums_list):
        # 检查是否专辑id已存在
        exist_albums = set([album[0] for album in self.db_cursor.execute("SELECT id FROM Album")])
        input_albums = set([album[0] for album in albums_list])
        new_albums = input_albums - exist_albums

        # 专辑id及其名字
        self.db_cursor.executemany('INSERT OR IGNORE INTO Album VALUES (?,?)',
                                   [album for album in albums_list if album[0] in new_albums])
        # 提交插入更改请求
        self.db_connection.commit()

    # 写入歌手信息
    def write_Singer_info(self, singers_list):
        # 检查是否歌手id已存在
        exist_singers = set([singer[0] for singer in self.db_cursor.execute("SELECT id FROM Singer")])
        input_singers = set([singer[0] for singer in singers_list])
        new_singers = input_singers - exist_singers

        # 专辑id及其名字
        self.db_cursor.executemany('INSERT OR IGNORE INTO Singer VALUES (?,?)',
                                   [singer for singer in singers_list if singer[0] in new_singers])
        # 提交插入更改请求
        self.db_connection.commit()

    # 写入歌单页爬取到的数据
    def write_SongList_infos(self, songlist_infos_list, songlist2tag_list, songlist2song_list):
        # 检查是否歌单id已存在
        exist_songlists = set([songlist[0] for songlist in self.db_cursor.execute("SELECT id FROM SongList")])
        input_songlists = set([songlist[0] for songlist in songlist_infos_list])
        new_songlists = input_songlists - exist_songlists

        # 歌单7项基本信息
        self.db_cursor.executemany('INSERT OR IGNORE INTO SongList VALUES (?,?,?,?,?,?,?)',
                                   [songlist for songlist in songlist_infos_list if songlist[0] in new_songlists])
        # 歌单与歌单标签的多对多关系
        self.db_cursor.executemany('INSERT INTO SongList2Tag VALUES (?,?)', list(
            set([songlist for songlist in songlist2tag_list if songlist[0] in new_songlists])))
        # 歌单与歌曲的多对多关系
        self.db_cursor.executemany('INSERT INTO SongList2Song VALUES (?,?)', list(
            set([songlist for songlist in songlist2song_list if songlist[0] in new_songlists])))
        # 提交插入更改请求
        self.db_connection.commit()

    # 写入歌单标签信息
    def write_Tag_info(self, tags_list):
        # 检查是否标签id已存在
        exist_tags = set([tag[0] for tag in self.db_cursor.execute("SELECT id FROM Tag")])
        input_tags = set([tag[0] for tag in tags_list])
        new_tags = input_tags - exist_tags

        # 歌单标签id及其名字
        self.db_cursor.executemany('INSERT OR IGNORE INTO Tag VALUES (?,?)',
                                   [tag for tag in tags_list if tag[0] in new_tags])
        # 提交插入更改请求
        self.db_connection.commit()

    # 写入用户页爬取到的数据
    def write_User_infos(self, user_infos_list, user2song_list, user2songlist_list, follow_list):
        # 检查是否用户id已存在
        exist_users = set([user[0] for user in self.db_cursor.execute("SELECT id FROM User_Table")])
        input_users = set([user[0] for user in user_infos_list])
        new_users = input_users - exist_users

        # 用户3项基本信息
        self.db_cursor.executemany('INSERT OR IGNORE INTO User_Table VALUES (?,?,?)',
                                   [user for user in user_infos_list if user[0] in new_users])
        # 用户与歌曲的多对多关系（最近听的歌）
        self.db_cursor.executemany('INSERT INTO User2Song VALUES (?,?)',
                                   list(set([user for user in user2song_list if user[0] in new_users])))
        # 用户与歌单的多对多关系（用户收藏的歌单）
        self.db_cursor.executemany('INSERT INTO User2SongList VALUES (?,?)',
                                   list(set([user for user in user2songlist_list if user[0] in new_users])))
        # 用户之间的多对多关系（关注or被关注）
        self.db_cursor.executemany('INSERT INTO Follow VALUES (?,?)',
                                   list(set([user for user in follow_list if user[0] in new_users])))
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
        return list(self.db_cursor.execute("SELECT " + result_col + " FROM Song WHERE " + requirement))

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
