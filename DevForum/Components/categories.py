import reflex as rx
from DevForum.Backend.Controllers.CategoryController import BackendCategory
from DevForum.Components.addCat import addCat
from DevForum.Backend.Models.Category import Category

class HandleCat(rx.State):
    async def loadCat(self):
        aux = await self.get_state(BackendCategory)
        await aux.getAllCat()

def cat() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.heading("Administración de Categorias", width="100%", textAlign="center"),
            rx.divider(margin="1rem 0"),
            rx.box(
                addCat(),
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
                    rx.foreach(BackendCategory.listAllCat, ListPosts)
                ),
                width="100%"
            ),
            paddingTop="2rem"
        ),
        width="100%",
        on_mount= lambda: HandleCat.loadCat()
    )

def ListPosts(cat: Category):
    return rx.table.row(
        rx.table.row_header_cell(cat.catId),
        rx.table.cell(cat.name),
        rx.table.cell(rx.stack(
        )),
    )