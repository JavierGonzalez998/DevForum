import reflex as rx
from DevForum.Components.navbar import navbar
from DevForum.Components.addPost import addPost
from DevForum.Components.editPost import editPost
from DevForum.Components.deletePost import deletePost
from DevForum.Components.categories import cat
from DevForum.Components.roles import roles
from DevForum.Backend.Controllers.UserController import userData
from DevForum.Backend.Controllers.PostController import getUserPost, userPostDTO
from typing import List

import base64
class ImgState(rx.State):
    """The app state."""

    # The images to show.
    img: str = ""

    async def handle_upload(self, files: List[rx.UploadFile]):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            
            contenido_base64 = base64.b64encode(upload_data).decode()

            enlace_html = f'data:image/png;base64,{contenido_base64}'
            # Update the img var.
            user = await self.get_state(userData)
            user.imgPhoto = enlace_html


class validatePassword(rx.State):
    samePass:bool = True
    errorUpdate = False

    async def validatePass(self,text):
        user = await self.get_state(userData)
        if text == user.passwrd:
            self.samePass = True
        else:
            self.samePass = False
        user.set_confirmPasswrd(text)
    
    def setErrorUpdate(self, update:bool):
        self.errorUpdate = update

class sumbitChange(rx.State):
    async def updateUser(self):
        user = await self.get_state(userData)
        response = await user.updateUserData()
        if response:
            return rx.redirect("/login?update=true")
        else:
            validatePassword.setErrorUpdate(True)

class ManagePosts(rx.State):
    postListTable:List[userPostDTO]

    async def getAllUserPost(self):
        posts = await self.get_state(getUserPost)
        await posts.getUserPosts()
        self.postListTable = posts.userPosts


def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.box(
                    rx.heading("Perfil", size="4", weight="light", width="100%", textAlign="center"),
                    rx.divider(size="4"),
                    width="100%",
                    paddingTop="1rem"
                ),
                rx.vstack(
                   rx.tabs.root(
                        rx.tabs.list(
                            rx.tabs.trigger("Usuario", value="tab1"),
                            rx.tabs.trigger("Posts", value="tab2"),
                            rx.cond(userData.role == 1, rx.fragment(rx.tabs.trigger("Roles", value="tab3"), rx.tabs.trigger("Categorias",value="tab4")), None)
                        ),
                        rx.tabs.content(
                            profile(),
                            value="tab1"
                        ),
                        rx.tabs.content(
                            posts(),
                            value="tab2",
                        ),
                        rx.cond(userData.role == 1,rx.fragment(rx.tabs.content(
                            roles(),
                            value="tab3",
                        ),
                        rx.tabs.content(
                            cat(),
                            value="tab4",
                        )), None),
                        default_value="tab1",
                        width="100%"  
                    ),
                    width="100%"
                ),
                width="100%",
                height="50rem",
                boxShadow="rgba(0, 0, 0, 0.24) 0px 3px 8px",
                backgroundColor="white",
                borderRadius="12px" 
            ),
            width="100%",
            background="linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/programming.png');",
            backgroundReapeat="no-repeat",
            backgroundSize="auto",
           paddingTop="1rem"
        ),
        width="100vw",
        height="100vh",
        gap="0"
    )



def profile() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Imagen de perfil", width="100%", textAlign="center"),
            rx.box(
                rx.image(src=rx.cond(userData.imgPhoto == "", "/profile.jpg", userData.imgPhoto), width="5rem", border_radius="100%"),
                rx.upload(
                    rx.button(rx.icon(tag="camera"),"Cambiar imagen de perfil", color_scheme="plum", variant="outline", marginTop="1rem"),
                    id="upload1",
                    accept = {"image/png": [".png"],"image/jpeg": [".jpg", ".jpeg"]},
                    on_drop=ImgState.handle_upload(rx.upload_files(upload_id="upload1"))
                ),
                rx.text("Para actualizar la foto de perfil, presione en 'Cambiar imagen de perfil' y suba su imagen. Para confirmar, presione en 'Actualizar datos.'", size="1", weight="light", margin="1rem 0"),
                rx.divider(margin="1rem 0"),
                rx.heading("Datos personales", size="4", width="100%", textAlign="center"),
                rx.callout(
                        "Las contraseñas no son las mismas. Intente nuevamente",
                        icon="triangle_alert",
                        color_scheme="red",
                        role="alert",
                        display=rx.cond(validatePassword.samePass == False, "block", "none")
                    ),
                rx.callout(
                    "Error al intentar actualizar el usuario. Intente nuevamente",
                    icon="triangle_alert",
                    color_scheme="red",
                    role="alert",
                    display=rx.cond(validatePassword.errorUpdate, "block", "none")
                ),
                rx.grid(
                    rx.heading("Nombre de usuario", size="3", weight="light"),
                    rx.input(
                        placeholder="Nombre de usuario",
                        name="name",
                        type="text",
                        value=userData.username,
                        on_change=userData.set_username
                    ),
                    rx.heading("Correo", size="3", weight="light"),
                    rx.input(
                        placeholder="Correo",
                        name="mail",
                        type="email",
                        value=userData.mail,
                        on_change=userData.set_mail
                    ),
                    rx.heading("Contraseña", size="3", weight="light"),
                    rx.input(
                        placeholder="contraseña",
                        name="password",
                        type="password",
                        value=userData.passwrd,
                        on_change=userData.set_passwrd
                    ),
                    rx.heading("Repetir contraseña", size="3", weight="light"),
                    rx.input(
                        placeholder="Repetir contraseña",
                        name="confirmPassword",
                        type="password",
                        value=userData.confirmPasswrd,
                        on_change=validatePassword.validatePass
                    ),
                    columns="2",
                    spacing="4",
                    width="100%",
                    padding="0 5rem",
                    margin="1rem 0"
                ),
                rx.button("Actualizar datos", color_scheme="plum", disabled=rx.cond(validatePassword.samePass, False, True), on_click=sumbitChange.updateUser),
                width="100%",
                display="flex",
                flexDirection="column",
                justifyContent="center",
                alignItems="center"  
            ),
            width="100%",
            margin="2rem 0"
        ),
        width="100%",
        height="100%",
        on_mount=userData.getUserData
    )

def posts() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Administración de Posts", width="100%", textAlign="center"),
            rx.divider(margin="1rem 0"),
            rx.box(
                addPost(),
                width="100%",
                display="flex",
                flexDirection="row",
                alignItems="center",
                justifyContent="center",
                margin="1rem 0"
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Id"),
                        rx.table.column_header_cell("Nombre del post"),
                        rx.table.column_header_cell("Categoria"),
                        rx.table.column_header_cell("Fecha"),
                        rx.table.column_header_cell("Acción")
                    ),
                ),
                rx.table.body(
                    rx.foreach(ManagePosts.postListTable, lambda post: ListPosts(post))
                ),
                width="100%"
            ),
            paddingTop="2rem"
        ),
        width="100%",
        on_mount= ManagePosts.getAllUserPost
    )

def ListPosts(post: userPostDTO) -> rx.Component:   
    return rx.table.row(
        rx.table.row_header_cell(post.postId),
        rx.table.cell(post.title),
        rx.table.cell(post.cat),
        rx.table.cell(post.posted_at),
        rx.table.cell(rx.stack(
            editPost(post.postId),
            deletePost(post.postId)
        ))
    )