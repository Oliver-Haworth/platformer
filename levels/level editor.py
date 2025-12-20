'''
code is AI generated because it is a tool that allows me to progress the main game development
rather than putting focus on the level editor
'''
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# --- FILE PATH SETUP ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(SCRIPT_DIR, "..", "Assets")

# --- CONFIGURATION ---
ROWS = 20
COLS = 40
TILE_PX = 16 

class PixelEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("LvlEdit - Scrollable Sidebar")
        self.root.resizable(False, False)
        
        self.current_file = None

        # You can now add as many tiles here as you want!
        self.tile_map = {
            ".": {"name": "Eraser", "file": None},
            "1": {"name": "Dirt",   "file": "Dirt.png"},
            "2": {"name": "Grass",  "file": "Grass.png"},
        }

        self.img_data = {}
        for char, info in self.tile_map.items():
            if info["file"]:
                path = os.path.join(ASSETS_DIR, info["file"])
                self.img_data[char] = tk.PhotoImage(file=path) if os.path.exists(path) else None
            else:
                self.img_data[char] = None
        
        self.grid_data = [["." for _ in range(COLS)] for _ in range(ROWS)]
        self.selected_tile = tk.StringVar(value="1")

        self.setup_ui()

    def setup_ui(self):
        # --- SCROLLABLE SIDEBAR LOGIC ---
        # 1. Container for the sidebar area
        side_container = tk.Frame(self.root, bg="#222", width=120)
        side_container.pack(side=tk.LEFT, fill=tk.Y)

        # 2. Canvas and Scrollbar
        self.side_canvas = tk.Canvas(side_container, bg="#222", width=100, highlightthickness=0)
        scrollbar = tk.Scrollbar(side_container, orient="vertical", command=self.side_canvas.yview)
        
        # 3. The actual frame that holds buttons
        self.scrollable_frame = tk.Frame(self.side_canvas, bg="#222")
        
        # Configure the canvas to scroll the frame
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.side_canvas.configure(scrollregion=self.side_canvas.bbox("all"))
        )

        self.side_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.side_canvas.configure(yscrollcommand=scrollbar.set)

        # Pack Canvas and Scrollbar
        self.side_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mousewheel Support
        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

        # --- UI CONTENT (Inside scrollable_frame) ---
        # Tile Selection
        for char, info in self.tile_map.items():
            tk.Radiobutton(self.scrollable_frame, text=info["name"], variable=self.selected_tile, 
                           value=char, indicatoron=0, width=12, font=("Arial", 8)).pack(pady=1, padx=5)

        tk.Frame(self.scrollable_frame, height=20, bg="#222").pack() # Spacer

        # Save/Load Buttons
        tk.Button(self.scrollable_frame, text="Load File", command=self.load_level, font=("Arial", 8)).pack(fill=tk.X, pady=1, padx=5)
        
        self.save_btn = tk.Button(self.scrollable_frame, text="Save (Ctrl+S)", command=self.quick_save, 
                                  bg="#4a4", fg="white", font=("Arial", 8))
        self.save_btn.pack(fill=tk.X, pady=1, padx=5)
        
        tk.Button(self.scrollable_frame, text="Save As...", command=self.save_as, font=("Arial", 8)).pack(fill=tk.X, pady=1, padx=5)

        # --- MAIN CANVAS (The Map) ---
        self.canvas = tk.Canvas(self.root, width=COLS*TILE_PX, height=ROWS*TILE_PX, bg="black", highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT)

        # Draw grid lines
        for c in range(COLS): self.canvas.create_line(c*TILE_PX, 0, c*TILE_PX, ROWS*TILE_PX, fill="#111")
        for r in range(ROWS): self.canvas.create_line(0, r*TILE_PX, COLS*TILE_PX, r*TILE_PX, fill="#111")

        # Bindings
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_click)
        self.root.bind("<Control-s>", lambda e: self.quick_save())

    def _on_mousewheel(self, event):
        # Allow scrolling only if the mouse is over the sidebar area
        self.side_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_click(self, event):
        c, r = event.x // TILE_PX, event.y // TILE_PX
        if 0 <= r < ROWS and 0 <= c < COLS:
            self.grid_data[r][c] = self.selected_tile.get()
            self.redraw_tile(r, c)

    def redraw_tile(self, r, c):
        char = self.grid_data[r][c]
        tags = f"tile_{r}_{c}"
        self.canvas.delete(tags)
        if self.img_data.get(char):
            self.canvas.create_image(c*TILE_PX, r*TILE_PX, image=self.img_data[char], anchor="nw", tags=tags)
        else:
            self.canvas.create_rectangle(c*TILE_PX, r*TILE_PX, (c+1)*TILE_PX, (r+1)*TILE_PX, fill="black", outline="#111", tags=tags)

    def quick_save(self):
        if self.current_file:
            self.perform_save(self.current_file)
            self.root.title(f"LvlEdit - Saved: {os.path.basename(self.current_file)}")
        else:
            self.save_as()

    def save_as(self):
        path = filedialog.asksaveasfilename(initialdir=SCRIPT_DIR, defaultextension=".txt")
        if path:
            self.current_file = path
            self.quick_save()

    def perform_save(self, path):
        with open(path, "w") as f:
            for row in self.grid_data:
                f.write("".join(row) + "\n")

    def load_level(self):
        path = filedialog.askopenfilename(initialdir=SCRIPT_DIR)
        if path:
            self.current_file = path
            self.root.title(f"LvlEdit - Editing: {os.path.basename(path)}")
            with open(path, "r") as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
                for r in range(min(len(lines), ROWS)):
                    for c in range(min(len(lines[r]), COLS)):
                        self.grid_data[r][c] = lines[r][c]
                        self.redraw_tile(r, c)

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelEditor(root)
    root.mainloop()