import reflex as rx
import os


env="PROD"

railway_domain = "RAILWAY_PUBLIC_DOMAIN"
db = "postgres:msemSBRKuEuguWFvsMDsqczpUBGGqCGn@viaduct.proxy.rlwy.net:41996/railway" if os.environ.get("DATABASE_URL") is None else os.environ.get("DATABASE_URL")

val = db if env == "PROD" else "postgres:admin12345@localhost:5432/postgres"

conn = "sqlite:///DevForum/Backend/Database/database.db"

print(conn)

class ReflextemplateConfig(rx.Config):
    pass

config = ReflextemplateConfig(
    app_name="DevForum",
    db_url=conn,
    frontend_port=3000, # default frontend port
    backend_port=8000, # default backend port
    # use https and the railway public domain with a backend route if available, otherwise default to a local address
    api_url=f'https://{os.environ[railway_domain]}/backend' if railway_domain in os.environ else "http://127.0.0.1:8000"
)