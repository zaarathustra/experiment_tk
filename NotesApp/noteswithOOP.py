import tkinter as tk
from tkinter import ttk, messagebox
import json
from ttkbootstrap import Style

class NotesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Story Planner")
        self.root.geometry("500x500")
        self.style = Style(theme='journal')

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.notes = {}
        self.load_notes()

        new_button = ttk.Button(root, text="New Note", command=self.add_note, style="info.TButton")
        new_button.pack(side=tk.LEFT, padx=10, pady=10)

        delete_button = ttk.Button(root, text="Delete", command=self.delete_note, style="primary.TButton")
        delete_button.pack(side=tk.LEFT, padx=10, pady=10)

    def add_note(self):
        note_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(note_frame, text="New Note")

        title_label = ttk.Label(note_frame, text="Title:")
        title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        title_entry = ttk.Entry(note_frame, width=40)
        title_entry.grid(row=0, column=1, padx=10, pady=10)

        content_label = ttk.Label(note_frame, text="Content:")
        content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        content_entry = tk.Text(note_frame, width=40, height=10)
        content_entry.grid(row=1, column=1, padx=10, pady=10)

        save_button = ttk.Button(note_frame, text="Save", command=lambda: self.save_note(title_entry, content_entry),
                                 style="secondary.TButton")
        save_button.grid(row=2, column=1, padx=10, pady=10)

    def save_note(self, title_entry, content_entry):
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)
        self.notes[title] = content.strip()
        
        with open("notes.json", "w") as f:
            json.dump(self.notes, f)
        
        note_content = tk.Text(self.notebook, width=50, height=15)
        note_content.insert(tk.END, content)
        note_content.insert(tk.END, "(reopen window to alter this note)")
        self.notebook.forget(self.notebook.select())
        self.notebook.add(note_content, text=title)

    def load_notes(self):
        try:
            with open("notes.json", "r") as f:
                self.notes = json.load(f)
            for title, content in self.notes.items():
                note_content = tk.Text(self.notebook, width=50, height=15)
                note_content.insert(tk.END, content)
                self.notebook.add(note_content, text=title)

            save_button_main = ttk.Button(self.notebook, text="Save", command=self.save_note_main, style="secondary.TButton")
            save_button_main.pack(side=tk.BOTTOM, padx=10, pady=10)

        except FileNotFoundError:
            pass

    def save_note_main(self):
        current_tab = self.notebook.index(self.notebook.select())
        note_title = self.notebook.tab(current_tab, "text")
        content = self.notebook.winfo_children()[current_tab].get("1.0", tk.END)

        self.notes[note_title] = content.strip()

        with open("notes.json", "w") as f:
            json.dump(self.notes, f)
        confirm = messagebox.showinfo("Thanks", "Your note is saved")

    def delete_note(self):
        current_tab = self.notebook.index(self.notebook.select())
        note_title = self.notebook.tab(current_tab, "text")
        confirm = messagebox.askyesno("Delete Note", f"Are you sure you want to delete ({note_title})?")

        if confirm:
            self.notebook.forget(current_tab)
            self.notes.pop(note_title)

            with open("notes.json", "w") as f:
                json.dump(self.notes, f)

if __name__ == "__main__":
    root = tk.Tk()
    app = NotesApp(root)
    root.mainloop()
