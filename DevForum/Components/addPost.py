import reflex as rx
from DevForum.Backend.Controllers.PostController import getUserPost
from DevForum.Backend.Controllers.CategoryController import BackendCategory
from typing import List

class addPostClass(rx.State):
    async def handleAddPost(self):
        add = await self.get_state(getUserPost)
        response = await add.addPost()
        if response:
            return rx.redirect("/forum")

class handleCat(rx.State):
    catList: List[str] = []
    selected:str

    async def loadCat(self):
        cat = await self.get_state(BackendCategory)
        await cat.getAllListCat()
        self.catList = cat.responseCat
            
        
def addPost() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("plus"), "Agregar Post", color_scheme="plum", variant="outline")),
        rx.dialog.content(
            rx.dialog.title("Agregar Post"),
            rx.dialog.description(
                "Para agregar un post, complete los siguientes campos",
                margin="1rem 0"
            ),
            rx.flex(
                rx.text(
                    "TÍtulo del post",
                    as_="div",
                    size="2",
                    margin_bottom="4px",
                    weight="bold"
                ),
                rx.input(
                    placeholder="Ingresa un título para el post",
                    color_scheme="plum", variant="soft", radius="full",
                    value=getUserPost.title,
                    on_change=getUserPost.set_title
                ),
                rx.text(
                    "Categoría",
                    as_="div",
                    size="2",
                    margin_bottom="4px",
                    weight="bold",
                ),
                rx.select(BackendCategory.responseCat, on_change=getUserPost.set_cat, placeholder="Seleccione una categoría", color_scheme="plum", variant="soft", radius="full"),
                rx.text(
                    "Descripción del post",
                    as_="div",
                    size="2",
                    margin_bottom="4px",
                    weight="bold"
                ),
                rx.input(
                    placeholder="Ingresa una pequeña descripción del post",
                    color_scheme="plum", variant="soft", radius="full",
                    value=getUserPost.desc,
                    on_change=getUserPost.set_desc
                ),
                 rx.text(
                    "Contenido del post",
                    as_="div",
                    size="2",
                    margin_bottom="4px",
                    weight="bold"
                ),
                rx.vstack(
                    rx.text_area(
                        placeholder="Escriba el contenido del post...",
                        size="3",
                        width="100%",
                        color_scheme="plum", variant="soft", radius="full",
                        value=getUserPost.content,
                        on_change=getUserPost.set_content
                    ),
                    rx.text("(Les prometo que buscaré la forma de integrar texto enriquecido ♥)", size="1", weight="light"),
                    width="100%"                    
                ),
                direction="column",
                spacing="3",
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cancel",
                        color_scheme="gray",
                        variant="soft",
                    ),
                ),
                rx.dialog.close(
                    rx.button("Save", color_scheme="plum", on_click=addPostClass.handleAddPost),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
        ),
        on_mount=handleCat.loadCat
    )