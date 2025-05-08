import tkinter as tk
import math

# Initialize main window
root = tk.Tk()
root.title("Scientific Calculator")
root.configure(bg="#fceef5")  # Pastel background

# Mode switch variable
is_scientific = tk.BooleanVar(value=False)

# Entry field
entry = tk.Entry(root, width=30, font=('Arial', 20), borderwidth=5, relief="groove",
                 bg="#f8e1f4", fg="#3e3e3e", insertbackground="#3e3e3e")
entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

# Define allowed names for eval (safe use)
allowed_names = {name: getattr(math, name) for name in dir(math) if not name.startswith("__")}
allowed_names.update({'pi': math.pi, 'e': math.e})

# Safe evaluation function
def safe_eval(expr):
    try:
        result = eval(expr, {"__builtins__": None}, allowed_names)
        entry.delete(0, tk.END)
        entry.insert(0, str(result))
    except:
        entry.delete(0, tk.END)
        entry.insert(0, "Error")

# Insert text into entry
def click(btn_text):
    current = entry.get()
    entry.delete(0, tk.END)
    entry.insert(0, current + btn_text)

# Clear entry
def clear():
    entry.delete(0, tk.END)

# Toggle between normal and scientific mode
def toggle_mode():
    is_scientific.set(not is_scientific.get())
    build_buttons()

# Clear all buttons except toggle
def clear_buttons():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button) and widget != toggle_button:
            widget.destroy()
    entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10)

# Build buttons
def build_buttons():
    clear_buttons()
    
    btn_font = ('Arial', 14)
    normal_bg = "#d7f0db"  # pastel green
    sci_bg = "#ffe1e1"     # pastel red
    text_color = "#333333"
    active_bg = "#e4c1f9"  # pastel purple

    # Normal calculator buttons
    normal_buttons = [
        ('7',), ('8',), ('9',), ('/',),
        ('4',), ('5',), ('6',), ('*',),
        ('1',), ('2',), ('3',), ('-',),
        ('0',), ('.',), ('=', lambda: safe_eval(entry.get())), ('+',)
    ]

    # Place normal buttons
    row = 1
    col = 0
    for btn in normal_buttons:
        text = btn[0]
        cmd = btn[1] if len(btn) > 1 else lambda x=text: click(x)
        b = tk.Button(root, text=text, width=5, height=2, command=cmd,
                      font=btn_font, bg=normal_bg, fg=text_color, activebackground=active_bg)
        b.grid(row=row, column=col, padx=3, pady=3)
        col += 1
        if col > 3:
            col = 0
            row += 1

    # Scientific buttons
    if is_scientific.get():
        scientific_buttons = [
            'sin(', 'cos(', 'tan(', 'log(',
            'sqrt(', '(', ')', 'pi',
            '**'
        ]
        sci_row = 1
        sci_col = 4
        for btn in scientific_buttons:
            b = tk.Button(root, text=btn, width=5, height=2, command=lambda x=btn: click(x),
                          font=btn_font, bg=sci_bg, fg=text_color, activebackground=active_bg)
            b.grid(row=sci_row, column=sci_col, padx=3, pady=3)
            sci_row += 1

    # Clear button
    clr_btn = tk.Button(root, text='C', width=5, height=2, command=clear,
                        font=btn_font, bg="#ffcccb", fg="black", activebackground="#f4b6c2")
    clr_btn.grid(row=row, column=0, padx=3, pady=3)

# Toggle button
toggle_button = tk.Button(root, text='Switch Mode', width=20, height=2, command=toggle_mode,
                          font=('Arial', 12), bg="#bde0fe", fg="black", activebackground="#a2d2ff")
toggle_button.grid(row=7, column=1, columnspan=3, pady=10)

# Start the UI
build_buttons()
root.mainloop()
