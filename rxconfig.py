import reflex as rx
import os


env="PROD"

railway_domain = "RAILWAY_PUBLIC_DOMAIN"
db = "postgres:admin12345@152.173.9.111:5432/postgres" if os.environ.get("DATABASE_URL") is None else os.environ.get("DATABASE_URL")

val = db if env == "PROD" else "postgres:admin12345@localhost:5432/postgres"

conn ="postgresql+psycopg2://" + val

print(conn)

class ReflextemplateConfig(rx.Config):
    pass

config = ReflextemplateConfig(
    app_name="DevForum",
    deploy_url="devforum-production.up.railway.app",
    db_url=conn,
    frontend_port=3000, # default frontend port
    backend_port=8000, # default backend port
    # use https and the railway public domain with a backend route if available, otherwise default to a local address
    api_url=f'https://{os.environ[railway_domain]}/backend' if railway_domain in os.environ else "http://127.0.0.1:8000"
)