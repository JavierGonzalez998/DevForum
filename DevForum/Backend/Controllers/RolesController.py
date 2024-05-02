import reflex as rx
from DevForum.Backend.Models.Role import Role
from DevForum.Backend.Models.Auth import Auth
from DevForum.States.UserCookies import userCookie
from typing import List

class Roles(rx.State):
    roleId: int
    name: str = ""

    listRoles: List[Role]

    async def addRoles(self):
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
                        Role(
                            name=self.name
                        )
                    )
                    session.commit()
                return True
            except():
                return False
        else:
            return False
    async def getAllRoles(self):
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            res = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()
        if res is not None:
            with rx.session() as session:
                self.listRoles = session.exec(
                    Role.select()
                ).all()
    
    async def GetOneRole(self, roleId):
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
                    Role.select().where(
                        Role.roleId == roleId
                    )
                ).first()
            self.name = aux.name
            self.roleId = aux.roleId
    
    async def editRole(self, roleId):
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
                    Role.select().where(
                        Role.roleId == roleId
                    )
                ).first()
                aux.roleId = self.roleId
                aux.name = self.name
                session.add(aux)
                session.commit()
    
    async def deleteRole(self, roleId):
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
                    Role.select().where(
                        Role.roleId == roleId
                    )
                ).first()
                session.delete(aux)
                session.commit()