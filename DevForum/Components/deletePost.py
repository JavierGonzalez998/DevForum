import reflex as rx
from DevForum.Backend.Controllers.PostController import getUserPost

class DeletePostClass(rx.State):
    async def handleDeletePost(self, idPost):
        add = await self.get_state(getUserPost)
        response = await add.deletePost(idPost)
        if response:
            return rx.redirect("/forum")
        
    async def loadUser(self, id):
        user = await self.get_state(getUserPost)
        await user.loadPost(id)
        
def deletePost(postId):

    return rx.dialog.root(
        rx.dialog.trigger(rx.button(rx.icon("trash"), "Eliminar Post", color_scheme="red", variant="outline", on_click=DeletePostClass.loadUser(postId))),
        rx.dialog.content(
            rx.dialog.title("Eliminar Post"),
            rx.flex(
                rx.heading(f"Desea eliminar el post: {getUserPost.title}?", size="5"),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            color_scheme="gray",
                            variant="soft",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button("Eliminar", color_scheme="red", on_click=DeletePostClass.handleDeletePost(postId)),
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
                direction="column",
                spacing="3",
            ),
        ),
    )