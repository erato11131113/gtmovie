

import os
import sqlite3
import requests
import random
from tkinter import Tk, Label, ttk, Button, messagebox


API_KEY = "64fa0648d91c600e2817c27be8e2d02c"
BASE_URL = "https://api.themoviedb.org/3"
IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"
DB_PATH = "db.sqlite3"
IMAGE_DIR = os.path.join("movie_images")
os.makedirs(IMAGE_DIR, exist_ok=True)  


# Fetch Movies from TMDb API
def get_movies(page=1):
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
    response = requests.get(url)
    return response.json().get("results", []) if response.status_code == 200 else []


def save_movies_to_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS movies_movie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        description TEXT,
        image TEXT,
        price INTEGER
    )
    """)
    
    for page in range(1, 5):  # Fetch ~80 movies (20 per page)
        movies = get_movies(page)
        for movie in movies:
            image_url = IMAGE_BASE_URL + movie["poster_path"]
            image_path = os.path.join(IMAGE_DIR, f"{movie['title'].replace(' ', '_')}.jpg")
            with open(image_path, "wb") as img_file:
                img_file.write(requests.get(image_url).content)
            price = random.randint(15, 25)  # Set random price between 15 and 25
            cursor.execute("INSERT INTO movies_movie (name, description, image, price) VALUES (?, ?, ?, ?)",
                           (movie["title"], movie["overview"], image_path, price))
    conn.commit()
    conn.close()


class SQLiteEditor:
    def __init__(self, root):
        self.root = root
        self.db_path = DB_PATH  
        self.connect_db()  

        self.root.title("SQLite Database Editor")

        self.table_label = Label(root, text="Select Table:")
        self.table_label.pack()
        
        self.table_dropdown = ttk.Combobox(root, state="readonly")
        self.table_dropdown.pack()
        self.table_dropdown.bind("<<ComboboxSelected>>", self.load_table)
        
        self.tree = ttk.Treeview(root, show="headings")
        self.tree.pack(fill="both", expand=True)
        
        self.save_button = Button(root, text="Save Changes", command=self.save_changes)
        self.save_button.pack()

        self.load_tables()

    def connect_db(self):
        """Re-establish connection to the database if it is closed."""
        if not hasattr(self, "conn") or self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()

    def load_tables(self):
        """Fetch table names."""
        self.connect_db()  
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        self.table_dropdown['values'] = [row[0] for row in self.cursor.fetchall()]
    
    def load_table(self, event):
        """Load the selected table into Treeview."""
        self.connect_db()  
        table_name = self.table_dropdown.get()
        self.current_table = table_name
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = [row[1] for row in self.cursor.fetchall()]

        self.tree.delete(*self.tree.get_children())
        self.tree['columns'] = columns
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        self.cursor.execute(f"SELECT * FROM {table_name};")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)
    
    def save_changes(self):
        """Save modified table data back to SQLite."""
        self.connect_db()  
        table_name = self.current_table
        columns = self.tree['columns']
        rows = [self.tree.item(item, 'values') for item in self.tree.get_children()]
        self.cursor.execute(f"DELETE FROM {table_name};")
        for row in rows:
            placeholders = ', '.join('?' * len(row))
            self.cursor.execute(f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders});", row)
        self.conn.commit()
        messagebox.showinfo("Success", "Changes saved successfully!")

    def close(self):
        """Close the connection properly when the GUI exits."""
        if hasattr(self, "conn") and self.conn:
            self.conn.close()
            self.conn = None  

if __name__ == "__main__":
    save_movies_to_db()
    root = Tk()
    editor = SQLiteEditor(root)
    root.protocol("WM_DELETE_WINDOW", editor.close)
    root.mainloop()
