import tkinter as tk
from tkinter import filedialog
import os
from tkinter import messagebox
import subprocess
import shutil
global file_open
global current_file
file_open = 0
last_file_path = os.path.join(os.path.expanduser('~'), 'Library', 'Caches', 'NotepadEE', 'last_file_path')
if os.path.exists(last_file_path):
    with open(last_file_path, 'r') as file:
        current_file = file.read()
        if current_file.strip() == '':
            file_open = 0
        else:
            file_open = 1
else:
    current_file = ""
    file_open = 0
last_write = os.path.join(os.path.expanduser('~'), 'Library', 'Caches', 'NotepadEE', 'last_write')
folder_path = os.path.join(os.path.expanduser('~'), 'Library', 'Caches', 'NotepadEE')
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
make_new_instance = """#!/bin/bash
INSTANCES=~/Library/Caches/NotepadEE/Instances
if [ ! -d "$INSTANCES" ]; then
  mkdir "$INSTANCES"
fi
SRC_DIR=/Applications/Notepad==.app/Contents/Resources/Clone
SRC_FILE="Notepad=="
TARGET_DIR=~/Library/Caches/NotepadEE/Instances
EXT=.app
cp -R "$SRC_DIR/Notepad==.app" "${TARGET_DIR}/Notepad==0$EXT"
NUM=0
for (( NUM=0; ; NUM++ )); do
  if [ ! -e "${TARGET_DIR}/Notepad==$NUM$EXT" ]; then
    break
  fi
done
cp -R "${TARGET_DIR}/Notepad==0${EXT}" "${TARGET_DIR}/Notepad==$NUM$EXT"
open -a "${TARGET_DIR}/Notepad==$NUM$EXT"
"""
instanceshellscriptpath = os.path.join(os.path.expanduser('~'), 'Library', 'Caches', 'NotepadEE', 'make_new_instance.sh')
with open(instanceshellscriptpath, "w") as f:
    f.write(make_new_instance)
def autosave_file(event=None):
    global current_file
    global file_open
    try:
        if file_open == 1:
            with open(current_file, 'w') as file:
                text = text_area.get('1.0', 'end-1c')
                file.write(text)
    except FileNotFoundError:
        return 'break'
def write_cache(event=None):
    global current_file
    global file_open
    with open(os.path.join(os.path.expanduser('~'), 'Library', 'Caches', 'NotepadEE', 'last_write'), 'w') as file:
        file.write(text_area.get('1.0', 'end-1c'))
    last_file_path = os.path.join(os.path.expanduser('~'), 'Library', 'Caches', 'NotepadEE', 'last_file_path')
    with open(last_file_path, 'w') as file:
        file.write(current_file)
    autosave_file()
    root.after(5000, write_cache)
def save_as(event=None):
    global current_file
    global file_open
    file_path = filedialog.asksaveasfilename(defaultextension=".txt")
    current_file = file_path
    with open(file_path, 'w') as file:
        text = text_area.get(1.0, "end-1c")
        file.write(text)
    write_cache()
    file_open = 1
def open_file(event=None):
    global current_file, file_open
    file_path = filedialog.askopenfilename(filetypes=[("All Files", "*.*")])
    if file_path:
        text_area.delete(1.0, "end")
        current_file = file_path
        with open(file_path, 'r') as file:
            text_area.insert(1.0, file.read())
    write_cache()
    file_open = 1
def save_file(event=None):
    global current_file
    global file_open
    if file_open == 1:
        with open(current_file, 'w') as file:
            text = text_area.get('1.0', 'end-1c')
            file.write(text)
        write_cache()
    else:
        response = messagebox.askyesno("Create new file", "The file does not exist. Do you want to create it as a new file?")
        if response:
            save_as()


def clear(event=None):
    global current_file, file_open
    text_area.delete(1.0, "end")
    current_file = ""
    write_cache()
    file_open = 0
def cut_text(event=None):
    text_area.clipboard_clear()
    text_area.clipboard_append(text_area.get("sel.first", "sel.last"))
    text_area.delete("sel.first", "sel.last")
    return 'break'
def copy_text(event=None):
    text_area.clipboard_clear()
    text_area.clipboard_append(text_area.get("sel.first", "sel.last"))
    return 'break'
def paste_text(event=None):
    text_area.insert("insert", text_area.clipboard_get())
    return 'break'
def select_all_text(event=None):
    text_area.tag_add("sel", "1.0", "end")
    return 'break'
def add_instance(event=None):
    subprocess.run(["/bin/bash", instanceshellscriptpath])
def clear_instances(event=None):
    response2 = messagebox.askyesno("Clear instances", "Are you sure you want to clear all instances? Make sure to close all other instances before clearing. Click 'No' to get back to clear all other instances.")
    if response2:
        folder_path = os.path.join(os.path.expanduser('~'), 'Library', 'Caches', 'NotepadEE', 'Instances')
        shutil.rmtree(folder_path)
# --- Font Styling Functions ---
def toggle_bold():
    global text_area
    current_tags = text_area.tag_names("sel.first")
    if "bold" in current_tags:
        text_area.tag_remove("bold", "sel.first", "sel.last")
    else:
        text_area.tag_add("bold", "sel.first", "sel.last")
def toggle_italic():
    global text_area
    current_tags = text_area.tag_names("sel.first")
    if "italic" in current_tags:
        text_area.tag_remove("italic", "sel.first", "sel.last")
    else:
        text_area.tag_add("italic", "sel.first", "sel.last")
def toggle_underline():
    global text_area
    current_tags = text_area.tag_names("sel.first")
    if "underline" in current_tags:
        text_area.tag_remove("underline", "sel.first", "sel.last")
    else:
        text_area.tag_add("underline", "sel.first", "sel.last")
# --- Font Size Options ---
def change_font_size(new_size):
    global text_area
    text_area.config(font=(current_font, new_size))

current_size = 12  # Set the font size to 12

# --- Font Family Selection ---
def change_font_family(new_family):
    global text_area, current_font
    current_font = new_family
    text_area.config(font=(new_family, current_size))
def apply_color(color):
    global text_area
    text_area.tag_add(color, "sel.first", "sel.last")
    text_area.tag_config(color, foreground=color)

def insert_bullet_point():
    global text_area
    text_area.insert("insert", "- ")

def align_left():
    global text_area
    text_area.tag_add("left", "sel.first", "sel.last")
    text_area.tag_config("left", justify=tk.LEFT)

def align_center():
    global text_area
    text_area.tag_add("center", "sel.first", "sel.last")
    text_area.tag_config("center", justify=tk.CENTER)

def align_right():
    global text_area
    text_area.tag_add("right", "sel.first", "sel.last")
    text_area.tag_config("right", justify=tk.RIGHT)

root = tk.Tk()
ask_quit = False
root.title("Notepad== Rich text Editor")
text_area = tk.Text(root, width=100, height=80, wrap=tk.WORD)
text_area.pack()
if os.path.exists(last_write):
    text_area.delete(1.0, "end")
    with open(last_write, 'r') as file:
        text_area.insert(1.0, file.read())
# Configure tags for bold, italic, and underline
text_area.tag_config("bold", font=("Arial", current_size, "bold"))
text_area.tag_config("italic", font=("Arial", current_size, "italic"))
text_area.tag_config("underline", font=("Arial", current_size, "underline"))
menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=clear)
file_menu.add_command(label="Open...", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save as...", command=save_as)
edit_menu = tk.Menu(menu)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)
edit_menu.add_command(label="Select All", command=select_all_text)
edit_menu.add_separator()  # Add a separator line
edit_menu.add_command(label="Bold", command=toggle_bold)
edit_menu.add_command(label="Italic", command=toggle_italic)
edit_menu.add_command(label="Underline", command=toggle_underline)
# --- Font Size Menu ---
font_size_menu = tk.Menu(edit_menu, tearoff=0)
edit_menu.add_cascade(label="Font Size", menu=font_size_menu)
font_size_menu.add_command(label="Small", command=lambda: change_font_size(10))
font_size_menu.add_command(label="Medium", command=lambda: change_font_size(12))
font_size_menu.add_command(label="Large", command=lambda: change_font_size(14))
# --- Font Family Menu ---
font_family_menu = tk.Menu(edit_menu, tearoff=0)
edit_menu.add_cascade(label="Font Family", menu=font_family_menu)
font_family_menu.add_command(label="Arial", command=lambda: change_font_family("Arial"))
font_family_menu.add_command(label="Times New Roman", command=lambda: change_font_family("Times New Roman"))
font_family_menu.add_command(label="Courier New", command=lambda: change_font_family("Courier New"))
window_menu = tk.Menu(menu)
menu.add_cascade(label="Window", menu=window_menu)
window_menu.add_command(label="Launch new instance", command=add_instance)
window_menu.add_command(label="Clear all instances", command=clear_instances)
# --- Tools Menu ---
tools_menu = tk.Menu(menu)
menu.add_cascade(label="Tools", menu=tools_menu)
# --- Color Menu ---
color_menu = tk.Menu(tools_menu, tearoff=0)
tools_menu.add_cascade(label="Color", menu=color_menu)
color_menu.add_command(label="Red", command=lambda: apply_color("red"))
color_menu.add_command(label="Green", command=lambda: apply_color("green"))
color_menu.add_command(label="Blue", command=lambda: apply_color("blue"))
# --- Bullet Point Menu ---
tools_menu.add_command(label="Bullet Point", command=insert_bullet_point)
# --- Alignment Menu ---
alignment_menu = tk.Menu(tools_menu, tearoff=0)
tools_menu.add_cascade(label="Alignment", menu=alignment_menu)
alignment_menu.add_command(label="Left", command=align_left)
alignment_menu.add_command(label="Center", command=align_center)
alignment_menu.add_command(label="Right", command=align_right)
root.bind('<Command-n>', clear)
root.bind('<Command-o>', open_file)
root.bind('<Command-s>', save_file)
root.bind('<Command-S>', save_as)
text_area.bind('<Command-x>', cut_text)
text_area.bind('<Command-c>', copy_text)
text_area.bind('<Command-v>', paste_text)
text_area.bind('<Command-a>', select_all_text)
root.bind('<Command-l>', add_instance)
root.bind('<Command-L>', clear_instances)
# --- Keyboard Shortcuts for Font Styling ---
text_area.bind('<Control-b>', toggle_bold)
text_area.bind('<Control-i>', toggle_italic)
text_area.bind('<Control-u>', toggle_underline)
# --- Initial Font Settings ---
current_font = "Arial"
current_size = 12
text_area.config(font=(current_font, current_size))
write_cache()
root.mainloop()
