from fastapi import FastAPI
from mangum import Mangum
from DevForum import DevForum as reflex_app

app = FastAPI()
app.mount("/", reflex_app)

handler = Mangum(app)