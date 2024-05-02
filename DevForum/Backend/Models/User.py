import reflex as rx
import sqlmodel

class User(rx.Model, table=True):
    userId:int = sqlmodel.Field(primary_key=True)
    username: str
    role_id: int
    email: str
    passwrd: str
    profileimg: str