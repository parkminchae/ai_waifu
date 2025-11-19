import queue
import threading

import customtkinter as ctk

from scripts.gpt import conf
from scripts.live2d import live2d_frame
from scripts.tts import save_tts


class App(ctk.CTk):
    def __init__(self, callback):
        super().__init__()
        self.message_callback = callback
        self.bot_name = conf["bot_name"]
        self.theme = "Dark"

        self.setup_window()
        self.create_main_frames()

    def setup_window(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("ai_waifu")
        self.geometry("1200x800")
        self.resizable(0, 0)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=15)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=5)

    def create_main_frames(self):
        self.frame_head = ctk.CTkFrame(self, corner_radius=0, height=1)
        self.frame_head.grid(row=0, column=0, columnspan=2, sticky="nsew")
        self.create_head_widgets()

        self.frame_left = ctk.CTkFrame(self, corner_radius=0)
        self.frame_left.grid(row=1, column=0, sticky="nsew")
        self.setup_chat_frame()
        self.create_chat_widgets()

        self.frame_right = ctk.CTkFrame(self, corner_radius=0)
        self.frame_right.grid(row=1, column=1, sticky="nsew")
        self.setup_l2d_frame()
        self.after(100, self.create_l2d_widgets)

    def create_head_widgets(self):
        self.theme_toggle = ctk.CTkSwitch(self.frame_head, text=self.theme, command=self.toggle_theme)
        self.theme_toggle.pack(side="right")

        self.check_tts = ctk.StringVar(value="on")
        self.tts_checkbox = ctk.CTkCheckBox(
            self.frame_head, variable=self.check_tts, onvalue="on", offvalue="off", text="TTS"
        )
        self.tts_checkbox.pack(side="left", padx=10)

    def toggle_theme(self):
        if ctk.get_appearance_mode() == "Dark":
            ctk.set_appearance_mode("Light")
            self.theme = "Light"

        else:
            ctk.set_appearance_mode("Dark")
            self.theme = "dark"

        self.theme_toggle.configure(text=self.theme)

    def setup_chat_frame(self):
        self.frame_left.grid_columnconfigure(0, weight=1)
        self.frame_left.grid_rowconfigure(0, weight=10)
        self.frame_left.grid_rowconfigure(1, weight=1)

    def create_chat_widgets(self):
        self.chat_frame = ctk.CTkFrame(self.frame_left, corner_radius=0, height=1)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid(row=0, column=0, sticky="nsew")

        self.textbox = ctk.CTkTextbox(self.chat_frame, corner_radius=0)
        self.textbox.grid(row=0, column=0, sticky="nsew")
        self.textbox.configure(state="disabled")

        self.chat_input_frame = ctk.CTkFrame(self.frame_left, corner_radius=0, height=1)
        self.chat_input_frame.grid_columnconfigure(0, weight=1)
        self.chat_input_frame.grid_rowconfigure(0, weight=1)
        self.chat_input_frame.grid(row=1, column=0, sticky="nsew")

        self.text_input = ctk.CTkEntry(self.chat_input_frame, fg_color="transparent")
        self.text_input.grid(row=0, column=0, sticky="nsew", padx=15, pady=10)
        self.text_input.bind("<Return>", self.send_text)

    def send_text(self, event=None):
        text = self.text_input.get()
        self.text_input.delete(0, "end")

        print(f"user: {text}")
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"user\n{text}\n\n")
        self.textbox.configure(state="disabled")
        self.textbox.see("end")

        thread = threading.Thread(target=self._run_callback, args=(text,), daemon=True)
        thread.daemon = True
        thread.start()

    def _run_callback(self, text):
        chatbot_text = queue.Queue()
        self.message_callback(text, chatbot_text)
        bot_response = chatbot_text.get()
        self.textbox.after(0, self._display_bot_response, bot_response)

    def _display_bot_response(self, text):
        self.textbox.configure(state="normal")
        self.textbox.insert("end", f"{self.bot_name}\n{text}\n\n")
        self.textbox.configure(state="disabled")
        self.textbox.see("end")

        if self.check_tts.get() == "on":
            thread = threading.Thread(target=self.play_tts, args=(text,), daemon=True)
            thread.daemon = True
            thread.start()

    def play_tts(self, text):
        audio_path = save_tts(text)
        self.opengl_frame.start_tts(audio_path)

    def setup_l2d_frame(self):
        self.frame_right.grid_columnconfigure(0, weight=1)
        self.frame_right.grid_rowconfigure(0, weight=1)

    def create_l2d_widgets(self):
        x = self.frame_right.winfo_rootx() + (self.frame_right.winfo_width() // 2) - 250
        y = self.frame_right.winfo_rooty() + (self.frame_right.winfo_height() // 2) - 250

        self.l2d_widgets = ctk.CTkToplevel(self)
        self.l2d_widgets.geometry(f"500x500+{x}+{y}")
        self.l2d_widgets.attributes("-transparentcolor", "black")
        self.l2d_widgets.attributes("-topmost", True)
        self.l2d_widgets.overrideredirect(True)

        self.opengl_frame = live2d_frame(self.l2d_widgets, height=500, width=500)
        self.opengl_frame.animate = 1
        self.opengl_frame.grid(row=0, column=0, sticky="nsew")

        self.opengl_frame.bind("<Button-1>", self.start_drag)
        self.opengl_frame.bind("<B1-Motion>", self.do_drag)

    def start_drag(self, event):
        self.drag_start_x = event.x
        self.drag_start_y = event.y

    def do_drag(self, event):
        new_x = event.x_root - self.drag_start_x
        new_y = event.y_root - self.drag_start_y
        self.l2d_widgets.geometry(f"500x500+{new_x}+{new_y}")

    def run(self):
        self.mainloop()
