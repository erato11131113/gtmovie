import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class SQLiteEditor:
    def __init__(self, root, db_path):
        self.root = root
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.root.title("SQLite Database Editor")

        # Table Selection Dropdown
        self.table_label = tk.Label(root, text="Select Table:")
        self.table_label.pack(pady=5)

        self.table_dropdown = ttk.Combobox(root, state="readonly")
        self.table_dropdown.pack(pady=5)
        self.table_dropdown.bind("<<ComboboxSelected>>", self.load_table)

        # Treeview for Table Data
        self.tree = ttk.Treeview(root, show="headings")
        self.tree.pack(pady=5, fill=tk.BOTH, expand=True)

        # Save Button
        self.save_button = tk.Button(root, text="Save Changes", command=self.save_changes)
        self.save_button.pack(pady=10)

        self.load_tables()

    def load_tables(self):
        """Load all table names into the dropdown."""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in self.cursor.fetchall()]
        self.table_dropdown['values'] = tables

    def load_table(self, event):
        """Load the selected table into the Treeview."""
        table_name = self.table_dropdown.get()
        self.current_table = table_name

        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in self.cursor.fetchall()]

        # Clear existing tree
        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = columns

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.cursor.execute(f"SELECT * FROM {table_name};")
        rows = self.cursor.fetchall()
        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def save_changes(self):
        """Save changes made in the Treeview back to the database."""
        try:
            # Get all data from the Treeview
            table_name = self.current_table
            columns = self.tree['columns']
            rows = [self.tree.item(item, 'values') for item in self.tree.get_children()]

            # Clear and repopulate the table
            self.cursor.execute(f"DELETE FROM {table_name};")
            for row in rows:
                placeholders = ', '.join('?' for _ in row)
                self.cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders});", row)

            self.conn.commit()
            messagebox.showinfo("Success", "Changes saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def close(self):
        self.conn.close()

if __name__ == "__main__":
    db_path = "db.sqlite3"  # Replace with your SQLite file path
    root = tk.Tk()
    editor = SQLiteEditor(root, db_path)
    root.protocol("WM_DELETE_WINDOW", editor.close)
    root.mainloop()
