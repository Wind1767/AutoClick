import tkinter as tk
from tkinter import ttk
import pyautogui
def clicking_options(self):
        win = tk.Toplevel(self.root)
        win.title("Clicking options")
        win.geometry("320x240+500+500")
        win.resizable(False, False)

        main_frame = ttk.Frame(win, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Mouse:").grid(row=0, column=0, sticky=tk.W, pady=10)

        self.mouse_var = tk.StringVar(value="Left")
        ttk.Combobox(main_frame, textvariable=self.mouse_var,
                    values=["Left", "Right", "Middle"],
                    state="readonly").grid(row=0, column=1, padx=10)

        ttk.Label(main_frame, text="Click:").grid(row=1, column=0, sticky=tk.W, pady=10)

        self.click_var = tk.StringVar(value="Single")
        ttk.Combobox(main_frame, textvariable=self.click_var,
                    values=["Single", "Double"],
                    state="readonly").grid(row=1, column=1, padx=10)

        self.freeze_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame,
                        text="Freeze the pointer (only single click)",
                        variable=self.freeze_var).grid(row=2, columnspan=2, pady=20)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, columnspan=2)

        ttk.Button(button_frame, text="Ok", command=win.destroy).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=win.destroy).pack(side=tk.LEFT, padx=5)
        self.root.mainloop()
clicking_options()