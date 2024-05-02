import reflex as rx
from DevForum.Backend.Controllers.PostController import getUserPost
class HandleSearchState(rx.State):
    text:str = ""

    def setText(self, text:str):
        self.text = text

    def handleSubmit(self):
        print(self.text)
        return rx.redirect(f"/search/{self.text}")

def SearchBar() -> rx.Component:
    return  rx.hstack(
                rx.input(placeholder="Ingrese un tema", max_length="200", width="20rem", value=getUserPost.title, on_change=getUserPost.set_title),
                rx.button(rx.icon(tag="search"),"Buscar",color_scheme="cyan", on_click=rx.redirect(f"/search/{getUserPost.title}")),
                align="center",
                justify="center",
                height="100%",
            ),