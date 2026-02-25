# Live-PDF-Notebook
A lightweight automation background utility to instantly turn screenshots and typed notes into a formatted PDF document using global hotkeys.

# Live PDF Notebook

The Problem: Taking screenshots while studying or working usually results in a messy folder full of files like screenshot_123.png with no context.
The Solution: This python tool lets you press F9, capture your screen, and immediately type a note. It then builds a "living" PDF document that handles the layout, image scaling, and page breaks for you—leaving you with a single, organized file.

## ✨ Features
- **F9 Capture:** Instant screenshot followed by a text prompt for notes.
- **Smart Layout:** Automatically wraps text and handles page breaks.
- **Daily Filing:** Saves PDFs with the current date to keep your notes organized.
- **ctrl + C** Cleanly saves and closes the document.

## 🚀 How to Use
1. Clone this repository or download the script.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the script: `python notebook.py`
4. Use **F9** to take a note and **F10** to save the final PDF.

## 🛠️ Requirements
- Python 3.x
- Windows (for `keyboard` and `pyautogui` global hotkeys)
