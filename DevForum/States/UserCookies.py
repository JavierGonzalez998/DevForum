import reflex as rx

class userCookie(rx.State):
    auth_token: str = rx.Cookie("", path="/")

    def setAuthCookie(self, token:str):
        self.auth_token = token

    def getAuthCookie(self):
        return self.auth_token
    
    def Logout(self):
        self.auth_token = ""