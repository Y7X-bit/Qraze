import customtkinter as ctk
import qrcode
from PIL import Image, ImageTk
import cv2
import os
import numpy as np
import pyperclip
import webbrowser
from tkinter import filedialog, messagebox
from datetime import datetime

# App Setup
app = ctk.CTk()
app.title("Qraze 💗")
app.geometry("700x665")
app.resizable(False, False)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Styles
button_style = {
    "corner_radius": 20,
    "fg_color": "#000000",
    "hover_color": "#000000",
    "text_color": "#ffffff",
    "font": ("Segoe UI", 13, "bold"),
    "border_color": "#ff3333",
    "border_width": 2,
    "height": 40
}
entry_style = {
    "fg_color": "#000000",
    "border_color": "#ff3333",
    "border_width": 2,
    "text_color": "#ffffff",
    "corner_radius": 20,
    "height": 40
}

# Logic
def save_history(data):
    with open("qr_history.txt", "a") as f:
        f.write(f"[{datetime.now()}] {data}\n")

def generate_qr():
    data = entry_data.get().strip()
    fill = entry_fill.get().strip() or "black"
    bg = entry_bg.get().strip() or "white"
    filename = entry_filename.get().strip() or "qr_code"
    filename += ".png"

    if not data:
        messagebox.showwarning("Warning", "Text/URL cannot be empty!")
        return

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=int(entry_boxsize.get().strip() or 14),
        border=int(entry_border.get().strip() or 4),
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fill, back_color=bg).convert("RGB")

    logo_path = entry_logo.get().strip()
    if logo_path and os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_size = int(img.size[0] * 0.2)
        logo = logo.resize((logo_size, logo_size))
        pos = ((img.size[0] - logo_size) // 2, (img.size[1] - logo_size) // 2)
        img.paste(logo, pos, logo)

    img.save(filename)
    img_preview = ImageTk.PhotoImage(img.resize((250, 250)))
    qr_image_label.configure(image=img_preview)
    qr_image_label.image = img_preview
    messagebox.showinfo("Success", f"QR saved as {filename}")

def browse_logo():
    path = filedialog.askopenfilename(title="Select logo image")
    if path:
        entry_logo.delete(0, ctk.END)
        entry_logo.insert(0, path)

def read_qr_image():
    filepath = filedialog.askopenfilename(title="Select QR Image")
    if not filepath:
        return
    img = cv2.imread(filepath)
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(img)
    if bbox is not None and data:
        pyperclip.copy(data)
        save_history(data)
        if data.startswith("http"):
            webbrowser.open(data)
        messagebox.showinfo("QR Data", f"\U0001F4E6 {data}\n\n(Copied to clipboard)")
    else:
        messagebox.showerror("Error", "QR code not detected.")

def scan_webcam():
    cap = cv2.VideoCapture(0)
    detector = cv2.QRCodeDetector()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        data, bbox, _ = detector.detectAndDecode(frame)
        if data:
            pyperclip.copy(data)
            save_history(data)
            if data.startswith("http"):
                webbrowser.open(data)
            messagebox.showinfo("QR Detected", f"\U0001F4E6 {data}\n(Copied to clipboard)")
            break
        cv2.imshow("Scanning... Press 'q' to cancel", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def show_history():
    if not os.path.exists("qr_history.txt"):
        messagebox.showinfo("History", "No history available yet.")
        return
    with open("qr_history.txt", "r") as file:
        content = file.read()
    messagebox.showinfo("QR History", content or "No entries found.")

# UI
frame = ctk.CTkFrame(app, corner_radius=15, fg_color="#000000")
frame.pack(padx=36, pady=28, fill="both", expand=True)
frame.grid_columnconfigure((0, 1), weight=1, uniform="cols")

row_pad = 12
col_pad = 14

entry_data = entry_filename = entry_fill = entry_bg = entry_boxsize = entry_border = entry_logo = qr_image_label = None

widgets = [
    (ctk.CTkLabel(frame, text="📎 Qraze - QR Suite", font=("Segoe UI Bold", 18), text_color="white"), 0, 0, 2),
    (ctk.CTkEntry(frame, width=420, placeholder_text="Enter text or URL", **entry_style), 1, 0, 2),
    (ctk.CTkEntry(frame, width=420, placeholder_text="Filename (no extension)", **entry_style), 2, 0, 2),
    (ctk.CTkEntry(frame, width=200, placeholder_text="Fill Color", **entry_style), 3, 0, 1),
    (ctk.CTkEntry(frame, width=200, placeholder_text="Background Color", **entry_style), 3, 1, 1),
    (ctk.CTkEntry(frame, width=200, placeholder_text="Box Size", **entry_style), 4, 0, 1),
    (ctk.CTkEntry(frame, width=200, placeholder_text="Border", **entry_style), 4, 1, 1),
    (ctk.CTkEntry(frame, width=420, placeholder_text="Logo path (optional)", **entry_style), 5, 0, 2),
    (ctk.CTkButton(frame, text="Browse Logo", command=browse_logo, **button_style), 6, 0, 2),
    (ctk.CTkButton(frame, text="🎨 Generate QR", command=generate_qr, **button_style), 7, 0, 1),
    (ctk.CTkButton(frame, text="🖼 From Image", command=read_qr_image, **button_style), 7, 1, 1),
    (ctk.CTkButton(frame, text="📷 Webcam Scan", command=scan_webcam, **button_style), 8, 0, 1),
    (ctk.CTkButton(frame, text="📑 View History", command=show_history, **button_style), 8, 1, 1),
    (ctk.CTkLabel(frame, text="🔎 Powered by Y7X 💗", font=("Segoe UI", 12), text_color="white"), 9, 0, 2),
    (ctk.CTkLabel(frame, text="", fg_color="#000000"), 10, 0, 2),
]

for w, r, c, cs in widgets:
    w.grid(row=r, column=c, columnspan=cs, pady=row_pad, padx=col_pad, sticky="ew")
    if isinstance(w, ctk.CTkEntry):
        if "text or URL" in w._placeholder_text:
            entry_data = w
        elif "Filename" in w._placeholder_text:
            entry_filename = w
        elif "Fill Color" in w._placeholder_text:
            entry_fill = w
        elif "Background" in w._placeholder_text:
            entry_bg = w
        elif "Box Size" in w._placeholder_text:
            entry_boxsize = w
        elif "Border" in w._placeholder_text:
            entry_border = w
        elif "Logo" in w._placeholder_text:
            entry_logo = w
    elif isinstance(w, ctk.CTkLabel) and not w.cget("text"):
        qr_image_label = w

app.mainloop()