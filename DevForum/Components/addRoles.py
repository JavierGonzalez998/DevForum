import reflex as rx
from DevForum.Backend.Controllers.RolesController import Roles

class addRolesClass(rx.State):
    async def handleAddRole(self):
        add = await self.get_state(Roles)
        response = await add.addRoles()
        if response:
            return rx.redirect("/forum")
        
def addRole() -> rx.Component:
    return rx.dialog.root(
            rx.dialog.trigger(rx.button(rx.icon("plus"), "Agregar Rol", color_scheme="plum", variant="outline")),
            rx.dialog.content(
                rx.dialog.title("Agregar Rol"),
                rx.dialog.description(
                    "Para agregar un rol, complete los siguientes campos",
                    margin="1rem 0"
                ),
                rx.flex(
                    rx.text(
                        "Nombre del rol",
                        as_="div",
                        size="2",
                        margin_bottom="4px",
                        weight="bold"
                    ),
                    rx.input(
                        placeholder="Ingresa un nombre del rol",
                        color_scheme="plum", variant="soft", radius="full",
                        value=Roles.name,
                        on_change=Roles.set_name
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
                        rx.button("Save", color_scheme="plum", on_click=addRolesClass.handleAddRole),
                    ),
                    spacing="3",
                    margin_top="16px",
                    justify="end",
                ),
            ),
        )