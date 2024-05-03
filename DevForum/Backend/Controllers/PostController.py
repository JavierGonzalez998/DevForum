import reflex as rx
from DevForum.Backend.Models.Post import Post
from DevForum.States.UserCookies import userCookie
from DevForum.Backend.Models.Auth import Auth
from DevForum.States.UserCookies import userCookie
from DevForum.Backend.Models.Category import Category
from DevForum.Backend.Models.Comment import Comment
from DevForum.Backend.DTO.PostDetailDTO import DTOPostDetail, DTORankPost
from typing import List
import sqlalchemy

class userPostDTO(rx.Base):
    postId:int
    title:str
    cat:str
    desc: str
    content:str
    posted_at: str



class getUserPost(rx.State):
    #Datos del post a manejar
    title:str
    cat:str
    desc: str
    content:str
    #Respuesta de la BD 
    userPosts: List[userPostDTO]
    detailPost: DTOPostDetail = None
    topPost: List[DTORankPost]

    def getAllPosts(self):
        with rx.session() as session:
            self.userPosts = session.exec(
                Post.select().order_by(Post.posted_at,"desc")
            ).all()

    def topCommentedPosts(self):
        with rx.session() as session:
            aux = session.exec(
                sqlalchemy.text(
                    'select p."postId", p.title, p."desc" , p."content" , p.posted_at , c."name" , u.username , count(c2."commentId") as "countComment" from post p inner join category c  on c."catId"  = p.cat_id inner join "user" u on u."userId" = p.user_id inner join  "comment" c2 on c2.post_id  = p."postId" group by p."postId", c."name" , u.username  order by count(c2."commentId") desc'
                )
            )
            del self.topPost[:]
            for row in aux:
                row_as_dict = row._mapping
                res = DTORankPost(postId=row_as_dict["postId"], title=row_as_dict["title"], desc=row_as_dict["desc"], posted_at=row_as_dict["posted_at"], cat=row_as_dict["name"], comments=row_as_dict["countComment"], username=row_as_dict["username"])
                self.topPost.append(res)
    
    def getPostByName(self, name):
        with rx.session() as session:
            aux = session.exec(
                sqlalchemy.text(
                    f'''select p."postId" ,p.user_id ,p.title ,p."desc" , p."content" , p.posted_at, c."name" from post p inner join category c on c."catId" = p.cat_id where p.title like '%{name}%'; '''
                )
            )
            del self.userPosts[:]
            for row in aux:
                row_as_dict = row._mapping
                res = userPostDTO(postId=row_as_dict["postId"],title=row_as_dict["title"], cat=row_as_dict["name"], desc=row_as_dict["desc"], content=row_as_dict["content"], posted_at=row_as_dict["posted_at"])
                self.userPosts.append(res)       

    def getPostByCat(self):
        with rx.session() as session:
            aux = session.exec(
                Category.select().where(Category.name.contains(self.cat))
            ).first()
            aux = session.exec(
                sqlalchemy.text(
                    f'''select p."postId", p.title, p.user_id , p."desc" ,p."content" ,c."name" , p.posted_at  from post p inner join category c on p.cat_id = c."catId" where c."catId" = {aux.catId} order by p.posted_at desc'''
                )
            )
            del self.userPosts[:]
            for row in aux:
                row_as_dict = row._mapping
                res = userPostDTO(postId=row_as_dict["postId"],title=row_as_dict["title"], cat=row_as_dict["name"], desc=row_as_dict["desc"], content=row_as_dict["content"], posted_at=row_as_dict["posted_at"])
                self.userPosts.append(res)

    async def getUserPosts(self):
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            res = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()
        print(res)
        if res is not None:    
            with rx.session() as session:
                stmt = f'''select p."postId" , p.title , p."desc" , p."content" , c."name" , p.posted_at from post p inner join category c on p."cat_id" = c."catId" WHERE p."user_id" = {str(res.user_id)} '''
                response= session.exec(
                    sqlalchemy.text(
                        stmt
                    )
                ).all()
                if response is not None:
                    print(response)
                    del self.userPosts[:]
                    for row in response:
                        row_as_dict = row._mapping
                        res = userPostDTO(postId=row_as_dict["postId"],title=row_as_dict["title"], cat=row_as_dict["name"], desc=row_as_dict["desc"], content=row_as_dict["content"], posted_at=str(row_as_dict["posted_at"]))
                        self.userPosts.append(res)
                    
    async def loadPost(self, postId:int):
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            res = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()
        if res is not None:
            with rx.session() as session:
                aux = session.exec(
                    Post.select().where(
                        Post.postId == postId
                    )
                ).first()
            print(aux)
            if aux is not None:
                self.title = aux.title
                self.desc = aux.desc
                self.content = aux.content

    async def addPost(self) -> bool:
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            res = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()
        if res is not None:
            try:
                with rx.session() as session:
                    cat = session.exec(Category.select().where(Category.name.contains(self.cat))).first()
                    session.add(
                        Post(
                            user_id=res.user_id,
                            title=self.title,
                            desc=self.desc,
                            cat_id=cat.catId,
                            content= self.content
                        )
                    )
                    session.commit()
                return True
            except():
                return False
        else:
            return False

    async def editPost(self, idPost):
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            res = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()
        if res is not None:
            try:
                with rx.session() as session:
                    cat = session.exec(Category.select().where(Category.name.contains(self.cat))).first()
                    post = session.exec(
                        Post.select().where(
                            Post.postId == idPost
                        )
                    ).first()
                    post.title = self.title
                    post.cat_id = cat.catId
                    post.desc = self.desc
                    post.content = self.content
                    session.add(post)
                    session.commit()
                return True
            except():
                return False
        return False

    async def deletePost(self, idPost):
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            res = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()
        if res is not None:
            try:
                with rx.session() as session:
                    response = session.exec(
                        Post.select().where(
                            Post.postId == idPost
                        )
                    ).first()
                    session.delete(response)
                    session.commit()
                return True
            except():
                return False
        else:
            return False
    
    async def getPostDetail(self, idPost):
        with rx.session() as session:
            stmt = f'''select p.postId , p.title , p."desc" , p."content" , c."name" as cat, u.username, p.posted_at , p.updated_at  from post p inner join category c on c."catId" = p."cat_id" inner join "user" u on u."userId" =p."user_id" where p."postId" =  {str(idPost)} '''
            print(stmt)
            aux = session.exec(
                sqlalchemy.text(
                    stmt
                )
            ).first()
            if aux is not None:
                res = DTOPostDetail(postId=aux.postId,title=aux.title, cat=aux.cat,username=aux.username,updated_at=aux.updated_at,desc=aux.desc, content=aux.content, posted_at=aux.posted_at, comments=[])

                comm = session.exec(
                    Comment.select().where(Comment.post_id.contains(idPost))
                ).all()
                res.comments = comm

                self.detailPost = res