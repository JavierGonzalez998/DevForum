import reflex as rx
from DevForum.Backend.DTO.CategoryDTO import CategoryWithPost
def catCard(post: CategoryWithPost) -> rx.Component:
    return rx.card(
        rx.link(
            rx.flex(
                rx.avatar(src="/reflex_banner.png"),
                rx.box(
                    rx.heading(post.name),
                    rx.text(
                        f"N° Post: {post.nPost}"
                    ),
                    color="black"
                ),
                spacing="2",
            ),
            on_click=rx.redirect(f"/categories/{post.name.lower( )}")
        ),
        as_child=True,
    )  