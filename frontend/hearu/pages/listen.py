import reflex as rx
from hearu.state import State, CATEGORIES

BG = "#0F0F0F"
ACCENT = "#E8D5B0"
TEXT_PRIMARY = "#F5F5F5"
TEXT_SECONDARY = "#888888"


def category_picker_listen(on_select) -> rx.Component:
    return rx.vstack(
        rx.foreach(
            CATEGORIES,
            lambda cat: rx.text(
                cat,
                color=TEXT_SECONDARY,
                font_size="18px",
                font_weight="500",
                cursor="pointer",
                _hover={"color": TEXT_PRIMARY, "text_decoration": "underline"},
                on_click=on_select(cat),
            ),
        ),
        spacing="4",
        align="start",
    )


def listen_page() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Back button
            rx.text(
                "← Back",
                color=TEXT_SECONDARY,
                cursor="pointer",
                font_size="14px",
                on_click=rx.redirect("/"),
                _hover={"color": TEXT_PRIMARY},
            ),

            # Step 1 — Category
            rx.cond(
                State.listen_step == "category",
                rx.vstack(
                    rx.text(
                        "What do you want to hear?",
                        font_size="22px",
                        font_weight="600",
                        color=TEXT_PRIMARY,
                    ),
                    category_picker_listen(State.select_category_and_fetch),
                    spacing="6",
                    align="start",
                ),
            ),

            # Step 2 — Listening
            rx.cond(
                State.listen_step == "listening",
                rx.vstack(
                    rx.text(
                        State.current_audio_category,
                        font_size="13px",
                        color=TEXT_SECONDARY,
                    ),
                    rx.audio(
                        url=State.current_audio_url,
                        width="100%",
                        playing=True,
                    ),
                    rx.hstack(
                        rx.button(
                            "Skip",
                            on_click=State.mark_and_next,
                            background="transparent",
                            border="1px solid #2A2A2A",
                            color=TEXT_SECONDARY,
                            border_radius="4px",
                            padding="10px 24px",
                            cursor="pointer",
                        ),
                        rx.button(
                            "Next Voice",
                            on_click=State.mark_and_next,
                            background=ACCENT,
                            color=BG,
                            border_radius="4px",
                            padding="10px 24px",
                            cursor="pointer",
                        ),
                        spacing="4",
                    ),
                    spacing="4",
                    align="start",
                ),
            ),

            # Step 3 — Empty
            rx.cond(
                State.listen_step == "empty",
                rx.vstack(
                    rx.text(
                        "You've heard all voices in this category.",
                        color=TEXT_PRIMARY,
                        font_size="18px",
                    ),
                    rx.text(
                        "Check back later.",
                        color=TEXT_SECONDARY,
                        font_size="14px",
                    ),
                    rx.button(
                        "Pick another category",
                        on_click=State.reset_listen,
                        background="transparent",
                        border="1px solid #2A2A2A",
                        color=TEXT_SECONDARY,
                        border_radius="4px",
                        padding="10px 24px",
                        cursor="pointer",
                    ),
                    spacing="4",
                    align="start",
                ),
            ),

            spacing="8",
            align="start",
            max_width="560px",
            margin="0 auto",
            padding="48px 24px",
        ),
        background=BG,
        min_height="100vh",
        on_mount=State.init_session,
    )