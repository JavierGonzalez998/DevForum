import reflex as rx
import sqlmodel
import datetime
import sqlalchemy

class Comment(rx.Model, table=True):
    commentId:int = sqlmodel.Field(primary_key=True)
    post_id: int = sqlmodel.Field(foreign_key="post.postId", nullable=False)
    user_id: int = sqlmodel.Field(foreign_key="user.userId", nullable=False)
    comment: str
    date: datetime.datetime = sqlmodel.Field(
        default=sqlalchemy.func.now(),
        sa_column=sqlalchemy.Column(
            "date",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),)