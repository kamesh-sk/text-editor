import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file(text_edit, line_numbers, word_count_label):
    filepath = askopenfilename(filetypes=[("Text File", "*.txt")])
    if not filepath:
        return
    text_edit.delete(1.0, tk.END)
    line_numbers.config(state=tk.NORMAL)
    line_numbers.delete(1.0, tk.END)
    with open(filepath, "r") as f:
        content = f.read()
        text_edit.insert(tk.END, content)
        lines = len(content.split('\n'))
        for line in range(1, lines+1):
            line_numbers.insert(tk.END, str(line) + '\n')
    line_numbers.config(state=tk.DISABLED)
    update_word_count(text_edit, word_count_label)

def save_file(text_edit):
    filepath = asksaveasfilename(filetypes=[("Text File", "*.txt")])
    if not filepath:
        return
    with open(filepath, "w") as f:
        content = text_edit.get(1.0, tk.END)
        f.write(content)

def new_file(text_edit, line_numbers, word_count_label):
    text_edit.delete(1.0, tk.END)
    line_numbers.config(state=tk.NORMAL)
    line_numbers.delete(1.0, tk.END)
    line_numbers.config(state=tk.DISABLED)
    word_count_label.config(text="Word Count: 0")

def update_word_count(text_edit, word_count_label):
    content = text_edit.get(1.0, tk.END)
    words = content.split()
    word_count = len(words)
    char_count = len(content)
    line_count = content.count('\n') + 1  # Counting '\n' to determine lines
    word_count_label.config(text=f"Word Count: {word_count}, Character Count: {char_count}, Line Count: {line_count}")

def make_bold(text_edit):
    text_edit.tag_add("bold", "sel.first", "sel.last")
    text_edit.tag_config("bold", font=("Times", 12, "bold"))

def make_italic(text_edit):
    text_edit.tag_add("italic", "sel.first", "sel.last")
    text_edit.tag_config("italic", font=("Times", 12, "italic"))

def make_underline(text_edit):
    text_edit.tag_add("underline", "sel.first", "sel.last")
    text_edit.tag_config("underline", underline=True)


def zoom_in(text_edit):
    current_size = text_edit["font"].actual()["size"]
    new_size = current_size + 2  # Increase font size by 2
    text_edit.configure(font=(text_edit["font"].actual()["family"], new_size))

def zoom_out(text_edit):
    current_size = text_edit["font"].actual()["size"]
    new_size = max(6, current_size - 2)  # Ensure font size does not go below 6
    text_edit.configure(font=(text_edit["font"].actual()["family"], new_size))

def main():
    window = tk.Tk()
    window.title("Text Editor")
    window.geometry("700x400")  

    text_edit = tk.Text(window, font="Times 12")
    text_edit.pack(expand=True, fill='both')

    line_numbers = tk.Text(window, width=4, padx=4, borderwidth=0, background='#f0f0f0', state=tk.DISABLED)
    line_numbers.pack(side=tk.LEFT, fill=tk.Y)

    word_count_label = tk.Label(window, text="Word Count: 0")
    word_count_label.pack()

    menu_bar = tk.Menu(window)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="New", command=lambda: new_file(text_edit, line_numbers, word_count_label))
    file_menu.add_command(label="Open", command=lambda: open_file(text_edit, line_numbers, word_count_label))
    file_menu.add_command(label="Save", command=lambda: save_file(text_edit))
    file_menu.add_command(label="Exit", command=window.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)

    edit_menu = tk.Menu(menu_bar, tearoff=0)
    edit_menu.add_command(label="Cut", command=lambda: text_edit.event_generate("<<Cut>>"))
    edit_menu.add_command(label="Copy", command=lambda: text_edit.event_generate("<<Copy>>"))
    edit_menu.add_command(label="Paste", command=lambda: text_edit.event_generate("<<Paste>>"))
    edit_menu.add_separator()
    edit_menu.add_command(label="Bold", command=lambda: make_bold(text_edit))
    edit_menu.add_command(label="Italic", command=lambda: make_italic(text_edit))
    edit_menu.add_command(label="Underline", command=lambda: make_underline(text_edit))
    menu_bar.add_cascade(label="Edit", menu=edit_menu)

    view_menu = tk.Menu(menu_bar, tearoff=0)
    view_menu.add_command(label="Zoom In", command=lambda: zoom_in(text_edit))
    view_menu.add_command(label="Zoom Out", command=lambda: zoom_out(text_edit))
    menu_bar.add_cascade(label="View", menu=view_menu)

    window.config(menu=menu_bar)

    text_edit.bind("<KeyRelease>", lambda event: update_word_count(text_edit, word_count_label))

    window.mainloop()

main()
