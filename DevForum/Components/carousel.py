import reflex as rx
from DevForum.Backend.Controllers.PostController import getUserPost
from DevForum.Backend.DTO.PostDetailDTO import DTORankPost

class handlePostIndex(rx.State):
    async def loadPosts(self):
        post = await self.get_state(getUserPost)
        post.topCommentedPosts()


def Carousel() -> rx.Component:
    return rx.center(
        rx.grid(
            rx.foreach(getUserPost.topPost, lambda post: Post(post)),
            on_mount=handlePostIndex.loadPosts,
            gap="1rem",
            columns="5",
            spacing="2",
            width="100%",
        ),
    )

def Post(post: DTORankPost) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.text(post.title, size="2", weight="bold"),
            rx.text(post.desc, size="1", weight="light"),
            rx.text(f"comentarios: {post.comments}", size="1", weight="light"),
            rx.button("Ir al post", on_click=rx.redirect(f"/post/{post.postId}"), size="1", color_scheme="plum"),
            gap="1rem"            
        ),
        size="1"
    )