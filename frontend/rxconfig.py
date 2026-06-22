import reflex as rx

config = rx.Config(
    app_name="hearu",
    backend_port=8001,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)