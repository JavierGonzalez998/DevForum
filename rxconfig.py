import reflex as rx
import os
from dotenv import load_dotenv,find_dotenv


railway_domain = "RAILWAY_PUBLIC_DOMAIN"

load_dotenv(find_dotenv())

db = os.getenv("POSTGRE_DB_CONN")

class ReflextemplateConfig(rx.Config):
    pass

config = ReflextemplateConfig(
    app_name="DevForum",
    deploy_url="devforum-production.up.railway.app",
    db_url=f"postgresql+psycopg2://{db}",
    frontend_port=3000, # default frontend port
    backend_port=8000, # default backend port
    # use https and the railway public domain with a backend route if available, otherwise default to a local address
    api_url=f'https://{os.environ[railway_domain]}/backend' if railway_domain in os.environ else "http://127.0.0.1:8000"
)