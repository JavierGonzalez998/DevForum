import reflex as rx
from DevForum.Components.navbar import navbar
from DevForum.Components.carousel import Carousel
from datetime import datetime
from DevForum.Components.footer import Footer

def getBirthday():
    current_year = datetime.now().year
    return current_year - 1998

def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.center(
            rx.video(url="/IndexVideo.mp4", width="100vw", height="100vh", filter="brightness(50%)", playing=True, loop=True,controls=False),
            rx.vstack(
                rx.heading("Bienvenid@ a DevForum!", size="9"),
                rx.heading("Un foro donde podrás compartir tus dudas y consultas a la comunidad de desarrolladores", weight="regular"),
                width="100%",
                height="100%",
                position="absolute",
                top="0",
                left="0",
                right="0",
                display="flex",
                flexDirection="column",
                justifyContent="center",
                alignItems="center",
                color="white"
            ),
            width="100vw",
            height="100vh",
            position="relative"
        ),
        rx.container(
            rx.hstack(
                rx.box(
                    rx.image(src="/aboutImage.jpg", width="100%", objectFit="cover"),
                    width="100rem"
                ),
                rx.vstack(
                    rx.heading("¿Qué es DevForum?", size="4", weight="bold"),
                    rx.heading("DevForum es un foro público en donde los desarrolladores podrán consultar sus dudas y consultas respecto a sus códigos y la comunidad podrá responder, aconsejar y también podrán puntuar las mejores respuestas.", size="3", weight="regular"),
                    rx.heading("Hecho por devs para devs ♥!", size="3", weight="bold"),
                    rx.button("Ir al foro", size="4", color_scheme="plum", on_click=rx.redirect("/forum")),
                    gap="2rem"
                ),
                gap="5em",              
            ),
            rx.vstack(
                rx.heading("Los temas más comentados:", width="100%", textAlign="center"),
                rx.box(
                    Carousel(),
                    width="100%",                 
                ),
                marginTop="5rem",
            ),
            rx.hstack(
                rx.vstack(
                    rx.heading("Acerca de mi", size="4", weight="bold"),
                    rx.heading(f"Mi nombre es Javier González (Javito para los amigos). tengo {getBirthday()} años. Actualmente vivo en Iquique, Chile. Soy Analista Programador titulado en INACAP y soy muy entusiasta por la tecnología y el desarrollo. Me gustan los videojuegos y tocar guitarra.", size="3", weight="regular"),
                    rx.button("Ir a mi portfolio (está un poco desactualizado 😅)", on_click=rx.redirect("https://javier-gonzalez.me/", external=True), color_scheme="plum"),
                    gap="2rem"
                ),
                rx.box(
                    rx.image(src="/aboutMe.jpg", width="100%", objectFit="cover"),
                    width="25rem"
                ),
                gap="5em",
                marginTop="3rem"              
            ),
            font_size="2em",
            marginTop="1rem"             
        ),
        Footer(),
        height="100vh",
        overflow="scroll",
        overflowX="hidden",
        backgroundColor="#FEFAF6"
    )

