import reflex as rx
from typing import List
from DevForum.Backend.Controllers.UserController import userData
from DevForum.States.UserCookies import userCookie
from DevForum.Components.searchBar import SearchBar
from typing import Dict
class NavbarLink(rx.State):
    links_list: Dict[str, str] = {
        "foro": "/forum",
        "categorias": "/categories"
    }

class UserCookieState(rx.State):
    token: str

    async def LoadCookie(self):
        auth = await self.get_state(userCookie)
        self.token = auth.getAuthCookie()

    async def Logout(self):
        user = await self.get_state(userData)
        await user.Logout()
        return rx.redirect("/login")

class getUser(rx.State):
    username: str
    imgPhoto: str

    async def LoadData(self):
        user =  await self.get_state(userData)
        await user.getUserData()
        self.set_username(user.username)
        self.set_imgPhoto(user.imgPhoto)
    

def display_color(link: List):
    return rx.box(rx.text(link[0], on_click=rx.redirect(link[1]), size="5", weight="regular"), cursor="pointer", )


def navbar() -> rx.Component:
    return rx.box(
        rx.center(
            rx.image(src="/grid.svg",width="7em", alt="logo"),
            display="flex",
            flexDirection="column",
            justifyContent="center",
            alignItems="center",
            height="100%",
            alignSelf="start",
            on_click=rx.redirect("/"),
            cursor="pointer"
        ),
        rx.hstack(
             rx.foreach(NavbarLink.links_list, display_color),
            gap="4rem"
        ),
        SearchBar(),
        rx.cond(
            UserCookieState.token != "",
            profileInfo(),
            None
        ),
        rx.button(
            rx.icon(tag="user"),
            rx.cond(UserCookieState.token == "", "Iniciar sesion", "Mi Perfil"),
            on_click=rx.redirect(rx.cond(UserCookieState.token == "", "/login", "/profile")),
            color_scheme="plum"
        ),
        rx.cond(
            UserCookieState.token != "",
            rx.button(
                rx.icon("log-out"),
                "Cerrar sesión",
                on_click= UserCookieState.Logout(),
                color_scheme="red"
            ),
            None
        ),
        width="100%",
        height="5rem",
        backgroundColor="#f3f3f3",
        position="sticky",
        top="0",
        border="1px solid #e4e4e4",
        boxShadow= "rgba(0, 0, 0, 0.24) 0px 3px 8px",
        display="flex",
        flexDirection="row",
        justifyContent="space-around",
        alignItems="center",
        zIndex="300",
        on_mount=lambda:UserCookieState.LoadCookie()
    )


def profileInfo():

    return rx.hstack(
        rx.image(src=rx.cond(getUser.imgPhoto == "", "/profile.jpg", getUser.imgPhoto), width="3rem", border_radius="100%"),
        rx.text(getUser.username, size="2", weight="light"),
        on_mount=lambda: getUser.LoadData(),
        width="5rem",
        gap="1rem",
        align="center"
    )