import reflex as rx
from DevForum.Components.navbar import navbar
from DevForum.Components.addPost import addPost
from DevForum.Components.postCard import postCard
from DevForum.Backend.Controllers.PostController import getUserPost

class HandleRankPost(rx.State):
    async def loadPosts(self):
        post = await self.get_state(getUserPost)
        post.topCommentedPosts()

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.box(
                    rx.heading("Temas más comentados", size="4", weight="light", width="100%", textAlign="center"),
                    rx.divider(size="4"),
                    width="100%",
                    paddingTop="1rem"
                ),
                rx.box(
                    addPost(),
                    width="100%",
                    display="flex",
                    flexDirection="row",
                    justifyContent="center",
                    alignItems="center",
                    margin="1rem 0"
                ),
                rx.grid(
                    rx.foreach(
                        getUserPost.topPost,
                        lambda post: postCard(post),
                    ),
                    columns="2",
                    spacing="6",
                    width="100%",
                    margin="2rem 0",
                    padding="0 2rem"
                ),
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
        gap="0",
        width="100vw",
        height="100vh",
        on_mount=HandleRankPost.loadPosts   
    )

