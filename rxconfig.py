import reflex as rx
import os
from dotenv import load_dotenv,find_dotenv


load_dotenv(find_dotenv())

db = os.getenv("POSTGRE_DB_CONN")

class ReflextemplateConfig(rx.Config):
    pass

config = ReflextemplateConfig(
    app_name="DevForum",
    db_url=f"postgresql+psycopg2://{db}",
    frontend_port=3000, # default frontend port
    backend_port=8000, # default backend port
)