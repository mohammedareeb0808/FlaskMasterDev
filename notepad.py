import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font, colorchooser, ttk
from PIL import Image, ImageTk
import os
import sys

class NotepadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Notepad")
        self.root.geometry("800x600")

        # Initialize default settings
        self.font_family = "Arial"
        self.font_size = 12
        self.font_weight = "normal"
        self.font_slant = "roman"
        self.font_underline = 0
        self.text_color = "black"
        self.bg_color = "white"

        # Create a Text widget with a Scrollbar
        self.text_area = tk.Text(self.root, wrap='word', undo=True, font=(self.font_family, self.font_size),
                                 fg=self.text_color, bg=self.bg_color)
        self.text_area.pack(expand='yes', fill='both')

        self.scroll_y = tk.Scrollbar(self.root, orient='vertical', command=self.text_area.yview)
        self.scroll_y.pack(side='right', fill='y')
        self.text_area.config(yscrollcommand=self.scroll_y.set)

        self.scroll_x = tk.Scrollbar(self.root, orient='horizontal', command=self.text_area.xview)
        self.scroll_x.pack(side='bottom', fill='x')
        self.text_area.config(xscrollcommand=self.scroll_x.set)

        # Create a Menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        self.file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_app)

        # Add Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label="Redo", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        self.edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        self.edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Find", command=self.find_text, accelerator="Ctrl+F")
        self.edit_menu.add_command(label="Replace", command=self.replace_text, accelerator="Ctrl+H")

        # Add Format Menu
        self.format_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Format", menu=self.format_menu)
        self.format_menu.add_command(label="Font", command=self.change_font)
        self.format_menu.add_command(label="Text Color", command=self.change_text_color)
        self.format_menu.add_command(label="Background Color", command=self.change_bg_color)
        self.format_menu.add_separator()
        self.format_menu.add_command(label="Bold", command=self.toggle_bold)
        self.format_menu.add_command(label="Italic", command=self.toggle_italic)
        self.format_menu.add_command(label="Underline", command=self.toggle_underline)
        self.format_menu.add_command(label="Word Wrap", command=self.toggle_word_wrap)

        # Add View Menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        self.view_menu.add_command(label="Toggle Status Bar", command=self.toggle_status_bar)
        self.view_menu.add_command(label="Toggle Line Numbers", command=self.toggle_line_numbers)

        # Add Theme Menu
        self.theme_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Theme", menu=self.theme_menu)
        self.theme_menu.add_command(label="Light", command=lambda: self.change_theme("light"))
        self.theme_menu.add_command(label="Dark", command=lambda: self.change_theme("dark"))

        # Add Settings Menu
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Preferences", command=self.open_preferences)

        # Add Help Menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about)

        # Status Bar
        self.status_bar = tk.Label(self.root, text="Line: 1, Column: 1", anchor='w')
        self.status_bar.pack(side='bottom', fill='x')
        self.text_area.bind('<KeyRelease>', self.update_status_bar)

        # Line Numbers
        self.line_numbers = tk.Text(self.root, width=4, padx=3, takefocus=0, border=0,
                                    background='lightgrey', state='disabled')
        self.line_numbers.pack(side='left', fill='y')

        # Bind events
        self.text_area.bind('<Control-n>', lambda e: self.new_file())
        self.text_area.bind('<Control-o>', lambda e: self.open_file())
        self.text_area.bind('<Control-s>', lambda e: self.save_file())
        self.text_area.bind('<Control-f>', lambda e: self.find_text())
        self.text_area.bind('<Control-h>', lambda e: self.replace_text())

        # Update line numbers
        self.update_line_numbers()

        # Open file if provided as a command-line argument
        if len(sys.argv) > 1:
            file_path = sys.argv[1]
            if os.path.isfile(file_path):
                self.open_file(file_path)

    def new_file(self):
        self.text_area.delete(1.0, tk.END)

    def open_file(self, file_path=None):
        if file_path is None:
            file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                self.text_area.  delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.root.title(f"Enhanced Notepad - {os.path.basename(file_path)}")

    def save_file(self):
        if self.root.title() == "Enhanced Notepad":
            self.save_as_file()
        else:
            file_path = self.root.title().split(" - ")[1]
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.root.title(f"Enhanced Notepad - {os.path.basename(file_path)}")

    def exit_app(self):
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            self.root.quit()

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def find_text(self):
        search_term = simpledialog.askstring("Find", "Enter text to find:")
        if search_term:
            start_pos = self.text_area.search(search_term, 1.0, tk.END)
            if start_pos:
                end_pos = f"{start_pos}+{len(search_term)}c"
                self.text_area.tag_add('search', start_pos, end_pos)
                self.text_area.tag_config('search', background='yellow')
                self.text_area.see(start_pos)
            else:
                messagebox.showinfo("Find", f"'{search_term}' not found.")

    def replace_text(self):
        search_term = simpledialog.askstring("Replace", "Enter text to find:")
        if search_term:
            replace_term = simpledialog.askstring("Replace", "Enter replacement text:")
            if replace_term:
                content = self.text_area.get(1.0, tk.END)
                new_content = content.replace(search_term, replace_term)
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, new_content)

    def change_font(self):
        font_tuple = font.families()
        font_family = simpledialog.askstring("Font", "Enter font name:", initialvalue=self.font_family)
        font_size = simpledialog.askinteger("Font Size", "Enter font size:", initialvalue=self.font_size)

        if font_family in font_tuple and font_size:
            self.font_family = font_family
            self.font_size = font_size
            self.text_area.config(font=(self.font_family, self.font_size))

    def change_text_color(self):
        color = colorchooser.askcolor(initialcolor=self.text_color)[1]
        if color:
            self.text_color = color
            self.text_area.config(fg=self.text_color)

    def change_bg_color(self):
        color = colorchooser.askcolor(initialcolor=self.bg_color)[1]
        if color:
            self.bg_color = color
            self.text_area.config(bg=self.bg_color)

    def toggle_bold(self):
        self.font_weight = "bold" if self.font_weight == "normal" else "normal"
        self.update_font_style()

    def toggle_italic(self):
        self.font_slant = "italic" if self.font_slant == "roman" else "roman"
        self.update_font_style()

    def toggle_underline(self):
        self.font_underline = 1 if self.font_underline == 0 else 0
        self.update_font_style()

    def update_font_style(self):
        self.text_area.config(font=(self.font_family, self.font_size, self.font_weight, self.font_slant, 'underline' if self.font_underline else ''))

    def toggle_word_wrap(self):
        current_wrap = self.text_area.cget('wrap')
        new_wrap = 'word' if current_wrap == 'none' else 'none'
        self.text_area.config(wrap=new_wrap)

    def toggle_status_bar(self):
        if self.status_bar.winfo_ismapped():
            self.status_bar.pack_forget()
        else:
            self.status_bar.pack(side='bottom', fill='x')

    def toggle_line_numbers(self):
        if self.line_numbers.winfo_ismapped():
            self.line_numbers.pack_forget()
        else:
            self.line_numbers.pack(side='left', fill='y')
            self.update_line_numbers()

    def change_theme(self, theme):
        if theme == "light":
            self.root.config(bg='white')
            self.text_area.config(bg='white', fg='black')
            self.line_numbers.config(bg='lightgrey')
        elif theme == "dark":
            self.root.config(bg='black')
            self.text_area.config(bg='black', fg='white')
            self.line_numbers.config(bg='darkgrey')

    def open_preferences(self):
        preferences_window = tk.Toplevel(self.root)
        preferences_window.title("Preferences")
        preferences_window.geometry("300x300")

        tk.Label(preferences_window, text="Font Family:").pack(pady=5)
        self.font_family_entry = tk.Entry(preferences_window)
        self.font_family_entry.pack(pady=5)
        self.font_family_entry.insert(0, self.font_family)

        tk.Label(preferences_window, text="Font Size:").pack(pady=5)
        self.font_size_entry = tk.Entry(preferences_window)
        self.font_size_entry.pack(pady=5)
        self.font_size_entry.insert(0, self.font_size)

        tk.Label(preferences_window, text="Text Color:").pack(pady=5)
        self.text_color_button = tk.Button(preferences_window, bg=self.text_color, command=self.change_text_color)
        self.text_color_button.pack(pady=5)

        tk.Label(preferences_window, text="Background Color:").pack(pady=5)
        self.bg_color_button = tk.Button(preferences_window, bg=self.bg_color, command=self.change_bg_color)
        self.bg_color_button.pack(pady=5)

        self.spell_check_var = tk.BooleanVar(value=self.spell_check_enabled)
        tk.Checkbutton(preferences_window, text="Enable Spell Check", variable=self.spell_check_var).pack(pady=10)

        save_button = tk.Button(preferences_window, text="Save", command=self.save_preferences)
        save_button.pack(pady=10)

    def save_preferences(self):
        try:
            font_family = self.font_family_entry.get()
            font_size = int(self.font_size_entry.get())
            self.font_family = font_family
            self.font_size = font_size
            self.text_area.config(font=(self.font_family, self.font_size))

            self.spell_check_enabled = self.spell_check_var.get()

            # Update text color and background color
            self.text_area.config(fg=self.text_color, bg=self.bg_color)

        except ValueError:
            messagebox.showerror("Invalid Input", "Font size must be an integer.")

    def show_about(self):
        messagebox.showinfo("About", "Enhanced Notepad Application\nVersion 1.0\nby ShaikhMohammedAreeb  ")

    def update_status_bar(self, event=None):
        row, col = self.text_area.index(tk.INSERT).split('.')
        self.status_bar.config(text=f"Line: {row}, Column: {col}")

    def update_line_numbers(self):
        if self.line_numbers.winfo_ismapped():
            self.line_numbers.config(state='normal')
            self.line_numbers.delete(1.0, tk.END)
            lines = int(self.text_area.index('end-1c').split('.')[0])
            for i in range(1, lines + 1):
                self.line_numbers.insert(tk.END, f"{i}\n")
            self.line_numbers.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = NotepadApp(root)
    root.mainloop()
