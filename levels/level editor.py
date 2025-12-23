'''
code is AI generated because it is a tool that allows me to progress the main game development
rather than putting focus on the level editor
'''
import tkinter as tk
from tkinter import filedialog, messagebox
import os
import random  # Added for randomization

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
        self.root.title("LvlEdit - Randomized Panels")
        self.root.resizable(False, False)
        
        self.current_file = None
        # This stores which specific variant (index) is used at each grid coordinate
        self.tile_variant_map = {} 

        # Define your tile types
        self.tile_map = {
            ".": {"name": "Eraser", "prefix": None},
            "1": {"name": "Panels (Random)", "prefix": "pannel"},
        }

        self.img_data = {}
        self.load_assets()
        
        self.grid_data = [["." for _ in range(COLS)] for _ in range(ROWS)]
        self.selected_tile = tk.StringVar(value="1")

        self.setup_ui()

    def load_assets(self):
        """Finds all files in Assets starting with the prefix and loads them into lists."""
        for char, info in self.tile_map.items():
            self.img_data[char] = []
            prefix = info["prefix"]
            
            if prefix and os.path.exists(ASSETS_DIR):
                # Get all files that start with 'pannel' and end with '.png'
                files = [f for f in os.listdir(ASSETS_DIR) if f.startswith(prefix) and f.endswith(".png")]
                # Sort them so 'pannel1' is index 0, 'pannel2' is index 1, etc.
                files.sort() 
                
                for f in files:
                    path = os.path.join(ASSETS_DIR, f)
                    self.img_data[char].append(tk.PhotoImage(file=path))
            
            # If no images found for a non-eraser tile, set to None list
            if not self.img_data[char]:
                self.img_data[char] = None

    def setup_ui(self):
        side_container = tk.Frame(self.root, bg="#222", width=120)
        side_container.pack(side=tk.LEFT, fill=tk.Y)

        self.side_canvas = tk.Canvas(side_container, bg="#222", width=100, highlightthickness=0)
        scrollbar = tk.Scrollbar(side_container, orient="vertical", command=self.side_canvas.yview)
        
        self.scrollable_frame = tk.Frame(self.side_canvas, bg="#222")
        self.scrollable_frame.bind("<Configure>", lambda e: self.side_canvas.configure(scrollregion=self.side_canvas.bbox("all")))

        self.side_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.side_canvas.configure(yscrollcommand=scrollbar.set)
        self.side_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.root.bind_all("<MouseWheel>", self._on_mousewheel)

        for char, info in self.tile_map.items():
            tk.Radiobutton(self.scrollable_frame, text=info["name"], variable=self.selected_tile, 
                           value=char, indicatoron=0, width=12, font=("Arial", 8)).pack(pady=1, padx=5)

        tk.Frame(self.scrollable_frame, height=20, bg="#222").pack()

        tk.Button(self.scrollable_frame, text="Load File", command=self.load_level, font=("Arial", 8)).pack(fill=tk.X, pady=1, padx=5)
        self.save_btn = tk.Button(self.scrollable_frame, text="Save (Ctrl+S)", command=self.quick_save, 
                                  bg="#4a4", fg="white", font=("Arial", 8))
        self.save_btn.pack(fill=tk.X, pady=1, padx=5)
        tk.Button(self.scrollable_frame, text="Save As...", command=self.save_as, font=("Arial", 8)).pack(fill=tk.X, pady=1, padx=5)

        self.canvas = tk.Canvas(self.root, width=COLS*TILE_PX, height=ROWS*TILE_PX, bg="black", highlightthickness=0)
        self.canvas.pack(side=tk.RIGHT)

        for c in range(COLS): self.canvas.create_line(c*TILE_PX, 0, c*TILE_PX, ROWS*TILE_PX, fill="#111")
        for r in range(ROWS): self.canvas.create_line(0, r*TILE_PX, COLS*TILE_PX, r*TILE_PX, fill="#111")

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_click)
        self.root.bind("<Control-s>", lambda e: self.quick_save())

    def _on_mousewheel(self, event):
        self.side_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def on_click(self, event):
        c, r = event.x // TILE_PX, event.y // TILE_PX
        if 0 <= r < ROWS and 0 <= c < COLS:
            char = self.selected_tile.get()
            self.grid_data[r][c] = char
            
            # If it's a tile with variations, pick a random index
            if self.img_data.get(char) and len(self.img_data[char]) > 0:
                self.tile_variant_map[(r, c)] = random.randint(0, len(self.img_data[char]) - 1)
            else:
                self.tile_variant_map.pop((r, c), None)

            self.redraw_tile(r, c)

    def redraw_tile(self, r, c):
        char = self.grid_data[r][c]
        tags = f"tile_{r}_{c}"
        self.canvas.delete(tags)
        
        variants = self.img_data.get(char)
        
        if variants:
            # Check if we already have a chosen variant for this spot
            variant_idx = self.tile_variant_map.get((r, c))
            
            # If no variant index exists (e.g. after loading a file), pick one
            if variant_idx is None:
                variant_idx = random.randint(0, len(variants) - 1)
                self.tile_variant_map[(r, c)] = variant_idx
                
            img = variants[variant_idx]
            self.canvas.create_image(c*TILE_PX, r*TILE_PX, image=img, anchor="nw", tags=tags)
        else:
            self.canvas.create_rectangle(c*TILE_PX, r*TILE_PX, (c+1)*TILE_PX, (r+1)*TILE_PX, 
                                         fill="black", outline="#111", tags=tags)

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
            self.tile_variant_map.clear() # Reset variants on load so they re-randomize
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