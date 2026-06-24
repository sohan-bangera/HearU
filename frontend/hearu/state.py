import reflex as rx
import uuid
from hearu import api

CATEGORIES = ["Confession", "Rant", "Story", "Advice", "Random"]

class State(rx.State):

    # --- Session ---
    session_token: str = ""

    # --- Home Page ---
    total_voices: int = 0

    # --- Record Page ---
    record_step: str = "category"
    selected_category: str = ""
    record_status: str = ""
    record_message: str = ""
    audio_data: str = ""

    # --- Listen Page ---
    listen_step: str = "category"
    listen_category: str = ""
    current_audio_url: str = ""
    current_audio_id: str = ""
    current_audio_category: str = ""

    def init_session(self):
        if not self.session_token:
            self.session_token = str(uuid.uuid4())

    async def load_stats(self):
        data = await api.get_stats()
        self.total_voices = data.get("total_voices", 0)

    def select_record_category(self, category: str):
        self.selected_category = category
        self.record_step = "review"

    def select_listen_category(self, category: str):
        self.listen_category = category

    async def select_category_and_fetch(self, category: str):
        """Select Category and fetch audio in one event"""
        self.listen_category = category
        await self.fetch_random_audio()

    def set_audio_data(self, data: str):
        self.audio_data = data

    async def handle_submit_click(self):
        """Gets audio data from JS then submits."""
        return rx.call_script(
            "window._audioBase64 || ''",
            callback=State.submit_audio
        )

    async def submit_audio(self, audio_data: str):
        import base64

        if not audio_data:
            print("No audio data received")
            return

        self.record_step = "submitting"
        yield

        audio_bytes = base64.b64decode(audio_data)

        result = await api.upload_audio(
            audio_bytes,
            self.selected_category,
            self.session_token
        )

        if result.get("status") == "approved":
            self.record_step = "done"
        else:
            self.record_step = "flagged"

        self.audio_data = ""

    async def fetch_random_audio(self):
        data = await api.get_random_audio(
            self.listen_category,
            self.session_token
        )
        if data is None:
            self.listen_step = "empty"
        else:
            self.current_audio_url = data["audio_url"]
            self.current_audio_id = data["audio_id"]
            self.current_audio_category = data["category"]
            self.listen_step = "listening"

    async def mark_and_next(self):
        await api.mark_heard(self.current_audio_id, self.session_token)
        await self.fetch_random_audio()

    def reset_record(self):
        self.record_step = "category"
        self.selected_category = ""
        self.record_status = ""
        self.record_message = ""
        self.audio_data = ""

    def reset_listen(self):
        self.listen_step = "category"
        self.listen_category = ""
        self.current_audio_url = ""
        self.current_audio_id = ""