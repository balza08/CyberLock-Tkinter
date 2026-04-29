import tkinter as tk
import signal
from PIL import Image, ImageTk  #libreria per foto e GIF

# Ignora segnali di terminazione
for sig in (signal.SIGINT, signal.SIGTERM):
    try:
        signal.signal(sig, signal.SIG_IGN)
    except (OSError, ValueError):
        pass

# Finestra principale
root = tk.Tk()
root.title("LOCKSCREEN")
root.attributes("-fullscreen", True)
root.attributes("-topmost", True)
root.overrideredirect(True)

# Blocca chiusura finestra
root.protocol("WM_DELETE_WINDOW", lambda: None)

# Imposta focus e grab
def setup_grab():
    root.focus_force()
    root.grab_set()
    try:
        root.grab_set_global()
    except Exception:
        pass

root.after(300, setup_grab)

# Mantiene fullscreen e topmost
def enforce():
    root.attributes("-fullscreen", True)
    root.attributes("-topmost", True)
    root.lift()
    root.after(200, enforce)

root.after(200, enforce)

# Blocca scorciatoie
BLOCKED_KEYS = [
    "<Alt-F4>",
    "<Alt-Tab>",
    "<Super_L>",
    "<Super_R>",
    "<Control-Alt-Delete>",
    "<Escape>",
    "<Alt-F2>",
    "<Control-c>",
    "<Control-z>",
    "<Control-q>",
    "<F11>",
]

for key in BLOCKED_KEYS:
    root.bind_all(key, lambda e: "break")

# Dimensioni schermo
W = root.winfo_screenwidth()
H = root.winfo_screenheight()

# Canvas sfondo
canvas = tk.Canvas(
    root,
    width=W,
    height=H,
    bg="#0a0a0f",
    highlightthickness=0
)
canvas.pack(fill="both", expand=True)

panel = tk.Frame(root, bg="#0f0f1a")
panel.place(relx=0.5, rely=0.5, anchor="center")

img = Image.open("pawned.jpg")
img = img.resize((320, 180))
photo = ImageTk.PhotoImage(img)

img_label = tk.Label(panel, image=photo, bg="#0f0f1a")
img_label.pack(pady=(10, 5))

#output
title = tk.Label(
    panel,
    text="SYSTEM COMPROMISED",
    font=("Courier New", 18, "bold"),
    fg="#ff2e2e",
    bg="#0f0f1a"
)
title.pack(pady=(0, 10))

# Linee decorative
for i in range(0, W + H, 60):
    canvas.create_line(i, 0, 0, i, fill="#1a1a2e", width=1)
    
# Password
PASSWORD = "1234"

frame = tk.Frame(panel, bg="#0f0f1a")
frame.pack()

entry_var = tk.StringVar()
error_var = tk.StringVar()

entry = tk.Entry(
    frame,
    textvariable=entry_var,
    show="●",
    font=("Courier New", 20),
    bg="#12122a",
    fg="#e0e0ff",
    insertbackground="#e0e0ff",
    relief="flat",
    width=20,
    justify="center",
    highlightthickness=2,
    highlightcolor="#5555ff",
    highlightbackground="#2a2a4a"
)
entry.pack(ipady=10)
entry.focus_set()

error_label = tk.Label(
    frame,
    textvariable=error_var,
    font=("Courier New", 12),
    bg="#0a0a0f",
    fg="#ff5555"
)
error_label.pack(pady=(6, 0))

# Sblocco
def unlock(event=None):
    if entry_var.get() == PASSWORD:
        root.grab_release()
        root.overrideredirect(False)
        root.attributes("-fullscreen", False)
        root.destroy()
    else:
        error_var.set("Password errata, riprova")
        entry_var.set("")
        entry.focus_set()

# Bottone
btn = tk.Button(
    frame,
    text="UNLOCK",
    command=unlock,
    font=("Courier New", 13, "bold"),
    bg="#1e1e4a",
    fg="#e0e0ff",
    activebackground="#3333aa",
    activeforeground="#ffffff",
    relief="flat",
    padx=30,
    pady=8,
    cursor="hand2"
)
btn.pack(pady=(12, 15))

entry.bind("<Return>", unlock)
entry.bind("<Escape>", lambda e: "break")

# Focus sempre sull'entry
root.bind_all("<Button-1>", lambda e: entry.focus_set())

# Avvio
root.mainloop()