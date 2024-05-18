import reflex as rx


conn = "sqlite:///DevForum/Backend/Database/database.db"

class ReflextemplateConfig(rx.Config):
    pass

config = ReflextemplateConfig(
    app_name="DevForum",
    db_url=conn,
    frontend_port=3000, # default frontend port
    backend_port=8000, # default backend port
)