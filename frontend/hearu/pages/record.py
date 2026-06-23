import reflex as rx
from hearu.state import State, CATEGORIES

BG = "#0F0F0F"
SURFACE = "#1A1A1A"
ACCENT = "#E8D5B0"
TEXT_PRIMARY = "#F5F5F5"
TEXT_SECONDARY = "#888888"
DANGER = "#C0392B"
SUCCESS = "#27AE60"


def category_picker(on_select) -> rx.Component:
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


def recorder_script() -> rx.Component:
    return rx.script("""
        let mediaRecorder = null;
        let audioChunks = [];
        let timerInterval = null;
        let seconds = 0;
        let isRecording = false;

        window._audioBase64 = null;

        function formatTime(s) {
            const m = Math.floor(s / 60).toString().padStart(2, '0');
            const sec = (s % 60).toString().padStart(2, '0');
            return m + ':' + sec;
        }

        function startTimer() {
            seconds = 0;
            if (timerInterval) clearInterval(timerInterval);
            timerInterval = setInterval(() => {
                seconds++;
                const display = document.getElementById('timer-display');
                if (display) display.textContent = formatTime(seconds);
                if (seconds >= 60) toggleRecording();
            }, 1000);
        }

        function stopTimer() {
            if (timerInterval) {
                clearInterval(timerInterval);
                timerInterval = null;
            }
        }

        async function toggleRecording() {
            if (!isRecording) {
                try {
                    audioChunks = [];
                    window._audioBase64 = null;

                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    mediaRecorder = new MediaRecorder(stream);

                    mediaRecorder.ondataavailable = e => {
                        if (e.data.size > 0) audioChunks.push(e.data);
                    };

                    mediaRecorder.onstop = () => {
                        stream.getTracks().forEach(t => t.stop());
                        const blob = new Blob(audioChunks, { type: 'audio/webm' });

                        // Show playback
                        const playback = document.getElementById('playback');
                        if (playback) {
                            playback.src = URL.createObjectURL(blob);
                            playback.style.display = 'block';
                        }

                        // Convert to base64
                        const reader = new FileReader();
                        reader.onloadend = () => {
                            window._audioBase64 = reader.result.split(',')[1];
                            console.log('Audio stored, length:', window._audioBase64.length);

                            // Show submit button
                            const submitBtn = document.getElementById('submit-btn');
                            if (submitBtn) submitBtn.style.display = 'inline-block';
                        };
                        reader.readAsDataURL(blob);

                        // Reset record button
                        const btn = document.getElementById('record-btn');
                        if (btn) {
                            btn.textContent = '🎙 Record Again';
                            btn.style.background = 'transparent';
                            btn.style.color = '#E8D5B0';
                            btn.style.border = '2px solid #E8D5B0';
                        }
                    };

                    mediaRecorder.start(100);
                    isRecording = true;
                    startTimer();

                    const btn = document.getElementById('record-btn');
                    if (btn) {
                        btn.textContent = '⏹ Stop';
                        btn.style.background = '#C0392B';
                        btn.style.color = 'white';
                        btn.style.border = 'none';
                    }

                } catch (err) {
                    console.error('Microphone error:', err);
                    alert('Could not access microphone. Please allow microphone access.');
                }

            } else {
                if (mediaRecorder && mediaRecorder.state !== 'inactive') {
                    mediaRecorder.stop();
                }
                stopTimer();
                isRecording = false;
            }
        }

        function setupRecorder() {
            const btn = document.getElementById('record-btn');
            if (btn && !btn._setup) {
                btn._setup = true;
                btn.onclick = toggleRecording;
            }
        }

        document.addEventListener('DOMContentLoaded', setupRecorder);
        setInterval(setupRecorder, 500);
    """)


def record_page() -> rx.Component:
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
                State.record_step == "category",
                rx.vstack(
                    rx.text(
                        "What are you sharing?",
                        font_size="22px",
                        font_weight="600",
                        color=TEXT_PRIMARY,
                    ),
                    category_picker(State.select_record_category),
                    spacing="6",
                    align="start",
                ),
            ),

            # Step 2 — Recording UI
            rx.cond(
                State.record_step == "review",
                rx.vstack(
                    # Selected category label
                    rx.text(
                        State.selected_category,
                        font_size="13px",
                        color=TEXT_SECONDARY,
                    ),

                    # Record button
                    rx.el.button(
                        "🎙 Start Recording",
                        id="record-btn",
                        style={
                            "width": "160px",
                            "height": "160px",
                            "border_radius": "50%",
                            "background": "transparent",
                            "border": f"2px solid {ACCENT}",
                            "color": ACCENT,
                            "font_size": "14px",
                            "cursor": "pointer",
                            "font_family": "Inter, sans-serif",
                        }
                    ),

                    # Timer
                    rx.el.p(
                        "00:00",
                        id="timer-display",
                        style={
                            "color": TEXT_SECONDARY,
                            "font_size": "14px",
                            "margin": "0",
                        }
                    ),

                    # Playback
                    rx.el.audio(
                        id="playback",
                        controls=True,
                        style={
                            "width": "100%",
                            "display": "none",
                            "margin_top": "8px",
                        }
                    ),

                    # Submit button — Reflex button with on_click
                    rx.button(
                        "Submit",
                        id="submit-btn",
                        on_click=State.handle_submit_click,
                        display="none",
                        background=ACCENT,
                        color=BG,
                        border_radius="4px",
                        padding="10px 24px",
                        cursor="pointer",
                        font_family="Inter, sans-serif",
                        font_size="14px",
                    ),

                    # Back button
                    rx.button(
                        "← Back",
                        on_click=State.reset_record,
                        background="transparent",
                        border="1px solid #2A2A2A",
                        color=TEXT_SECONDARY,
                        border_radius="4px",
                        padding="10px 20px",
                        cursor="pointer",
                        margin_top="8px",
                    ),

                    spacing="4",
                    align="center",
                ),
            ),

            # Step 3 — Submitting
            rx.cond(
                State.record_step == "submitting",
                rx.text(
                    "Checking your audio...",
                    color=TEXT_SECONDARY,
                    font_size="16px",
                ),
            ),

            # Step 4a — Done
            rx.cond(
                State.record_step == "done",
                rx.vstack(
                    rx.text("✓", color=SUCCESS, font_size="32px"),
                    rx.text(
                        "Your voice has been added.",
                        color=TEXT_PRIMARY,
                        font_size="18px",
                    ),
                    rx.button(
                        "Go Home",
                        on_click=rx.redirect("/"),
                        background=ACCENT,
                        color=BG,
                        border_radius="4px",
                        padding="10px 24px",
                        cursor="pointer",
                    ),
                    spacing="4",
                    align="center",
                ),
            ),

            # Step 4b — Flagged
            rx.cond(
                State.record_step == "flagged",
                rx.vstack(
                    rx.text(
                        "This audio contains inappropriate content and cannot be submitted.",
                        color=DANGER,
                        font_size="16px",
                    ),
                    rx.button(
                        "Try Again",
                        on_click=State.reset_record,
                        background="transparent",
                        border=f"1px solid {DANGER}",
                        color=DANGER,
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
        recorder_script(),
        background=BG,
        min_height="100vh",
        on_mount=State.init_session,
    )