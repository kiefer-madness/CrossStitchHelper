import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_canvas():
    try:
        hoop_size = float(hoop_size_entry.get())  # Inches
        stitch_count = int(stitch_count_entry.get())  # Stitches per inch
        
        if hoop_size <= 0 or stitch_count <= 0:
            messagebox.showerror("Input Error", "Values must be greater than zero.")
            return
        
        diameter = hoop_size * stitch_count  # Total stitch grid diameter
        radius = int(diameter // 2)
        
        # Create a symmetrical circular grid outline
        grid_size = int(diameter)
        canvas_array = np.zeros((grid_size, grid_size), dtype=int)
        
        for i in range(grid_size):
            for j in range(grid_size):
                distance = (i - radius) ** 2 + (j - radius) ** 2
                if radius**2 - radius <= distance <= radius**2 + radius:
                    canvas_array[i, j] = 1  # White pixels for the circle outline
        
        fig, ax = plt.subplots(figsize=(6,6))
        ax.imshow(canvas_array, cmap='gray_r', extent=[0, grid_size, 0, grid_size])
        
        # Add grid lines for stitch counting
        ax.set_xticks(np.arange(0, grid_size, 1), minor=True)
        ax.set_yticks(np.arange(0, grid_size, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=0.5)
        
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_frame_on(False)
        
        # Embed in Tkinter
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

# GUI Setup
root = tk.Tk()
root.title("Cross-Stitch Design Planner")

# Input Frame
input_frame = ttk.Frame(root, padding=10)
input_frame.pack(side=tk.TOP, fill=tk.X)

ttk.Label(input_frame, text="Hoop Size (inches):").grid(row=0, column=0, padx=5, pady=5)
hoop_size_entry = ttk.Entry(input_frame)
hoop_size_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Stitch Count (per inch):").grid(row=1, column=0, padx=5, pady=5)
stitch_count_entry = ttk.Entry(input_frame)
stitch_count_entry.grid(row=1, column=1, padx=5, pady=5)

generate_button = ttk.Button(input_frame, text="Generate Canvas", command=generate_canvas)
generate_button.grid(row=2, columnspan=2, pady=10)

# Canvas Frame
canvas_frame = ttk.Frame(root, padding=10)
canvas_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
