import tkinter as tk
from tkinter import ttk, messagebox
import json
from ttkbootstrap import Style

# Create the main window
root = tk.Tk()
root.title("story planner")
root.geometry("500x500")
style = Style(theme='journal')
style = ttk.Style()

# Configure the tab font to be bold
style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"))

# Create the notebook to hold the notes
notebook = ttk.Notebook(root, style="TNotebook")

# Load saved notes
notes = {}
try:
    with open("notes.json", "r") as f:
        notes = json.load(f)
except FileNotFoundError:
    pass

# Create the notebook to hold the notes
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create a function to add a new note
def add_note():
    # Create a new tab for the note
    note_frame = ttk.Frame(notebook, padding=10)
    notebook.add(note_frame, text="New Note")
    
    # Create entry widgets for the title and content of the note
    title_label = ttk.Label(note_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")
    
    title_entry = ttk.Entry(note_frame, width=40)
    title_entry.grid(row=0, column=1, padx=10, pady=10)
    
    content_label = ttk.Label(note_frame, text="Content:")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")
    
    content_entry = tk.Text(note_frame, width=40, height=10)
    content_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # Create a function to save the note
    def save_note():
        # Get the title and content of the note
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END)
        
        # Add the note to the notes dictionary
        notes[title] = content.strip()
        
        # Save the notes dictionary to the file
        with open("notes.json", "w") as f:
            json.dump(notes, f)
        
        # Add the note to the notebook
        note_content = tk.Text(notebook, width=50, height=15)
        note_content.insert(tk.END, content)
        note_content.insert(tk.END, "(reopen window to alter this note)")
        notebook.forget(notebook.select())
        notebook.add(note_content, text=title)
     
    # Add a save button to the note frame
    save_button = ttk.Button(note_frame, text="Save", 
                             command=save_note, style="secondary.TButton")
    save_button.grid(row=2, column=1, padx=10, pady=10)
global a

def load_notes():
    try:
        with open("notes.json", "r") as f:
            notes = json.load(f)
        a=[]
        i=0
        for title, content in notes.items():
            a.append("tab"+(str(i)))
            a[i] = tk.Text(notebook, width=50, height=15)
            a[i].insert(tk.END, content)
            notebook.add(a[i], text=title)
            i +=1
        # Add the save button

        save_button_main = ttk.Button(notebook, text="Save", 
                             command=save_note_main, style="secondary.TButton")
        save_button_main.pack(side=tk.BOTTOM, padx=10, pady=10)

    except FileNotFoundError:
        
        # If the file does not exist, do nothing
        pass
    return(a)
def save_note_main():
            # save button in each old tab, so changes don't get lost.
    current_tab = notebook.index(notebook.select())
    note_title = notebook.tab(current_tab, "text")
    content = a[(int(current_tab))].get("1.0", tk.END)

            # Add the note to the notes dictionary
    notes[note_title] = content.strip()
            
            # Save the notes dictionary to the file
    with open("notes.json", "w") as f:
        json.dump(notes, f)
    confirm = messagebox.showinfo("thanks","your note is saved")
# Call the load_notes function when the app starts
a = load_notes()

# Create a function to delete a note
def delete_note():
    # Get the current tab index
    current_tab = notebook.index(notebook.select())
    
    # Get the title of the note to be deleted
    note_title = notebook.tab(current_tab, "text")
    
    # Show a confirmation dialog
    confirm = messagebox.askyesno("Delete Note", 
                                  f"Are you sure you want to delete ({note_title})?")
    
    if confirm:
        # Remove the note from the notebook
        notebook.forget(current_tab)
        
        # Remove the note from the notes dictionary
        notes.pop(note_title)
        
        # Save the notes dictionary to the file
        with open("notes.json", "w") as f:
            json.dump(notes, f)

# Add buttons to the main window
new_button = ttk.Button(root, text="New Note", 
                        command=add_note, style="info.TButton")
new_button.pack(side=tk.LEFT, padx=10, pady=10)

delete_button = ttk.Button(root, text="Delete", 
                           command=delete_note, style="primary.TButton")
delete_button.pack(side=tk.LEFT, padx=10, pady=10)



root.mainloop()
