import reflex as rx
from hearu.pages.home import home

app = rx.App(
    style={
        "font_family": "Inter, sans-serif",
        "background_color": "#0F0F0F",
    }
)

app.add_page(home, route="/")