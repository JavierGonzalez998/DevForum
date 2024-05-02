import reflex as rx
from DevForum.Components.navbar import NavbarLink
from typing import List
from DevForum.Components.searchBar import SearchBar
def Footer() -> rx.Component:
    return rx.box(
        rx.center(
            rx.hstack(
                rx.vstack(
                    rx.box(
                        rx.image(src="/grid.svg", width="100%"),
                        width="10rem"
                    ),
                    rx.text("hecho por devs para devs ♥", size="1", weight="light"),
                    rx.divider(),
                    rx.vstack(
                        rx.foreach(NavbarLink.links_list, Item)
                    ),
                    align="center",
                    justify="center"
                ),
                SearchBar(),
                gap="25rem",
                height="15rem"
            ),
        ),
        color="white",
        width="100%",
        height="30%",
        position="relative",
        marginTop="3rem",
        paddingTop="1rem",
        backgroundColor="#5C5959",
        bottom="0",
        zIndex="10000"
    )

def Item(link: List):
    return rx.box(rx.text(link[0], on_click=rx.redirect(link[1]), size="3", weight="light"), cursor="pointer", )
