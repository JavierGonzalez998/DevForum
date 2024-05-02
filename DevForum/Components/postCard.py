import reflex as rx
from DevForum.Backend.DTO.PostDetailDTO import DTORankPost


def postCard(post: DTORankPost) -> rx.Component:
    return rx.card(
        rx.link(
            rx.flex(
                rx.vstack(
                    rx.heading(post.title),
                    rx.text(f"Posteado por: {post.username}", size="2", weight="light"),
                    rx.text(post.desc, size="1", weight="light"),
                    rx.text(f"Categoría: {post.cat}", size="1", weight="light"),
                    rx.text(f"Creado el: {post.posted_at}"),
                    rx.text(
                        f"Comentarios: {post.comments}", weight="bold", width="100%", textAlign="center"
                    ),
                    gap="1rem",
                    color="black"
                ),
                spacing="2",
            ),
            on_click=rx.redirect(f"/post/{post.postId}")
        ),
        as_child=True,
    )  