import tkinter as tk
from tkinter import ttk
import pyautogui
import time
import keyboard
import threading
from plyer import notification
import sys
import os
import ctypes
from ctypes import wintypes

def resource_path(relative_path):
    """ Lấy đường dẫn tuyệt đối đến tài nguyên, hỗ trợ cả dev và pyinstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

class AutoClickerbyPhong:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("250x120+800+500")
        self.root.resizable(False, False)
        
        # Xử lý khi đóng cửa sổ chính
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        try:
            icon_path = resource_path("resources/snowflake.ico")
            self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"Icon Load Error: {e}")

        self.running = False 
        
        self.delay_var = tk.DoubleVar(value=0.1) 
        self.repeat_var = tk.IntVar(value=-1)    
        
        self.mouse_var = tk.StringVar(value="Left")
        self.click_var = tk.StringVar(value="Single")

        self.freeze_var = tk.BooleanVar(value=False)
        
        self.hide_clicking_var = tk.BooleanVar(value=False)
        self.show_finish_var = tk.BooleanVar(value=False)
        
        self.hotkey_var = tk.StringVar(value="F8")

        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff= 0)
        file_menu.add_command(label="Exit", command=self.on_closing, background= "white")

        options_menu = tk.Menu(menubar, tearoff=0)
        clicking_menu = tk.Menu(options_menu, tearoff=0)
        clicking_menu.add_command(label="Options", background= "white", command= self.clicking_options)
        clicking_menu.add_command(label="Repeat", background= "white", command= self.clicking_repeat)
        options_menu.add_cascade(label="Clicking", menu=clicking_menu, background= "white")

        settings_menu = tk.Menu(options_menu, tearoff=0)
        settings_menu.add_command(label="Hot Key", background= "white", command= self.hotkey_setting)
        settings_menu.add_command(label="View", background= "white", command= self.view_setting)
        options_menu.add_cascade(label="Settings", menu=settings_menu, background= "white")

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", background= "white", command=self.help_about)
        
        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Options", menu=options_menu)
        menubar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=menubar)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=1)

        style = ttk.Style()
        style.configure("TButton", font=("Segoe UI", 9))

        self.btn_start = ttk.Button(button_frame, text="Start (F8)", width=12, command=self.start_clicking)
        self.btn_start.grid(row=0, column=0, padx=10, pady= 2, ipadx = 50, ipady= 5)

        self.btn_stop = ttk.Button(button_frame, text="Stop (F8)", width=12, command=self.stop_clicking)
        self.btn_stop.grid(row=1, column=0, padx=10, pady = 2, ipadx = 50, ipady= 5)

        self.footer = tk.Label(
            self.root, 
            text="Auto Clicker by Phong version 1.0", 
            font=("Segoe UI", 8), 
            fg="gray"
        )
        self.footer.pack(side="bottom", pady=5)

    def on_closing(self):
        keyboard.unhook_all_hotkeys()
        self.root.destroy()
        os._exit(0)

    def notify_status(self, title, message):
        try:
            path_to_icon = resource_path("resources/bell.ico")
            if not os.path.exists(path_to_icon):
                path_to_icon = None
                
            notification.notify(
                title=title,
                message=message,
                app_icon = path_to_icon,
                app_name='Auto Clicker',
                timeout=2 
            )
        except Exception as e:
            print(f"Error: {e}")

    def start_clicking(self):
        if self.running: return
        self.running = True
        
        delay = self.delay_var.get()
        repeat = self.repeat_var.get()
        btn = self.mouse_var.get().lower()
        is_double = self.click_var.get() == "Double"
        
        if self.hide_clicking_var.get():
            self.root.withdraw()

        def run():
            start_pos = pyautogui.position()
            count = 0
            while self.running:
                if self.freeze_var.get():
                    pyautogui.moveTo(start_pos)
                if is_double:
                    pyautogui.doubleClick(button=btn)
                else:
                    pyautogui.click(button=btn)
                count += 1
                if repeat != -1 and count >= repeat:
                    self.running = False
                    break
                time.sleep(delay)
            
            if self.show_finish_var.get():
                self.notify_status("Finish", "Đã hoàn thành lượt click tự động!")

        self.notify_status("Clicking", f"Đang bắt đầu click... nhấn phím {self.hotkey_var.get()} để dừng")
        threading.Thread(target=run, daemon=True).start()

    def stop_clicking(self):
        self.running = False
        self.notify_status("Stoping", "Đã dừng click tự động.")

    def toggle_clicking(self):
        if self.running:
            self.stop_clicking()
        else:
            self.start_clicking()

    def flash_window_standard(self, window):
        try:
            hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
            class FLASHWINFO(ctypes.Structure):
                _fields_ = [('cbSize', wintypes.UINT), ('hwnd', wintypes.HWND),
                            ('dwFlags', wintypes.DWORD), ('uCount', wintypes.UINT),
                            ('dwTimeout', wintypes.DWORD)]
            flash_info = FLASHWINFO(ctypes.sizeof(FLASHWINFO), hwnd, 3, 3, 0)
            ctypes.windll.user32.FlashWindowEx(ctypes.byref(flash_info))
        except: pass

    def flash_border_logic(self, frame, count=0):
        if not frame.winfo_exists(): return 
        if count < 6:
            current_color = "#0078d4" if count % 2 == 0 else "#adadad"
            frame.config(highlightbackground=current_color, highlightthickness=3 if count % 2 == 0 else 1)
            self.root.after(100, lambda: self.flash_border_logic(frame, count + 1))

    def clicking_options(self):
        win = tk.Toplevel(self.root)
        win.title("Clicking options")
        win.geometry("320x240+1100+450")
        win.resizable(False, False)
        
        try:
            win.iconbitmap(resource_path("resources/mouse-cursor.ico"))
        except: pass
        
        win.transient(self.root)
        self.root.attributes("-disabled", True)

        def on_close():
            self.root.attributes("-disabled", False) 
            win.destroy()
            self.root.focus_set() 
        win.protocol("WM_DELETE_WINDOW", on_close) 

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
                        text="Freeze the pointer",
                        variable=self.freeze_var).grid(row=2, columnspan=2, pady=20)

        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, columnspan=2)

        ttk.Button(button_frame, text="Ok", command=on_close).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=on_close).pack(side=tk.LEFT, padx=5)

    def clicking_repeat(self):
        win = tk.Toplevel(self.root)
        win.title("Clicking repeat")
        win.geometry("400x230+1100+450")
        win.resizable(False, False)
        
        try:
            win.iconbitmap(resource_path("resources/setting.ico"))
        except: pass
        
        win.transient(self.root)
        self.root.attributes("-disabled", True)

        def close_repeat():
            self.root.unbind("<Button-1>")
            self.root.attributes("-disabled", False)
            win.destroy()
        win.protocol("WM_DELETE_WINDOW", close_repeat)

        main_frame = ttk.Frame(win, padding=10)
        main_frame.pack(fill="both", expand=True)

        repeat_frame = ttk.LabelFrame(main_frame, text="Repeat", padding=8)
        repeat_frame.pack(fill="x", pady=4)

        self.repeat_mode = tk.IntVar(value=1)

        repeat_frame.columnconfigure(1, weight=1)

        ttk.Radiobutton(
            repeat_frame,
            text="Repeat",
            variable=self.repeat_mode,
            value=1
        ).grid(row=0, column=0, sticky="w")

        self.repeat_times = tk.IntVar(value=99999)
        ttk.Spinbox(
            repeat_frame,
            from_=1,
            to=999999,
            textvariable=self.repeat_times,
            width=8
        ).grid(row=0, column=1, padx=4)

        ttk.Label(repeat_frame, text="times").grid(row=0, column=2, sticky="w")

        ttk.Radiobutton(
            repeat_frame,
            text="Repeat until stopped",
            variable=self.repeat_mode,
            value=2
        ).grid(row=1, column=0, columnspan=3, sticky="w", pady=3)

        interval_frame = ttk.LabelFrame(main_frame, text="Interval", padding=8)
        interval_frame.pack(fill="x", pady=6)

        ttk.Label(interval_frame, text="Interval:").grid(row=0, column=0, padx=0)

        time_settings = [
            ["h", 0],
            ["m", 0],
            ["s", 0],
            ["ms", 10]
        ]

        self.time_vars = {}

        for i, item in enumerate(time_settings):
            label_text = item[0]
            default_val = item[1]
            var = tk.IntVar(value=default_val)
            self.time_vars[label_text] = var

            ttk.Entry(
                interval_frame,
                textvariable=var,
                width=5,
                justify="center"
            ).grid(row=0, column=i*2 + 1, padx=2)

            ttk.Label(
                interval_frame,
                text=label_text
            ).grid(row=0, column=i*2 + 2, padx=0)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=6)

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        def save_and_close():
            if self.apply_click_settings():
                close_repeat()

        ttk.Button(
            button_frame,
            text="Ok",
            width=10,
            command=save_and_close
        ).grid(row=0, column=0, sticky="e", padx=5)

        ttk.Button(
            button_frame,
            text="Cancel",
            width=10,
            command=close_repeat
        ).grid(row=0, column=1, sticky="w", padx=5)

    def apply_click_settings(self):
        if self.repeat_mode.get() == 1:
            self.repeat_var.set(self.repeat_times.get()) 
        else:
            self.repeat_var.set(-1)
        
        try:
            h = self.time_vars["h"].get()
            m = self.time_vars["m"].get()
            s = self.time_vars["s"].get()
            ms = self.time_vars["ms"].get()
            
            total_delay = h*3600 + m*60 + s + ms/1000
            self.delay_var.set(total_delay)
            return True
        except tk.TclError:
            self.notify_status("Input Error", "Please enter numbers only in the time field!")
            return False

    def change_hotkey(self, label_widget):
        label_widget.config(text="Press Key...", bg="#fff5f5", fg="#d32f2f", highlightbackground="#d32f2f")

        def wait_for_key():
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                new_key = event.name.upper()
                self.root.after(0, lambda: self.update_key_ui(label_widget, new_key))

        threading.Thread(target=wait_for_key, daemon=True).start()
    
    def update_key_ui(self, label_widget, new_key):
        if label_widget.winfo_exists():
            self.hotkey_var.set(new_key)
            label_widget.config(
                text=new_key, 
                bg="#ffffff", 
                fg="#0078d4", 
                highlightbackground="#0078d4"
            )
        else:
            self.hotkey_var.set(new_key)

    def apply_hotkey(self):
        new_key = self.hotkey_var.get()
        keyboard.unhook_all_hotkeys() 
        keyboard.add_hotkey(new_key, self.toggle_clicking) 
        
        self.btn_start.config(text=f"Start ({new_key})")
        self.btn_stop.config(text=f"Stop ({new_key})")
        
        self.notify_status("Hotkey", f"The hotkey has been changed {new_key}")

    def hotkey_setting(self):
        old_key = self.hotkey_var.get()
        win = tk.Toplevel(self.root)
        win.title("Hotkey Setting")
        win.geometry("320x180+1100+470")
        win.resizable(False, False)
        
        try:
            win.iconbitmap(resource_path("resources/key.ico"))
        except: pass
        
        win.configure(bg="#f8f9fa") 
        win.transient(self.root)
        self.root.attributes("-disabled", True)

        def close_hotkey():
            self.root.unbind("<Button-1>")
            self.root.attributes("-disabled", False)
            win.destroy()
        win.protocol("WM_DELETE_WINDOW", close_hotkey)

        main_frame = ttk.Frame(win, padding=20)
        main_frame.pack(fill="both", expand=True)

        top_row = ttk.Frame(main_frame)
        top_row.pack(pady=10)

        tk.Label(top_row, text="Click / Stop", font=("Segoe UI", 10)).pack(side="left", padx=10)
        
        self.key_display = tk.Label(
            top_row, 
            text=self.hotkey_var.get(),
            font=("Segoe UI", 12, "bold"),
            bg="#ffffff",          
            fg="#0078d4",          
            width=10,
            height=2,
            relief="flat",         
            highlightthickness=2,   
            highlightbackground="#0078d4", 
            cursor="hand2"         
        )
        self.key_display.pack(side="left", padx=10)

        self.key_display.bind("<Button-1>", lambda e: self.change_hotkey(self.key_display))
        self.key_display.bind("<Enter>", lambda e: self.key_display.config(bg="#f0f7ff"))
        self.key_display.bind("<Leave>", lambda e: self.key_display.config(bg="#ffffff"))

        ttk.Label(main_frame, text="Click the box above and press any key", 
                  font=("Segoe UI", 8, "italic"), foreground="gray").pack()

        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(side="bottom", pady=10)
        
        def save_and_close_hotkey():
            try:
                self.apply_hotkey()
            except Exception as e:
                print(f"Lỗi khi lưu phím: {e}")
            finally:
                close_hotkey()

        ttk.Button(btn_frame, text="Ok", width=10, 
                   command=save_and_close_hotkey).pack(side="left", padx=5)
        
        def cancel_action():
            self.hotkey_var.set(old_key)
            self.root.attributes("-disabled", False)
            win.destroy()
        
        ttk.Button(btn_frame, text="Cancel", width=10, command=cancel_action).pack(side="left", padx=5)

    def view_setting(self):
        old_hide = self.hide_clicking_var.get()
        old_show = self.show_finish_var.get()

        win = tk.Toplevel(self.root)
        win.title("View Setting")
        win.geometry("320x220+1100+450")
        win.resizable(False, False)
        win.configure(bg="#f8f9fa")
        
        try:
            win.iconbitmap(resource_path("resources/eyes.ico"))
        except: pass
        
        win.transient(self.root)
        self.root.attributes("-disabled", True)

        def close_setting():
            self.root.unbind("<Button-1>")
            self.root.attributes("-disabled", False)
            win.destroy()
        win.protocol("WM_DELETE_WINDOW", close_setting)

        main_frame = tk.Frame(win, bg="#f8f9fa", padx=30, pady=20)
        main_frame.pack(fill="both", expand=True)

        ttk.Checkbutton(main_frame, text="Hide when it is clicking", 
                        variable=self.hide_clicking_var).pack(anchor="w", pady=10)
        ttk.Checkbutton(main_frame, text="Show when it finish click", 
                        variable=self.show_finish_var).pack(anchor="w", pady=10)

        btn_frame = tk.Frame(main_frame, bg="#f8f9fa") 
        btn_frame.pack(side="bottom", pady=15, fill="x")

        ok_btn = tk.Button(
            btn_frame, text="Ok", width=11, bg="#e1f1ff", relief="flat", bd=0,
            highlightthickness=1, font=("Segoe UI", 9),
            command=close_setting, cursor="hand2"
        )
        ok_btn.pack(side="left", padx=15, ipady=2, expand=True)

        def on_cancel_view():
            self.hide_clicking_var.set(old_hide)
            self.show_finish_var.set(old_show)
            self.root.attributes("-disabled", False)
            win.destroy()

        cancel_btn = tk.Button(
            btn_frame, text="Cancel", width=11, bg="#ffffff", relief="flat", bd=0,
            highlightthickness=1, highlightbackground="#adadad", font=("Segoe UI", 9),
            command=on_cancel_view, cursor="hand2"
        )
        cancel_btn.pack(side="left", padx=15, ipady=2, expand=True)

    def help_about(self):
        win = tk.Toplevel(self.root)
        win.title("How to use")
        win.geometry("400x230+1100+450")
        win.resizable(False, False)
        
        try:
            win.iconbitmap(resource_path("resources/guide.ico"))
        except: pass
        
        win.transient(self.root)
        self.root.attributes("-disabled", True)
        def close_about():
            self.root.unbind("<Button-1>")
            self.root.attributes("-disabled", False)
            win.destroy()
        win.protocol("WM_DELETE_WINDOW", close_about)

        main_frame = tk.Frame(win, bg="#f8f9fa", padx=15, pady=20)
        main_frame.pack(fill="both", expand=True)

        huong_dan = """Instructions for use:
1. Options -> Clicking -> Options: Change mouse cursor L/R/M.
2. Options -> Clicking -> Repeat: Adjust speed and number of clicks.
3. Options -> Settings -> Hot Key: Change start/stop hot key.
4. Options -> Settings -> View: Customize window hide/show.

Note: L: Left, R: Right, M: Middle mouse cursor
Press the hot key Default F8 to Start/Stop Auto Click."""

        lbl_guide = tk.Label(
            main_frame, 
            text=huong_dan, 
            bg="#f8f9fa", 
            font=("Segoe UI", 9), 
            justify="left",        
            anchor="w"              
        )
        lbl_guide.pack(side="top", fill="both", expand=True, pady=0)

        btn_frame = tk.Frame(main_frame, bg="#f8f9fa") 
        btn_frame.pack(side="bottom", pady=15, fill="x")

        ok_btn = tk.Button(
            btn_frame, text="Ok", width=11, bg="#e1f1ff", relief="flat", bd=0,
            highlightthickness=1, font=("Segoe UI", 9),
            command=close_about, cursor="hand2")
        ok_btn.pack(side="left", padx=15, ipady=2, expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerbyPhong(root)
    keyboard.add_hotkey("F8", app.toggle_clicking)
    root.mainloop()