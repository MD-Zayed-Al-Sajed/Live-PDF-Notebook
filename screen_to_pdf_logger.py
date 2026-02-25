import os
import time
import queue
import pyautogui
import keyboard
from tkinter import Tk, simpledialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

# ================= LAYOUT CONFIG =================
TOP_MARGIN = 50
BOTTOM_MARGIN = 50
LEFT_MARGIN = 50
PAGE_WIDTH, PAGE_HEIGHT = A4
IMAGE_WIDTH = PAGE_WIDTH - (LEFT_MARGIN * 2)
LINE_HEIGHT = 15

# ================= SETUP =================
root = Tk()
root.withdraw()

folder = simpledialog.askstring("Setup", "Enter folder path:")
if not folder or not os.path.exists(folder):
    exit()

pdf_path = os.path.join(folder, "Living_Notebook.pdf")

# Create the canvas ONCE at the start
c = canvas.Canvas(pdf_path, pagesize=A4)
current_y = PAGE_HEIGHT - TOP_MARGIN
task_queue = queue.Queue()

def wrap_text(text, max_width, canvas_obj):
    words = text.split(' ')
    lines, current_line = [], []
    for word in words:
        test_line = ' '.join(current_line + [word])
        if canvas_obj.stringWidth(test_line, "Helvetica", 11) < max_width:
            current_line.append(word)
        else:
            lines.append(' '.join(current_line))
            current_line = [word]
    lines.append(' '.join(current_line))
    return lines

def process_capture():
    global current_y
    
    # 1. Capture
    timestamp = time.strftime("%H%M%S")
    temp_img = os.path.join(folder, f"temp_{timestamp}.png")
    pyautogui.screenshot().save(temp_img)

    # 2. Get Note
    note = simpledialog.askstring("Note", "Enter text:")
    if note is None: note = ""

    # 3. Calculate Dimensions
    img_reader = ImageReader(temp_img)
    iw, ih = img_reader.getSize()
    aspect = ih / float(iw)
    display_height = IMAGE_WIDTH * aspect
    
    wrapped_lines = wrap_text(note, IMAGE_WIDTH, c)
    text_height = len(wrapped_lines) * LINE_HEIGHT
    total_needed = display_height + text_height + 40

    # 4. Page Management (Word-style Flow)
    if current_y - total_needed < BOTTOM_MARGIN:
        c.showPage() # Create a NEW page
        current_y = PAGE_HEIGHT - TOP_MARGIN

    # 5. Draw Content
    c.drawImage(temp_img, LEFT_MARGIN, current_y - display_height, width=IMAGE_WIDTH, height=display_height)
    current_y -= (display_height + 15)

    c.setFont("Helvetica-Bold", 11)
    for line in wrapped_lines:
        if current_y < BOTTOM_MARGIN:
            c.showPage()
            current_y = PAGE_HEIGHT - TOP_MARGIN
        c.drawString(LEFT_MARGIN, current_y, line)
        current_y -= LINE_HEIGHT

    current_y -= 30 # Space before next capture
    
    # Clean up image immediately
    os.remove(temp_img)
    print("Capture added to document buffer...")

def hotkey_trigger():
    task_queue.put(True)

keyboard.add_hotkey("F9", hotkey_trigger)

print("Running... Press F9 to capture.")
print("IMPORTANT: To finish and save the PDF, close the program or press Ctrl+C in this window.")

# ================= MAIN LOOP =================
try:
    while True:
        try:
            task_queue.get(timeout=0.1)
            process_capture()
        except queue.Empty:
            root.update()
except KeyboardInterrupt:
    print("\nSaving PDF...")
finally:
    # This is the ONLY place we save. It writes all pages at once.
    c.save()
    print(f"File saved to: {pdf_path}")