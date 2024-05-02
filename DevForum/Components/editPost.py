import reflex as rx
from DevForum.Backend.Controllers.PostController import getUserPost
from DevForum.Backend.Controllers.CategoryController import BackendCategory

class EditPostClass(rx.State):
    selectedCat: str = ""
    async def handleEditPost(self, idPost):
        add = await self.get_state(getUserPost)
        response = await add.editPost(idPost)
        if response:
            return rx.redirect("/forum")
        
    async def loadUser(self, id):
        user = await self.get_state(getUserPost)
        await user.loadPost(id)
        self.selectedCat = user.cat
    
    async def loadCatList(self):
        cat = await self.get_state(BackendCategory)
        await cat.getAllCat()
        
def editPost(postId):

    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("pencil"), "Editar Post", color_scheme="yellow", variant="outline", on_click=EditPostClass.loadUser(postId))),
        rx.dialog.content(
            rx.dialog.title("Editar Post"),
            rx.dialog.description(
                "Para editar un post, complete los campos que desee cambiar",
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
                rx.select(BackendCategory.responseCat, default_value=EditPostClass.selectedCat, on_change=getUserPost.set_cat, placeholder="Seleccione una categoría", color_scheme="plum", variant="soft", radius="full"),
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
                on_mount=EditPostClass.loadCatList
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
                    rx.button("Save", color_scheme="plum", on_click=EditPostClass.handleEditPost(postId)),
                ),
                spacing="3",
                margin_top="16px",
                justify="end",
            ),
        ),
    )