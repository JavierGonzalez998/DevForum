import reflex as rx

class ReactCarousel(rx.Component):
    """Spline component."""

    library = "react-responsive-carousel"
    tag = "Carousel"
    children = rx.Component
    is_default = True
    lib_dependencies: list[str] = ["classnames", "prop-types", "react-easy-swipe"]

carousel = ReactCarousel.create

