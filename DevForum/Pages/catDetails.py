import reflex as rx
from DevForum.Components.navbar import navbar
from DevForum.Backend.Controllers.CategoryController import BackendCategory
from DevForum.Backend.Controllers.PostController import getUserPost, userPostDTO
from DevForum.Backend.DTO.CategoryDTO import CategoryWithPost
from DevForum.Backend.Models.Post import Post
from DevForum.Components.catCard import catCard
from typing import List

class HandleCategoryState(rx.State):
    listCat: List[CategoryWithPost]
    postList: List[userPostDTO]
    link: str
    async def loadCat(self):
        cat = await self.get_state(BackendCategory)
        cat.getAllCatWithPosts()
        self.listCat = cat.catWithPosts
    
    def getItemLink(self):
        link = self.router.page.params.get("detail", "")
        self.link = link[0].upper() + link[1:]

    async def loadPosts(self):
        post = await self.get_state(getUserPost)
        post.cat = self.link
        post.getPostByCat()
        self.listCat = post.userPosts

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.box(
                    rx.heading(HandleCategoryState.link, size="4", weight="light", width="100%", textAlign="center"),
                    rx.divider(size="4"),
                    width="100%",
                    paddingTop="1rem"
                ),
                rx.vstack(
                    rx.text(f"Aquí encontrarás todo lo relacionado a {HandleCategoryState.link}", width="100%", textAlign="center"),
                    rx.heading("Posts", size="7", weight="light", paddingLeft="2rem"),
                    rx.divider(),
                    gap="2rem",
                    width="100%"
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
        on_mount=[HandleCategoryState.loadCat, HandleCategoryState.getItemLink, HandleCategoryState.loadPosts],
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