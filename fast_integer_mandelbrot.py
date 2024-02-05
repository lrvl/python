#!/bin/env python
import numpy as np
import tkinter as tk
import tkinter.font as tkfont
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numba
import time

# Define the parameters for the initial fractal
MAX_WIDTH, MAX_HEIGHT = 1024, 1024  # Adjust this as per your highest quality requirement
MIN_WIDTH, MIN_HEIGHT = 128, 128  # Minimum resolution for fastest rendering
INITIAL_ZOOM_SPEED_MULTIPLIER = 1.0  # This should match your initial setup
width, height = MAX_WIDTH, MAX_HEIGHT
max_iterations = 512
zoom_speed = 0  # Initial zoom speed
zoom_factor = 1.0
zoom_speed_multiplier = INITIAL_ZOOM_SPEED_MULTIPLIER
zooming_in = False
zooming_out = False
running = True

ESCAPE_RADIUS_SQUARED = 4.0
COLOR_CONVERSION_FACTOR = 0.16
# Define initial fractal parameters as global constants for easy reset
INITIAL_XMIN, INITIAL_XMAX = -2.0, 1.0
INITIAL_YMIN, INITIAL_YMAX = -1.5, 1.5
xmin, xmax = INITIAL_XMIN, INITIAL_XMAX
ymin, ymax = INITIAL_YMIN, INITIAL_YMAX

# Create an array to store the image
image = np.zeros((height, width), dtype=np.uint8)

@numba.njit(parallel=True)
def mandelbrot_set(image, width, height, max_iterations, xmin, xmax, ymin, ymax):
    scale_x = (xmax - xmin) / (width - 1)
    scale_y = (ymax - ymin) / (height - 1)

    for y in numba.prange(height):
        cy = ymin + y * scale_y
        for x in numba.prange(width):
            cx = xmin + x * scale_x
            zx, zy = 0.0, 0.0
            iteration = 0

            while iteration < max_iterations:
                zx2, zy2 = zx * zx, zy * zy
                if zx2 + zy2 > ESCAPE_RADIUS_SQUARED:
                    break
                zy, zx = 2.0 * zx * zy + cy, zx2 - zy2 + cx
                iteration += 1

            if iteration < max_iterations:
                log_zn = np.log(zx2 + zy2) / 2
                nu = np.log(log_zn / np.log(2)) / np.log(2)
                iteration = iteration + 1 - nu

            image[y, x] = max(np.sin(COLOR_CONVERSION_FACTOR * iteration) * 230, 0)

# Initialize the Mandelbrot fractal
mandelbrot_set(image, width, height, max_iterations, xmin, xmax, ymin, ymax)

# GUI Setup
app = tk.Tk()
app.title("Mandelbrot Fractal Zoomer")
app.configure(bg='black')

fig = Figure(figsize=(5, 5), dpi=100, facecolor='black')
canvas = FigureCanvasTkAgg(fig, master=app)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

ax = fig.add_subplot(111)
ax.imshow(image, cmap='magma', extent=[xmin, xmax, ymin, ymax])
ax.axis('off')  # Hide axes
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Remove padding and margins

def calculate_resolution(zoom_speed_multiplier):
    # Calculate dynamic resolution based on zoom_speed_multiplier
    scale_factor = (zoom_speed_multiplier - 1) * 100

    # Calculate dynamic width and height based on scale_factor
    dynamic_width = max(int(MAX_WIDTH / (1 + scale_factor)), MIN_WIDTH)
    dynamic_height = max(int(MAX_HEIGHT / (1 + scale_factor)), MIN_HEIGHT)

    #print("dyn_width=%i dyn_height=%i" % (dynamic_width, dynamic_height))
    return dynamic_width, dynamic_height

def adjust_resolution(zoom_speed_multiplier):
    global width, height, image
    width, height = calculate_resolution(zoom_speed_multiplier)

    # Adjust the image array to the new resolution
    image = np.zeros((height, width), dtype=np.uint8)

def update_fractal():
    global image, width, height, last_update_time
    mandelbrot_set(image, width, height, max_iterations, xmin, xmax, ymin, ymax)
    ax.images[0].set_data(image)
    canvas.draw_idle()

def start_zoom_in():
    global zooming_in, zoom_speed_multiplier
    zooming_in = True
    zoom_speed_multiplier = INITIAL_ZOOM_SPEED_MULTIPLIER  # Reset speed multiplier

def start_zoom_out():
    global zooming_out, zoom_speed_multiplier
    zooming_out = True
    zoom_speed_multiplier = INITIAL_ZOOM_SPEED_MULTIPLIER  # Reset speed multiplier

def stop_zoom_in():
    global zooming_in
    zooming_in = False
    zoom_speed_multiplier = INITIAL_ZOOM_SPEED_MULTIPLIER  # Reset speed multiplier

def increase_zoom_speed():
    global zoom_speed_multiplier
    zoom_speed_multiplier *= 1.001
    #print(zoom_speed_multiplier)

def stop_zoom_out():
    global zooming_out
    zooming_out = False
    zoom_speed_multiplier = INITIAL_ZOOM_SPEED_MULTIPLIER  # Reset speed multiplier

def zoom():
    global zoom_factor, zooming_in, zooming_out, xmin, xmax, ymin, ymax
    if not zooming_in and not zooming_out:
        zoom_factor = 1
        return
    if zooming_in:
        zoom_factor *= 1.001 ** zoom_speed_multiplier
    elif zooming_out:
        zoom_factor /= 1.001 ** zoom_speed_multiplier

    # Adjust resolution based on zoom speed
    adjust_resolution(zoom_speed_multiplier)

    x_mid = (xmin + xmax) / 2
    y_mid = (ymin + ymax) / 2
    x_range = (xmax - xmin) * zoom_factor
    y_range = (ymax - ymin) * zoom_factor
    xmin, xmax = x_mid - x_range / 2, x_mid + x_range / 2
    ymin, ymax = y_mid - y_range / 2, y_mid + y_range / 2
    update_fractal()

def on_key_press(event):
    global zoom_speed_multiplier, zooming_in, zooming_out, xmin, xmax, ymin, ymax, width, height
    if event.char == '[':
        if zooming_in:
            increase_zoom_speed()
        else:
            start_zoom_in()
            stop_zoom_out()  # Stop zooming out when zooming in
    elif event.char == ']':
        if zooming_out:
            increase_zoom_speed()
        else:
            start_zoom_out()
            stop_zoom_in()  # Stop zooming in when zooming out
    elif event.char == 'a':
        # Pan left
        x_range = (xmax - xmin)
        xmin -= x_range * 0.1
        xmax -= x_range * 0.1
        update_fractal()
    elif event.char == 'd':
        # Pan right
        x_range = (xmax - xmin)
        xmin += x_range * 0.1
        xmax += x_range * 0.1
        update_fractal()
    elif event.char == 'w':
        # Pan up
        y_range = (ymax - ymin)
        ymin -= y_range * 0.1
        ymax -= y_range * 0.1
        update_fractal()
    elif event.char == 's':
        # Pan down
        y_range = (ymax - ymin)
        ymin += y_range * 0.1
        ymax += y_range * 0.1
        update_fractal()
    elif event.char == 'p':  # Check if 'p' is pressed
        # Stop zooming
        stop_zoom_in()
        stop_zoom_out()
        zoom_speed_multiplier = INITIAL_ZOOM_SPEED_MULTIPLIER
        adjust_resolution(zoom_speed_multiplier)
        update_fractal()  # Update the fractal with the new resolution
    elif event.char == 'q':
        global running
        running = False

app.bind("<KeyPress>", on_key_press)

if __name__ == '__main__':
    
    # Limit the frame rate to approximately 30 FPS
    target_fps = 30
    frame_time = 1.0 / target_fps

    try:
        while running:
            start_time = time.time()
            zoom()
            update_fractal()
            app.update()  # Update the GUI
            elapsed_time = time.time() - start_time
            
            # Sleep to achieve the target frame rate
            if elapsed_time < frame_time:
                time.sleep(frame_time - elapsed_time)
    except Exception as e:
        print("Exiting", e)
    finally:
        app.destroy()
