from SongSpider import  SongSpider
from database_demo import db_cls
import random
import time

def ScrapeAndSaveSong(seedUrl, maxNum = 1000):
    nextUrl = seedUrl
    i = 0
    song_infos_list = set()
    song2singer_list = []
    id_seed_list = set()
    visted_list = set()
    visted_list.add(int(seedUrl.split('=')[1]))

    
    while(i < maxNum):
        sp = SongSpider(nextUrl)
        res = sp.getInfo(sp.getPageSource())
        if(res == "ok"):

            #add all the ids of similar songs into the seed list
            id_seed_list = id_seed_list.union(set(list(sp.getSongRequiredTuple())[3:-1]))

            #save the song info into the outter list
            song_infos_list.add(sp.getSongRequiredTuple())
            
            #save the singers into the outter list
            song2singer_list.extend(sp.getSongArtistsList())
        
        i += 1

        #use a random seed to construct the next song
        # print(id_seed_list)
        nextSeed = id_seed_list.pop()
        # print(nextSeed)
        while nextSeed in visted_list:
            nextSeed = id_seed_list.pop()
            # print(nextSeed)

        visted_list.add(nextSeed)
        
        nextUrl = 'https://music.163.com/#/song?id=' + str(nextSeed)
        print(nextUrl)
    
    print(sorted(list(visted_list)))

    return [list(song_infos_list), song2singer_list]




if __name__ == "__main__":

    db = db_cls(db_filename="pj_data.db")

    start_time = time.time()
    [song_infos_list, song2singer_list] = ScrapeAndSaveSong(seedUrl='https://music.163.com/#/song?id=186453', maxNum=100)
    db.write_Song_infos(song_infos_list, song2singer_list)
    db.create_index()
    end_time = time.time()

    print('execution for 100 songs is ' + str(end_time - start_time))
    print(db.read_Data(sql_query="Select * FROM Song"))
    db.close_db()




