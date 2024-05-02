import reflex as rx
import sqlmodel
import datetime
import sqlalchemy

class Post(rx.Model, table=True):
    postId: int = sqlmodel.Field(primary_key=True)
    user_id: int = sqlmodel.Field(foreign_key="user.userId")
    title:str
    desc:str
    content:str
    cat_id:int = sqlmodel.Field(foreign_key="category.catId", nullable=True)
    posted_at: datetime.datetime = sqlmodel.Field(
        default=sqlalchemy.func.now(),
        sa_column=sqlalchemy.Column(
            "posted_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),)
    updated_at: datetime.datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "updated_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),)
    deleted_at: datetime.datetime = sqlmodel.Field(
        default=None,
        sa_column=sqlalchemy.Column(
            "deleted_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),)