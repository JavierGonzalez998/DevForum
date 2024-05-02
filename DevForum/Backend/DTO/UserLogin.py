from DevForum.Backend.Models.User import User

class UserLoginDto(User):
    username:str
    email: str
    userId:int