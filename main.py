import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def generate_canvas(zoom=1.0):
    try:
        hoop_size = float(hoop_size_entry.get())  # Inches
        stitch_count = int(stitch_count_entry.get())  # Stitches per inch
        
        if hoop_size <= 0 or stitch_count <= 0:
            messagebox.showerror("Input Error", "Values must be greater than zero.")
            return
        
        diameter = hoop_size * stitch_count  # Total stitch grid diameter
        radius = int(diameter // 2)
        grid_size = int(diameter)
        
        # Create blank image
        img = Image.new('RGBA', (grid_size, grid_size), (255, 255, 255, 255))  # White background
        draw = ImageDraw.Draw(img)
        
        # Draw circular outline
        draw.ellipse([(0, 0), (grid_size - 1, grid_size - 1)], outline=(0, 0, 0, 255))
        
        # Find center
        center_x, center_y = grid_size // 2, grid_size // 2
        red_transparent = (255, 0, 0, 128)  # Red with 50% transparency
        
        # Draw crosshair
        for y in range(grid_size):
            img.putpixel((center_x, y), red_transparent)
        for x in range(grid_size):
            img.putpixel((x, center_y), red_transparent)
        
        # Convert to numpy array
        pixel_data = np.array(img)
        
        # Display image with grid
        fig, ax = plt.subplots(figsize=(6 * zoom, 6 * zoom))
        ax.imshow(pixel_data)
        
        # Add grid lines for stitch counting
        ax.set_xticks(np.arange(-0.5, grid_size, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, grid_size, 1), minor=True)
        ax.grid(which='minor', color='gray', linestyle='-', linewidth=0.5)
        
        # Add labels for every 5th grid line
        major_ticks = np.arange(0, grid_size, 5)
        ax.set_xticks(major_ticks)
        ax.set_yticks(major_ticks)
        ax.set_xticklabels(major_ticks, fontsize=8 * zoom)
        ax.set_yticklabels(major_ticks, fontsize=8 * zoom)
        
        ax.set_frame_on(False)
        
        # Embed in Tkinter
        for widget in canvas_frame.winfo_children():
            widget.destroy()
        
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Close previous figures to prevent memory overflow
        plt.close(fig)
    
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

def zoom_in():
    global zoom_factor
    zoom_factor *= 1.2
    generate_canvas(zoom_factor)

def zoom_out():
    global zoom_factor
    zoom_factor /= 1.2
    generate_canvas(zoom_factor)

def on_closing():
    plt.close('all')  # Close all matplotlib figures
    root.quit()
    root.destroy()

# GUI Setup
root = tk.Tk()
root.title("Cross-Stitch Design Planner")
root.protocol("WM_DELETE_WINDOW", on_closing)  # Ensure program exits completely

zoom_factor = 1.0

# Input Frame
input_frame = ttk.Frame(root, padding=10)
input_frame.pack(side=tk.TOP, fill=tk.X)

ttk.Label(input_frame, text="Hoop Size (inches):").grid(row=0, column=0, padx=5, pady=5)
hoop_size_entry = ttk.Entry(input_frame)
hoop_size_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(input_frame, text="Stitch Count (per inch):").grid(row=1, column=0, padx=5, pady=5)
stitch_count_entry = ttk.Entry(input_frame)
stitch_count_entry.grid(row=1, column=1, padx=5, pady=5)

generate_button = ttk.Button(input_frame, text="Generate Canvas", command=lambda: generate_canvas(zoom_factor))
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

zoom_in_button = ttk.Button(input_frame, text="Zoom In", command=zoom_in)
zoom_in_button.grid(row=3, column=0, padx=5, pady=5)

zoom_out_button = ttk.Button(input_frame, text="Zoom Out", command=zoom_out)
zoom_out_button.grid(row=3, column=1, padx=5, pady=5)

# Canvas Frame
canvas_frame = ttk.Frame(root, padding=10)
canvas_frame.pack(fill=tk.BOTH, expand=True)

root.mainloop()
