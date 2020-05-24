"""
爬取策略
根据一个用户作为seed，将该用户的所有followed加入到seed集合
然后从这些seed集合中选取最近听歌超过20首的用户进行爬取，爬取这个用户的信息和最近听歌的信息
直到歌曲总数达到10w首位置

其中爬取用户的线程和爬取单个歌曲的线程都是单元素的线程
也就是说一个线程专门用来负责爬取一个用户或者一首歌
然后全局的线程总数保证为K个固定值
数据库在读写的时候，每个爬取线程都会向内存中写入信息
然后内存主线程在积累到了一定的数量的歌曲和用户之后写入到数据库线程中
"""
from queue import Queue
from UserSpider import UserSpider
from SongSpider import SongSpider
from database_demo import db_cls
import threading
import time
import random

class ThreadSafeData:
    def __init__(self):
        self.allSongids = []
        self.songSeedsList = Queue()
        self.userSeedsList = Queue()

        self.gsong_SongInfoList = []
        self.gsong_Song2SingerList = []
        self.guser_UserInfosList = []
        self.guser_User2SongList = []
        self.guser_User2SonglistList = []
        self.guser_FollowList = []

        self.lock_allSongids = threading.Lock()
        self.lock_gsong_SongInfoList = threading.Lock()
        self.lock_gsong_Song2SingerList = threading.Lock()
        self.lock_guser_UserInfosList = threading.Lock()
        self.lock_guser_User2SongList = threading.Lock()
        self.lock_guser_User2SonglistList = threading.Lock()
        self.lock_guser_FollowList = threading.Lock()

        self.db = None

    def create_db(self, db_filename = "pj_data.db"):
        self.db = db_cls(db_filename = db_filename)


    def addNewSongs_threadSafe(self, song_info_list, song2singer_list):
        self.lock_gsong_SongInfoList.acquire()
        self.gsong_SongInfoList.append(song_info_list)
        self.lock_gsong_SongInfoList.release()

        self.lock_gsong_Song2SingerList.acquire()
        self.gsong_Song2SingerList.extend(song2singer_list)
        self.lock_gsong_Song2SingerList.release()

    #this method will also extend the global seed list
    def addNewUsers_threadSafe(self, user_infos_list, user2song_list, user2songlist_list, follow_list):
        self.lock_guser_UserInfosList.acquire()
        self.guser_UserInfosList.append(user_infos_list)
        self.lock_guser_UserInfosList.release()

        self.lock_guser_User2SongList.acquire()
        self.guser_User2SongList.extend(user2song_list)
        for eachSong in user2song_list:
            self.songSeedsList.put(list(eachSong)[1])
        self.lock_guser_User2SongList.release()

        self.lock_guser_User2SonglistList.acquire()
        self.guser_User2SonglistList.extend(user2songlist_list)
        self.lock_guser_User2SonglistList.release()

        self.lock_guser_FollowList.acquire()
        self.guser_FollowList.extend(follow_list)
        for eachFollow in follow_list:
            self.userSeedsList.put(list(eachFollow)[1])
        self.lock_guser_FollowList.release()

    def writeIntoDatabase_threadSafe(self):
        self.lock_gsong_SongInfoList.acquire()
        self.lock_gsong_Song2SingerList.acquire()
        debug_print_thread(('song info list', self.gsong_SongInfoList))
        debug_print_thread(('song2singer list', self.gsong_Song2SingerList))
        self.db.write_Song_infos(self.gsong_SongInfoList, self.gsong_Song2SingerList)
        # self.db.create_index()
        self.gsong_SongInfoList.clear()
        self.gsong_Song2SingerList.clear()

        self.lock_gsong_Song2SingerList.release()
        self.lock_gsong_SongInfoList.release()

        self.lock_guser_UserInfosList.acquire()
        self.lock_guser_FollowList.acquire()
        self.lock_guser_User2SongList.acquire()
        self.lock_guser_User2SonglistList.acquire()

        debug_print_thread(('user info db', self.guser_UserInfosList))
        debug_print_thread(('user recent songs db', self.guser_User2SongList))
        debug_print_thread(('user songlist db', self.guser_User2SonglistList))
        debug_print_thread(('user follow db', self.guser_FollowList))

        self.db.write_User_infos(
            user_infos_list=self.guser_UserInfosList,
            user2song_list=self.guser_User2SongList,
            user2songlist_list=self.guser_User2SonglistList,
            follow_list=self.guser_FollowList
        )
        # self.db.create_index()
        self.guser_UserInfosList.clear()
        self.guser_User2SongList.clear()
        self.guser_User2SonglistList.clear()
        self.guser_FollowList.clear()

        self.lock_guser_User2SonglistList.release()
        self.lock_guser_User2SongList.release()
        self.lock_guser_FollowList.release()
        self.lock_guser_UserInfosList.release()
        


def debug_print_thread(msg):
    print('[*', threading.get_ident(), '*]', msg)

class ThreadPool:
    def __init__(self, threadMaxNums = 12):
        self.THREAD_MAX = threadMaxNums
        self.currentAvailThreads = self.THREAD_MAX
        self.availThreadCondi = threading.Condition()
        self.databaseWriteInCondi = threading.Condition()
        self.lock_availableThreads = threading.Lock()
        self.dataSpace = ThreadSafeData()
        self.dataSpace.userSeedsList.put(287829691)

        self.__first_db_initialize_flag = False

    def _util_scrapySingleUser(userUrl):
        up = UserSpider(userUrl)
        # up.getAllContents()
        res = up.getAllContents()
        if not up.UserConditionSatisfy20Songs():
            debug_print_thread('not satisfying with len ' +str(len(up.get_user2song_list())) )
            #pass do nothing
        elif res == "ok":
            #save it to class global variables
            debug_print_thread('satisfying the requirements, returning')
            debug_print_thread(('[**] song id seed list', up.get_user2song_list()))
            return [up.get_user_info(), up.get_user2song_list(), up.get_user2songlist_list(), up.get_follow_list()]
        else:
            return None

    def _thread_scrapyUserAndSave(self, userUrl, threadSafeData):
        debug_print_thread("new [*user*] thread seed is " + userUrl)
        res = ThreadPool._util_scrapySingleUser(userUrl)
        if(res != None):
            [user_infos_list, user2song_list, user2songlist_list, follow_list] = res
            debug_print_thread('adding new to data')
            debug_print_thread(user_infos_list)
            debug_print_thread(user2song_list)
            debug_print_thread(user2songlist_list)
            debug_print_thread(follow_list)
            threadSafeData.addNewUsers_threadSafe(
                tuple(user_infos_list),
                list(user2song_list),
                list(user2songlist_list),
                list(follow_list)
            )
        debug_print_thread('ending this user thread')
        self.lock_availableThreads.acquire()
        self.currentAvailThreads += 1
        self.lock_availableThreads.release()

    def _util_scrapySong(songUrl):
        sp = SongSpider(songUrl)
        res = sp.getInfo(sp.getPageSource())
        if res == "ok":
            song_info = sp.getSongRequiredTuple()
            song_artists = sp.getSongArtistsList()
            return [song_info, song_artists]
        else:
            debug_print_thread("song info not valid, returning None")
            return None

    def _thread_scrapySongAndSave(self, songUrl, threadSafeData):
        debug_print_thread("new [*song*] thread seed is " + songUrl)
        res = ThreadPool._util_scrapySong(songUrl)
        if(res != None):
            [song_info_tuple, song_artists_list] = res
            threadSafeData.addNewSongs_threadSafe(
                tuple(song_info_tuple),
                list(song_artists_list)
            )
        debug_print_thread('ending this song thread')
        self.lock_availableThreads.acquire()
        self.currentAvailThreads += 1
        self.lock_availableThreads.release()

    def newThread_User(self, userUrl):
        
        thread = threading.Thread(
            target=ThreadPool._thread_scrapyUserAndSave,
            args=(self, userUrl, self.dataSpace)
        )
        return thread        
        
    def newThread_Song(self, songUrl):
        thread = threading.Thread(
            target=ThreadPool._thread_scrapySongAndSave,
            args=(self, songUrl, self.dataSpace)
        )
        return thread

    def mainThread(self):
        while True:
            self.lock_availableThreads.acquire()
            for i in range(self.currentAvailThreads):
                if self.dataSpace.userSeedsList.empty():
                    debug_print_thread('current seed list empty')
                    break
                else:                    
                    debug_print_thread('start a new thread')
                    #randomly decide next is user or song
                    randres = random.choice([1,2])
                    if self.dataSpace.userSeedsList.empty(): randres = 2
                    elif self.dataSpace.songSeedsList.empty(): randres = 1
                    if(randres == 1): #then next user
                        id_next = self.dataSpace.userSeedsList.get()
                        user_thread = self.newThread_User('https://music.163.com/#/user/home?id=' + str(id_next))
                        user_thread.start()
                        self.currentAvailThreads -= 1
                    elif (randres == 2): #then next song
                        id_next = self.dataSpace.songSeedsList.get()
                        song_thread = self.newThread_Song('https://music.163.com/#/song?id=' + str(id_next))
                        song_thread.start()
                        self.currentAvailThreads -= 1

            self.lock_availableThreads.release()
            if self.availThreadCondi.acquire():
                self.availThreadCondi.notify()
                self.availThreadCondi.wait()
            self.availThreadCondi.release()
        
    def listenerThread(self):
        while True:
            #trying to produce new threads
            if(self.availThreadCondi.acquire()):
                if(self.currentAvailThreads > 0 and not self.dataSpace.songSeedsList.empty()):
                    self.availThreadCondi.notify()
                    self.availThreadCondi.wait()
            self.availThreadCondi.release()

            if(self.databaseWriteInCondi.acquire()):
                if(len(self.dataSpace.guser_UserInfosList) > 5 or len(self.dataSpace.gsong_SongInfoList) > 5):
                    self.databaseWriteInCondi.notify()
                    self.databaseWriteInCondi.wait()
            self.databaseWriteInCondi.release()

    def databaseWriteInThread(self):
        while True:
            if(self.databaseWriteInCondi.acquire()):
                if(len(self.dataSpace.guser_UserInfosList) > 5 or len(self.dataSpace.gsong_SongInfoList) > 5):
                    # if(not self.__first_db_initialize_flag):
                    self.dataSpace.create_db()
                    # self.__first_db_initialize_flag = False

                    self.dataSpace.writeIntoDatabase_threadSafe()
                    #then display the current stage information
                    db = self.dataSpace.db
                    
                    
                    songs = db.read_Data(sql_query="Select * FROM Song")
                    debug_print_thread("Main Thread, display all available songs, totally " + str(len(songs)))
                    for song in songs:
                        debug_print_thread(song)

                    users = db.read_Data(sql_query='Select * FROM User_Table')
                    debug_print_thread("Main Thread, display all available users, totally " + str(len(users)))
                    for user in users:
                        debug_print_thread(user)
                    db.close_db()
                    
                
                self.databaseWriteInCondi.notify()
                self.databaseWriteInCondi.wait()
            self.databaseWriteInCondi.release()




    




if __name__ == "__main__":
    try:
        tp = ThreadPool(threadMaxNums=4)
        threadingMain = threading.Thread(target=tp.mainThread, args=())
        threadingListener = threading.Thread(target=tp.listenerThread, args=())
        threadDb = threading.Thread(target=tp.databaseWriteInThread, args=())
        threadingMain.start()
        threadingListener.start()
        threadDb.start()
    finally:
        pass
        
        


    






    




    


