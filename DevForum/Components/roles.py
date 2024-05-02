import reflex as rx
from DevForum.Backend.Controllers.RolesController import Roles
from DevForum.Components.addRoles import addRole
from DevForum.Backend.Models.Role import Role as model

class HandleRoles(rx.State):
    async def loadRoles(self):
        aux = await self.get_state(Roles)
        await aux.getAllRoles()

def roles() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Administración de Roles", width="100%", textAlign="center"),
            rx.divider(margin="1rem 0"),
            rx.box(
                addRole(),
                width="100%",
                display="flex",
                flexDirection="row",
                alignItems="center",
                justifyContent="center",
                margin="1rem 0"
            ),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Id"),
                        rx.table.column_header_cell("Nombre del rol"),
                        rx.table.column_header_cell("Acción")
                    ),
                ),
                rx.table.body(
                    rx.foreach(Roles.listRoles, ListPosts)
                ),
                width="100%"
            ),
            paddingTop="2rem"
        ),
        width="100%",
        on_mount= HandleRoles.loadRoles
    )

def ListPosts(role: model):
    return rx.table.row(
        rx.table.row_header_cell(role.roleId),
        rx.table.cell(role.name),
        rx.table.cell(rx.stack(
        )),
    )