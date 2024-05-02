import reflex as rx

async def api_test():
    return {"hola": "mundo"}

app = rx.App()
app.api.add_api_route("/hola", api_test)