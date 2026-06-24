import reflex as rx
from hearu.pages.home import home
from hearu.pages.record import record_page
from hearu.pages.listen import listen_page

app = rx.App(
    style={
        "font_family": "Inter, sans-serif",
        "background_color": "#0F0F0F",
    }
)

app.add_page(home, route="/")
app.add_page(record_page, route="/record")
app.add_page(listen_page, route="/listen")