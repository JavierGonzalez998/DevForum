import reflex as rx
import sqlmodel

class Category(rx.Model, table=True):
    catId:int = sqlmodel.Field(primary_key=True)
    name: str