import reflex as rx
from DevForum.Components.navbar import navbar
from DevForum.Backend.Controllers.CategoryController import BackendCategory
from DevForum.Backend.DTO.CategoryDTO import CategoryWithPost
from DevForum.Components.catCard import catCard
from typing import List
class HandleCategory(rx.State):
    listCat: List[CategoryWithPost]

    async def loadCat(self):
        cat = await self.get_state(BackendCategory)
        cat.getAllCatWithPosts()
        self.listCat = cat.catWithPosts

def index() -> rx.Component:
    return rx.vstack(
        navbar(),
        rx.container(
            rx.vstack(
                rx.box(
                    rx.heading("Categorías", size="4", weight="light", width="100%", textAlign="center"),
                    rx.divider(size="4"),
                    width="100%",
                    paddingTop="1rem"
                ),
                rx.grid(
                    rx.foreach(
                        HandleCategory.listCat,
                        lambda post: catCard(post) ,
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
        on_mount=lambda: HandleCategory.loadCat(),
        gap="0",
        height="100vh",   
    )