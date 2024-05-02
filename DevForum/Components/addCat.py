import reflex as rx
from DevForum.Backend.Controllers.CategoryController import BackendCategory

class addCategoriesClass(rx.State):
    async def handleAddCat(self):
        add = await self.get_state(BackendCategory)
        response = await add.addCat()
        if response:
            return rx.redirect("/forum")
        
def addCat() -> rx.Component:
    return rx.dialog.root(
            rx.dialog.trigger(rx.button(rx.icon("plus"), "Agregar Categoría", color_scheme="plum", variant="outline")),
            rx.dialog.content(
                rx.dialog.title("Agregar Categoría"),
                rx.dialog.description(
                    "Para agregar una categoría, complete los siguientes campos",
                    margin="1rem 0"
                ),
                rx.flex(
                    rx.text(
                        "Nombre de la categoría",
                        as_="div",
                        size="2",
                        margin_bottom="4px",
                        weight="bold"
                    ),
                    rx.input(
                        placeholder="Ingresa un nombre de categoría",
                        color_scheme="plum", variant="soft", radius="full",
                        value=BackendCategory.name,
                        on_change=BackendCategory.set_name
                    ),
                    direction="column",
                    spacing="3",    
                ),
                rx.flex(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            color_scheme="gray",
                            variant="soft",
                        ),
                    ),
                    rx.dialog.close(
                        rx.button("Save", color_scheme="plum", on_click=addCategoriesClass.handleAddCat),
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
            ),
        )