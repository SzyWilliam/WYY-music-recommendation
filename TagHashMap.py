class TagHashMap:

    def __init__(self):
        self.map = dict()
        self.index = 1

    def get(self, key):
        return self.map[key]

    def addNewTag(self, key):
        if self.map.get(key) != None:  
            return self.map.get(key)
        else:
            self.index += 1
            self.map[key] = self.index
            return self.map.get(key)

    def getAllMapping(self):
        return self.map


#unit test cases
if __name__ == "__main__":
    mmap = TagHashMap()
    mmap.addNewTag('你好')
    mmap.addNewTag('很好')
    print(mmap.get('你好'))
    mmap.addNewTag('你好')
    print(mmap.get('你好'))
    print(mmap.getAllMapping())
