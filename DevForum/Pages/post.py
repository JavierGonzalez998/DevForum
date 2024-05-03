import reflex as rx
from DevForum.Components.navbar import navbar
from DevForum.Backend.Controllers.PostController import getUserPost
from DevForum.Backend.Controllers.UserController import userData
from DevForum.Backend.Controllers.CommentController import BackendComment
from DevForum.Backend.DTO.CommentDTO import CommentDTO
from DevForum.States.UserCookies import userCookie
from typing import List
import asyncio

class HandlePost(rx.State):
    urlVar: str

    def getItemLinkPost(self):
        link = self.router.page.params.get("id", "")
        self.urlVar = link

    async def getDetailPost(self):
        post = await self.get_state(getUserPost)
        await post.getPostDetail(self.urlVar)

class HandleUser(rx.State):
    async def loadUserData(self):
        user = await self.get_state(userData)
        await user.getUserData()

class HandleComments(rx.State):
    validateEmptyComment: bool = False
    listOfComment: List[CommentDTO] = []
    successCommented: bool = False

    async def loadComments(self):
        comm = await self.get_state(BackendComment)
        post = await self.get_state(HandlePost)
        comm.loadCommentPosts(post.urlVar)
        self.listOfComment = comm.ListOfComment

    async def submitComment(self):
        comm = await self.get_state(BackendComment)
        post = await self.get_state(HandlePost)
        if comm.comment == "":
            self.validateEmptyComment = True
        else:
            self.validateEmptyComment = False
            result = await comm.submitComment(post.urlVar)
            if result == True:
                self.successCommented = True
                comm.loadCommentPosts(post.urlVar)
   
def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.vstack(
            rx.vstack(
                rx.heading("Publicación", size="4", weight="light", width="100%", textAlign="center", marginTop="1rem"),
                rx.divider(margin="1rem 0"),
                rx.heading(getUserPost.detailPost.title, size="6", weight="bold", width="100%", textAlign="center"),
                rx.text(getUserPost.detailPost.desc, size="4", weight="light", width="100%", textAlign="center"),
                rx.vstack(
                    rx.text(f"Escrito por: {getUserPost.detailPost.username}", width="100%",textAlign="center"),
                    rx.text(f"Fecha de publicación: {getUserPost.detailPost.posted_at}",paddingLeft="3rem"),
                    rx.text(f"Fecha de modificación: {getUserPost.detailPost.updated_at}",paddingLeft="3rem"),
                    width="100%"
                ),
                rx.box(
                    rx.text(getUserPost.detailPost.content),
                    width="100%",
                    height="100%",
                    padding="1rem 5rem" 
                ),
                width='80%',
                boxShadow="rgba(0, 0, 0, 0.24) 0px 3px 8px",
                backgroundColor="white",
                borderRadius="12px", 
                height="100vh",
                overflowY="scroll"
            ),
            rx.vstack(
                rx.heading("Comentarios", size="3", weight="light", width="100%", textAlign="center", marginTop="1rem"),
                rx.divider(),
                rx.cond(userCookie.auth_token != "", userCommentSection(), noLoginComment()),
                rx.divider(),
                rx.cond(BackendComment.count > 0, 
                rx.foreach(
                    HandleComments.listOfComment, lambda comment: commentSection(comment)
                ), noComment()),
                width='80%',
                gap="2rem",
                boxShadow="rgba(0, 0, 0, 0.24) 0px 3px 8px",
                backgroundColor="white",
                borderRadius="12px", 
                height="50%",
                overflowY="scroll"
            ),
            width="100%",
            height="100%",
           paddingTop="1rem",
           align="center"
        ),
        gap="0",
        background="linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/programming.png');",
        backgroundSize="auto",
        height="100vh",
        on_mount=[lambda: HandlePost.getItemLinkPost(), lambda: HandlePost.getDetailPost(), lambda: HandleComments.loadComments()]   
    )

def userCommentSection() -> rx.Component:
    return rx.hstack(
        rx.box(
            rx.image(src=rx.cond(userData.imgPhoto == "", "./profile.jpg", userData.imgPhoto), width="100%", height="100%"),
            width="3rem",
            objectFit="cover",
            borderRadius="100%",
            border="1px solid black"
        ),
        rx.vstack(
            rx.input.root(
                rx.input(
                    placeholder="Inserte su comentario",
                    size="3",
                    borderRadius="12px",
                    value=BackendComment.comment,
                    on_change=BackendComment.set_comment
                ),
                width="90%"   
            ),
            rx.cond(HandleComments.validateEmptyComment, rx.text("Ingrese su comentario antes de enviar", size="1", weight="light", color_scheme="red"), None),
            rx.cond(HandleComments.successCommented,rx.callout("Comentario ingresado correctamente. Por favor, recargue la página para visualizar su comentario",icon="mail-check", color_scheme="green", role="alert",), None),
            width="50%",
            height="2rem",
            alignItems="center"
        ),
        rx.button("Enviar Comentario", size="3", color_scheme="plum", on_click=lambda: HandleComments.submitComment()),
        gap="0.5rem",
        justify="center",
        align="center",
        on_mount=HandleUser.loadUserData,
        width="100%"
    )
def noLoginComment() -> rx.Component:
    return rx.hstack(
        rx.heading("Si desea ser parte de esta conversación. Por favor, inicie sesión", size="3", weight="light"),
        rx.button("Iniciar sesión", size="3", on_click=rx.redirect("/login"), color_scheme="plum"),
        width="100%",
        gap="1rem",
        justify="center",
        align="center",
    )

def commentSection(comment: CommentDTO) -> rx.Component:
    return rx.hstack(
        rx.vstack(
            rx.box(
                rx.image(src=rx.cond(comment.imgProfile == "", "./profile.jpg", comment.imgProfile), width="100%", height="100%"),
                width="3rem",
                objectFit="cover",
                borderRadius="100%",
                border="1px solid black",
            ),
            rx.text(comment.username, size="1", weight="light"),
            align="center",
            justify="center"
        ),
        rx.box(
            rx.text(comment.comment, size="2", width="100%",alignSelf="center", justifySelf="center", padding="0 0.5rem"),
            rx.text(comment.date, size="1"),
            display="flex",
            flexDirection="column",
            alignItems="flex-start",
            justifyContent="flex-start",
            backgroundColor="#e4e4e4",
            boxShadow="rgba(0, 0, 0, 0.24) 0px 3px 8px",
            borderRadius="8px"
        ),
        width="100%",
        height="6rem",
        align="center",
        gap="1rem",
        marginLeft="3rem"
    )

def noComment() -> rx.Component:
    return rx.box(
        rx.text("Aún no hay comentarios en la publicacíon. Anímate y únete a la conversación ♥"),
        width="100%",
        height="100%",
        display="flex",
        flexDirection="column",
        justifyContent="center",
        alignItems="center"
    )