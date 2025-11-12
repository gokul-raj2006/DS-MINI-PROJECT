import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time

# --------------------------------
# 📚 Library Management System
# --------------------------------
books = []

# ------------------------------
# Selection Sort with Animation
# ------------------------------
def selection_sort_visual(tree, key="id"):
    n = len(books)
    for i in range(n - 1):
        min_index = i
        highlight_row(tree, i, "#FFD700")  # yellow highlight current
        for j in range(i + 1, n):
            highlight_row(tree, j, "#FF6666")  # red highlight comparison
            time.sleep(0.3)
            if books[j][key] < books[min_index][key]:
                min_index = j
            reset_highlight(tree, j)
        books[i], books[min_index] = books[min_index], books[i]
        highlight_row(tree, i, "#00FF88")  # green highlight swap
        refresh_table(tree)
        time.sleep(0.4)
        reset_highlight(tree, i)
    refresh_table(tree)
    messagebox.showinfo("✅ Sorting Complete", f"Books sorted by {key.upper()}!")


# ------------------------------
# Helper Functions
# ------------------------------
def highlight_row(tree, index, color):
    """Highlight a specific row."""
    try:
        item = tree.get_children()[index]
        tree.item(item, tags=("highlight",))
        tree.tag_configure("highlight", background=color)
        tree.update_idletasks()
    except IndexError:
        pass


def reset_highlight(tree, index):
    """Reset row highlight to default."""
    try:
        item = tree.get_children()[index]
        tree.item(item, tags=())
        tree.update_idletasks()
    except IndexError:
        pass


def add_book(entry_id, entry_title, entry_author, entry_year, tree):
    try:
        book_id = int(entry_id.get())
        title = entry_title.get()
        author = entry_author.get()
        year = entry_year.get()

        if not title or not author or not year:
            messagebox.showwarning("⚠ Warning", "Please fill all fields!")
            return

        books.append({"id": book_id, "title": title, "author": author, "year": year})
        refresh_table(tree)
        animate_message("✅ Book Added!", "#00FFAA")
    except ValueError:
        messagebox.showerror("❌ Error", "Book ID must be a number!")


def search_book(entry_search, tree):
    query = entry_search.get().lower()
    for row in tree.get_children():
        tree.delete(row)
    for b in books:
        if query in str(b['id']).lower() or query in b['title'].lower():
            tree.insert("", tk.END, values=(b['id'], b['title'], b['author'], b['year']))


def refresh_table(tree):
    for row in tree.get_children():
        tree.delete(row)
    for b in books:
        tree.insert("", tk.END, values=(b['id'], b['title'], b['author'], b['year']))


def sort_books(tree, key):
    threading.Thread(target=selection_sort_visual, args=(tree, key), daemon=True).start()


# ------------------------------
# Fancy Title and UI Animations
# ------------------------------
def animate_title(label):
    colors = ["#00FFAA", "#00D4FF", "#FFD700", "#FF66CC", "#00FF88"]
    i = 0
    while True:
        label.config(fg=colors[i % len(colors)])
        i += 1
        time.sleep(0.4)


def animate_message(text, color):
    popup = tk.Toplevel()
    popup.overrideredirect(True)
    popup.geometry("300x80+600+400")
    popup.config(bg=color)
    lbl = tk.Label(popup, text=text, font=("Arial Rounded MT Bold", 18), fg="black", bg=color)
    lbl.pack(expand=True, fill="both")

    def fade_out():
        alpha = 1.0
        while alpha > 0:
            popup.attributes("-alpha", alpha)
            alpha -= 0.05
            time.sleep(0.05)
        popup.destroy()

    threading.Thread(target=fade_out, daemon=True).start()


# ------------------------------
# GUI Setup
# ------------------------------
def main_ui():
    root = tk.Tk()
    root.title("📚 Library Management System (Animated Pro)")
    root.geometry("1000x650")
    root.configure(bg="#1e1e2f")

    # Title animation
    title_label = tk.Label(root, text="📚 Library Management System", font=("Arial Rounded MT Bold", 28),
                           bg="#1e1e2f", fg="#00FFAA")
    title_label.pack(pady=20)

    threading.Thread(target=animate_title, args=(title_label,), daemon=True).start()

    # Input frame
    frame_input = tk.Frame(root, bg="#29293d", bd=5, relief="ridge")
    frame_input.pack(pady=10, padx=10, fill="x")

    entry_id = tk.Entry(frame_input, width=10, font=("Arial", 14))
    entry_title = tk.Entry(frame_input, width=25, font=("Arial", 14))
    entry_author = tk.Entry(frame_input, width=20, font=("Arial", 14))
    entry_year = tk.Entry(frame_input, width=10, font=("Arial", 14))

    entry_id.grid(row=0, column=0, padx=8, pady=10)
    entry_title.grid(row=0, column=1, padx=8, pady=10)
    entry_author.grid(row=0, column=2, padx=8, pady=10)
    entry_year.grid(row=0, column=3, padx=8, pady=10)

    # Buttons frame
    frame_btn = tk.Frame(root, bg="#1e1e2f")
    frame_btn.pack(pady=10)

    def hover_in(btn):
        btn.config(bg="#00FFAA", fg="black")

    def hover_out(btn):
        btn.config(bg="#33334d", fg="white")

    def make_button(text, cmd):
        b = tk.Button(frame_btn, text=text, font=("Arial", 13, "bold"), bg="#33334d", fg="white",
                      width=15, relief="ridge", command=cmd)
        b.bind("<Enter>", lambda e: hover_in(b))
        b.bind("<Leave>", lambda e: hover_out(b))
        return b

    entry_search = tk.Entry(root, font=("Arial", 14), width=30, bd=3, relief="ridge")
    entry_search.pack(pady=10)

    # Table
    style = ttk.Style()
    style.configure("Treeview", background="#1e1e2f", fieldbackground="#1e1e2f", foreground="white", rowheight=25)
    style.map('Treeview', background=[('selected', '#00FFAA')])

    tree = ttk.Treeview(root, columns=("id", "title", "author", "year"), show="headings", height=14)
    tree.heading("id", text="ID")
    tree.heading("title", text="Title")
    tree.heading("author", text="Author")
    tree.heading("year", text="Year")
    tree.pack(padx=20, pady=10, fill="both", expand=True)

    # Buttons
    btn_add = make_button("➕ Add Book", lambda: add_book(entry_id, entry_title, entry_author, entry_year, tree))
    btn_search = make_button("🔍 Search", lambda: search_book(entry_search, tree))
    btn_sort_id = make_button("🔢 Sort by ID", lambda: sort_books(tree, "id"))
    btn_sort_title = make_button("📖 Sort by Title", lambda: sort_books(tree, "title"))
    btn_exit = make_button("🚪 Exit", root.destroy)

    btn_add.grid(row=0, column=0, padx=10, pady=10)
    btn_search.grid(row=0, column=1, padx=10, pady=10)
    btn_sort_id.grid(row=0, column=2, padx=10, pady=10)
    btn_sort_title.grid(row=0, column=3, padx=10, pady=10)
    btn_exit.grid(row=0, column=4, padx=10, pady=10)

    # Fade-in animation
    root.attributes("-alpha", 0.0)
    def fade_in():
        for i in range(0, 20):
            root.attributes("-alpha", i/20)
            time.sleep(0.05)
    threading.Thread(target=fade_in, daemon=True).start()

    root.mainloop()


# ------------------------------
# Run App
# ------------------------------
if __name__ == "__main__":
    main_ui()
