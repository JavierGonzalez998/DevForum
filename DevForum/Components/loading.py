import reflex as rx

def Loading(display: bool) -> rx.Component:
    return rx.box(
        rx.html('''<div class="spinner-box">
  <div class="circle-border">
    <div class="circle-core"></div>
  </div>  
</div>'''),
        class_name="loading",
        width="100vw",
        height="100vh",
        flexDirection="column",
        justifyContent="center",
        alignItems="center",
        background="linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), transparent",
        zIndex="1000",
        display=rx.cond(display, "flex", "none"),
        position="absolute",
        top="0"
    )