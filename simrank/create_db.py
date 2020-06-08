import sqlite3

def create_db(db_filename):

   db_connection = sqlite3.connect(db_filename)
   db_cursor = db_connection.cursor()

   # create song table
   db_cursor.execute("CREATE TABLE IF NOT EXISTS                                 \
                      Song       (  id                INTEGER     PRIMARY KEY,   \
                                    song_name         TEXT,                      \
                                    album_id          INTEGER,                   \
                                    comments_num      MEDIUMINT,                 \
                                    similar_songid1   INTEGER,                   \
                                    similar_songid2   INTEGER,                   \
                                    similar_songid3   INTEGER,                   \
                                    similar_songid4   INTEGER,                   \
                                    similar_songid5   INTEGER                    )")

   # create song list table
   db_cursor.execute("CREATE TABLE IF NOT EXISTS                                 \
                      SongList   (  id                INTEGER     PRIMARY KEY,   \
                                    songlist_name	  TEXT,                      \
                                    user_id	          INTEGER,                   \
                                    play_num    	  INTEGER,                   \
                                    fav_num	          INTEGER,                   \
                                    share_num	      INTEGER,                   \
                                    comments_num	  MEDIUMINT                  )")

   # create user table
   db_cursor.execute("CREATE TABLE IF NOT EXISTS                                 \
                      User_Table (  id                INTEGER     PRIMARY KEY,   \
                                    lv                TINYINT,                   \
                                    gender            TINYINT                    )")

   # create song to singer table
   db_cursor.execute("CREATE TABLE IF NOT EXISTS                                 \
                      Song2Singer(  song_id           INTEGER,                   \
                                    singer_id	      INTEGER                    )")

   # create song to song list table
   db_cursor.execute("CREATE TABLE IF NOT EXISTS                                 \
                      SongList2Song(   songlist_id    INTEGER,                   \
                                       song_id	      INTEGER                    )")

   # create song list to tag table
   db_cursor.execute("CREATE TABLE IF NOT EXISTS                                 \
                      SongList2Tag(    songlist_id    INTEGER,                   \
                                       tag_id 	      INTEGER                    )")

   # create user to song table
   db_cursor.execute("CREATE TABLE IF NOT EXISTS                                 \
                      User2Song  (  user_id           INTEGER,                   \
                                    song_id 	      INTEGER                    )")

   # create user to song list table
   db_cursor.execute("CREATE TABLE IF NOT EXISTS                                 \
                      User2SongList(   user_id        INTEGER,                   \
                                       songlist_id 	  INTEGER                    )")

   # create follow table
   db_cursor.execute("CREATE TABLE IF NOT EXISTS                                 \
                      Follow  (     user_id           INTEGER,                   \
                                    follow_id	      INTEGER                    )")

   # create album table
   db_cursor.execute("CREATE TABLE IF NOT EXISTS                                 \
                      Album   (     id                INTEGER     PRIMARY KEY,   \
                                    album_name        TEXT                       )")

   # create singer table
   db_cursor.execute("CREATE TABLE IF NOT EXISTS                                 \
                      Singer  (     id                INTEGER     PRIMARY KEY,   \
                                    singer_name       TEXT                       )")

   # create tag table
   db_cursor.execute("CREATE TABLE IF NOT EXISTS                                 \
                      Tag     (     id                INTEGER     PRIMARY KEY,   \
                                    tag_name          TEXT                       )")

   # 最后务必关闭数据库，否则可能有些更改并不会保存至硬盘
   db_connection.close()
