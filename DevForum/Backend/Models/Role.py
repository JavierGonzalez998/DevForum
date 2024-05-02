import reflex as rx
import sqlmodel

class Role(rx.Model, table=True):
    roleId:int = sqlmodel.Field(primary_key=True)
    name:str