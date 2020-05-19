from SongSpider import  SongSpider
from database_demo import db_cls
import random
import time
from queue import Queue
import threading

maxNum = 1000
#global_data_structure:
id_seed_list = Queue(maxNum)
visited_list = []
visited_list_lock = threading.Lock()
global_song_infos_list = []
global_song2singer_list = []
global_count = 0
def print_thread(str):
    # print('[*',threading.get_ident(),']', str)
    pass

def ScrapeAndSaveSong(seedUrl, maxNum = 1000):
    global id_seed_list
    global visited_list
    nextUrl = seedUrl
    i = 0
    song_infos_list = set()
    song2singer_list = []
    print_thread('begining while')

    visited_list_lock.acquire()

    visited_list.append(int(seedUrl.split('=')[1]))
    visited_list_lock.release()

    
    while(i < maxNum):
        print_thread('entering while with index=' + str(i))
        sp = SongSpider(nextUrl)
        res = sp.getInfo(sp.getPageSource())
        if(res == "ok"):

            #add all the ids of similar songs into the seed list
            # id_seed_list = id_seed_list.union(set(list(sp.getSongRequiredTuple())[3:-1]))
            nextSongSeeds = list(sp.getSongRequiredTuple())[3:-1]
            print_thread('entering while:for adding id seedlist')
            for item in nextSongSeeds:
                print_thread('in for, adding seeds')
                id_seed_list.put(item, timeout=5.0)
            print_thread("id seed list append")

            #save the song info into the outter list
            song_infos_list.add(sp.getSongRequiredTuple())
            
            #save the singers into the outter list
            song2singer_list.extend(sp.getSongArtistsList())
        
        i += 1

        #use a random seed to construct the next song
        # print(id_seed_list)
        nextSeed = id_seed_list.get()
        # print(nextSeed)
        visited_list_lock.acquire()

        while nextSeed in visited_list:
            print_thread("changing to a unvisited seed")
            nextSeed = id_seed_list.get()
            # print(nextSeed)
        visited_list.append(nextSeed)
        print_thread( "visited list append next seed")

        visited_list_lock.release()
        # visted_list.add(nextSeed)
        
        nextUrl = 'https://music.163.com/#/song?id=' + str(nextSeed)
        print(nextUrl)
    
    # wprint(sorted(list(visted_list)))

    return [list(song_infos_list), song2singer_list]

def Thread_Scrapy(seedUrl, maxNum):
    start_time = time.time()
    [song_infos_list, song2singer_list] = ScrapeAndSaveSong(seedUrl, maxNum)
    
    # db.write_Song_infos(song_infos_list, song2singer_list)
    global_song_infos_list.extend(song_infos_list)
    global_song2singer_list.extend(song2singer_list)
    end_time = time.time()
    print('process finished with execution time ', end_time-start_time)
    global global_count
    global_count += 1
    # db.create_index()


if __name__ == "__main__":

    db = db_cls(db_filename="pj_data.db")

   


    
    thread1 = threading.Thread(target=Thread_Scrapy, args=('https://music.163.com/#/song?id=31877628', 25))
    thread2 = threading.Thread(target=Thread_Scrapy, args=('https://music.163.com/#/song?id=186453', 25))
    thread3 = threading.Thread(target=Thread_Scrapy, args=('https://music.163.com/#/song?id=399410693', 25))
    thread4 = threading.Thread(target=Thread_Scrapy, args=('https://music.163.com/#/song?id=1989355', 25))
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    # thread1.join()
    # thread2.join()
    # thread3.join()
    while global_count != 4:
        time.sleep(5)
    db.write_Song_infos(global_song_infos_list, global_song2singer_list)
    db.create_index()
    # print('execution for 100 songs is ' + str(end_time - start_time))
    songs = db.read_Data(sql_query="Select * FROM Song")
    print(songs)
    print('valid song numbers', len(songs))
    db.close_db()
    



