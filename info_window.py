import tkinter as tk
class InfoWindow:
    def setup(self):
        self.root = tk.Tk()
        self.root.title("Painter Info")
        self.root.geometry("250x150")
        self.root.resizable(False, False)
        self.label = tk.Label(self.root, text="loading...", font=("Arial", 12), justify="center")
        self.label.pack(pady=30)
        self.root.mainloop()
    def update_info(self, mode, is_drawing):
        label_text = f"Drawing Mode : {mode}\n\n\n Drawing : {is_drawing}"
        self.label.config(text=label_text)