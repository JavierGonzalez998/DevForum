import reflex as rx
from DevForum.Backend.Models.User import User
from DevForum.States.UserCookies import userCookie
from DevForum.Backend.Models.Auth import Auth
from DevForum.States.UserCookies import userCookie
from DevForum.utils.utils import RegisterencryptPass, LoginCheckPassword
from DevForum.States.LoadingState import LoadingState
import time
import jwt
import datetime

class userAuth(rx.State):
    email:str
    passwrd: str
    response: User = None
    
    auth_token:str = rx.Cookie("")

    def cleanData(self):
        self.email = "",
        self.passwrd = ""

    async def LoginUser(self):
        auth_token = await self.get_state(userCookie)
        with rx.session() as session:
            self.response = session.exec(
                User.select().where(
                    User.email.contains(self.email)
                )
            ).first()
        if self.response is not None:
            if(LoginCheckPassword(self.passwrd, self.response.passwrd)):
                encoded_jwt = jwt.encode({"auth": str(self.response.userId)+datetime.date.today().strftime("%B%d%Y")}, "secret", algorithm="HS256")
                with rx.session() as session:
                    token = session.exec(
                        Auth().select().where(Auth.user_id == int(self.response.userId))
                    ).first()
                    if token is not None:
                        session.delete(token)
                    else:
                        session.add(
                            Auth(
                                user_id=self.response.userId, token=encoded_jwt
                            )
                        )
                    session.commit()
                self.cleanData()
                auth_token.setAuthCookie(encoded_jwt)
            else:
                self.response = None
        else:
            return None
    
class userData(rx.State):
    username: str
    mail: str
    imgPhoto: str = ""
    role: int = 1
    passwrd:str
    confirmPasswrd: str

    async def registerUser(self) -> User:
        try:
            with rx.session() as session:
                res = session.exec(
                    User.select().where(User.email.contains(self.mail))
                ).first()
            if res is None:
                with rx.session() as session:
                    session.add(
                        User(
                            username=self.username,
                            email= self.mail,
                            passwrd= RegisterencryptPass(self.passwrd),
                            role_id = 2,
                            profileimg=self.imgPhoto

                        )
                    )
                    session.commit()

                return True
            else:
                return False
        except():
            return False     

    async def getUserData(self) -> User:
        time.sleep(2)
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            res = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()
        if res is not None:    
            with rx.session() as session:
                users = session.exec(
                    User.select().where(
                        User.userId == int(res.user_id)
                    )
                ).first()
            if users is not None:
                self.set_username(users.username)
                self.set_mail(users.email)
                self.set_imgPhoto(users.profileimg)
                self.set_role(users.role_id)
                self.set_passwrd("")
                self.set_confirmPasswrd("")
    
    async def updateUserData(self) -> bool:
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            res = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()
        if res is not None:
            with rx.session() as session:
                user = session.exec(
                User.select().where(
                        (User.userId == res.user_id)
                    )   
                ).first()
                passwd = ""
                if (self.passwrd == ""):
                    passwd = user.passwrd 
                else:
                    passwd = RegisterencryptPass(self.passwrd)
                user.email = self.mail
                user.username = self.username
                user.profileimg = self.imgPhoto
                user.passwrd = passwd
                session.add(user)
                session.commit()
            auth.Logout()

            return True
        else:
            return False        
    
    async def Logout(self) -> bool:
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            user = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()
            if user is not None:
                response = session.exec(
                    Auth.select().where(
                        Auth.user_id == user.user_id
                    )
                ).all()
                if response is not None:
                    for i in response:
                        session.delete(i)
                        session.commit()
        auth.Logout()
        return True

    async def isLogged(self) -> bool:
        auth = await self.get_state(userCookie)
        with rx.session() as session:
            user = session.exec(
                Auth.select().where(
                    Auth.token.contains(auth.getAuthCookie())
                )
            ).first()
        if user is not None:
            return True
        else:
            return False