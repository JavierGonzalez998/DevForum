import reflex as rx
import sqlmodel
import datetime
import sqlalchemy

class Auth(rx.Model, table=True):
    user_id: int = sqlmodel.Field(foreign_key="user.userId")
    token: str
    logged: datetime.datetime = sqlmodel.Field(
        default=sqlalchemy.func.now(),
        sa_column=sqlalchemy.Column(
            "posted_at",
            sqlalchemy.DateTime(timezone=True),
            server_default=sqlalchemy.func.now(),
        ),)