import reflex as rx
from DevForum.Backend.Models.Category import Category
from DevForum.Backend.Models.Auth import Auth
from DevForum.States.UserCookies import userCookie
from DevForum.Backend.DTO.CategoryDTO import CategoryWithPost
from typing import List
import sqlalchemy

class responseAllCat:
    category: Category
    posts: int

class BackendCategory(rx.State):
    catId: int
    name:str

    listCat: List[responseAllCat]

    listAllCat: List[Category]
    
    responseCat: List[str] = []

    catWithPosts: List[CategoryWithPost]

    def getAllCatWithPosts(self):
        with rx.session() as session:
            aux = session.exec(
                sqlalchemy.text(
                    '''select c."catId" , c."name" , count(p."postId") as "postCount"  from category c inner join post p on p.cat_id =c."catId" group by p."postId", c."catId" '''
                )
            ).all()
            del self.catWithPosts[:]
            for row in aux:
                row_as_dict = row._mapping
                res = CategoryWithPost(idCat=row_as_dict["catId"],name=row_as_dict["name"], nPost=row_as_dict["postCount"])
                self.catWithPosts.append(res)

    async def getAllCat(self):
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            res = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()
        if res is not None:
            with rx.session() as session:
                self.listAllCat = session.exec(
                    Category.select()
                ).all()

    async def getAllListCat(self):
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            res = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()

        if res is not None:
            with rx.session() as session:
                self.listAllCat = session.exec(
                    Category.select()
                ).all()
            del self.responseCat[:]
            for i in self.listAllCat:
                self.responseCat.append(i.name)
            print(f"posts: {self.responseCat}")
    async def addCat(self):
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
                    session.add(
                        Category(
                            name=self.name
                        )
                    )
                    session.commit()
                return True
            except():
                return False
    