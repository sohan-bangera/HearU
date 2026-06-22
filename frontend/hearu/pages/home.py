import reflex as rx
from hearu.state import State

# Color palette
BG = "#0F0F0F"
ACCENT = "#E8D5B0"
TEXT_PRIMARY = "#F5F5F5"
TEXT_SECONDARY = "#888888"


def home() -> rx.Component:
    return rx.box(
        rx.vstack(
            # Header
            rx.text(
                "HearU",
                font_size="14px",
                color=TEXT_SECONDARY,
                font_weight="500",
                letter_spacing="0.1em",
            ),

            # Tagline
            rx.text(
                "Speak freely. Listen anonymously.",
                font_size="16px",
                color=TEXT_SECONDARY,
                text_align="center",
            ),

            # Two main buttons
            rx.hstack(
                rx.button(
                    "🎙 Record",
                    on_click=rx.redirect("/record"),
                    background=ACCENT,
                    color=BG,
                    border_radius="4px",
                    padding="16px 32px",
                    font_weight="500",
                    font_size="16px",
                    cursor="pointer",
                    _hover={"opacity": "0.9"},
                ),
                rx.button(
                    "🎧 Listen",
                    on_click=rx.redirect("/listen"),
                    background=ACCENT,
                    color=BG,
                    border_radius="4px",
                    padding="16px 32px",
                    font_weight="500",
                    font_size="16px",
                    cursor="pointer",
                    _hover={"opacity": "0.9"},
                ),
                spacing="4",
            ),

            # Stats counter
            rx.text(
                State.total_voices.to_string() + " voices shared so far",
                font_size="13px",
                color=TEXT_SECONDARY,
            ),

            # Footer
            rx.text(
                "HearU — anonymous by design",
                font_size="12px",
                color=TEXT_SECONDARY,
                margin_top="48px",
            ),

            align="center",
            justify="center",
            height="100vh",
            spacing="6",
        ),
        background=BG,
        min_height="100vh",
        on_mount=[State.init_session, State.load_stats],
    )