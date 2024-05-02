class userPostDTO:
    postId:int
    title:str
    cat:str
    desc: str
    content:str
    posted_at: str

    def setPostId(self, id):
        self.postId = id

    def setTitle(self, title):
        self.title = title

    def setCat(self, cat):
        self.cat = cat

    def setDesc(self, desc):
        self.desc = desc
    
    def setContent(self, content):
        self.content = content
    
    def setPostedAt(self, postedAt):
        self.posted_at = postedAt

    def getPostId(self):
        return self.postId

    def getTitle(self):
        return self.title

    def getCat(self):
        return self.cat

    def getDesc(self):
        return self.desc
    
    def getContent(self):
        return self.content
    
    def getPostedAt(self):
        return self.posted_at