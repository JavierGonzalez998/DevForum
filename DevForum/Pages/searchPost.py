import reflex as rx
from DevForum.Components.navbar import navbar
from DevForum.Backend.Controllers.PostController import getUserPost
from DevForum.Backend.DTO.UserPostDTO import userPostDTO

class HandlePostState(rx.State):
    link: str
    formattedLink:str

    def getItemLink(self):
        link = self.router.page.params.get("text", "")
        self.link = link
        self.formattedLink = link[0].upper() + link[1:]

    async def getSearch(self):
        post = await self.get_state(getUserPost)
        post.getPostByName(self.link)

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.box(
                    rx.heading(HandlePostState.formattedLink, size="4", weight="light", width="100%", textAlign="center"),
                    rx.divider(size="4"),
                    width="100%",
                    paddingTop="1rem"
                ),
                rx.grid(
                    rx.foreach(getUserPost.userPosts, lambda post: postCard(post)),
                    width="100%",
                    height="100%",
                    overflowY="scroll",
                    justifyContent="center",
                    paddingLeft="2rem"
                ),
                boxShadow="rgba(0, 0, 0, 0.24) 0px 3px 8px",
                height="50rem",
                backgroundColor="white",
                borderRadius="12px"
            ),
            width="100%",
            background="linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url('/programming.png');",
            backgroundReapeat="no-repeat",
            backgroundSize="auto",
           paddingTop="1rem"
        ),
        on_mount=[HandlePostState.getItemLink, lambda: HandlePostState.getSearch()],
        gap="0",
        height="100vh",   
    )


def postCard(post:userPostDTO) -> rx.Component:
    return rx.card(
    rx.link(
        rx.flex(
            rx.box(
                rx.heading(post.title),
                rx.text(
                    post.desc
                ),
                    rx.text("Categoría: " + post.cat,
                    alignSelf="end"
                ),
                spacing="2",
                color="black"
            ),
            height="100%"
        ),
        as_child=True,
    ),
    width="50%",
    height="10rem",
    on_click=rx.redirect(f"/post/{post.postId}")
)