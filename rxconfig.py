import reflex as rx


conn = "sqlite:///DevForum/Backend/Database/database.db"

class ReflextemplateConfig(rx.Config):
    pass

config = ReflextemplateConfig(
    app_name="DevForum",
    db_url=conn,
    deploy_url="https://6648ba6e9b39f90008d47758--zingy-pasca-d1f1b6.netlify.app/",
    frontend_port=3000, # default frontend port
    backend_port=8000, # default backend port
)