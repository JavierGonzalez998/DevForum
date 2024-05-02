import reflex as rx

class Toastify(rx.Component):
    """Spline component."""

    library = "toastify-js"
    tag = "Toastify"
    text: rx.Var[str]
    duration: rx.Var[int]
    is_default = True

toastify = Toastify.create

