import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider, Button, TextBox, RadioButtons


# Define grid size and wave parameters
grid_size = 300
center = (grid_size // 2, grid_size // 2)  # Wave origin
frequency = 0.1  # Initial frequency
amplitude = 1.0  # Initial amplitude
velocity_speed = 1.0  # Wave speed
attenuation_coefficient = 0.1  # Initial attenuation coefficient
time = 0  # Elapsed time
selected_point = (center[0], center[1])  # Initially selected point for amplitude tracking
amplitude_history = []  # To store amplitude values over time for the selected point
history_duration = 60.0  # Duration of graph history in seconds

# Initialize wave height (z), velocity, obstacles and wave source grids
z = np.zeros((grid_size, grid_size))
velocity = np.zeros((grid_size, grid_size))
obstacles = np.zeros((grid_size, grid_size), dtype=bool)
wave_sources = np.zeros((grid_size, grid_size), dtype=bool)


# Update wave equation with velocity damping
def update_wave(z, velocity, obstacles, attenuation, dt=0.1, c=1.0):
    """Update wave height and velocity considering damping."""
    laplacian = (
        np.roll(z, 1, axis=0)
        + np.roll(z, -1, axis=0)
        + np.roll(z, 1, axis=1)
        + np.roll(z, -1, axis=1)
        - 4 * z
    )
    laplacian[obstacles] = 0  # No changes at obstacles

    # Update velocity with damping applied continuously
    velocity += (c**2 * laplacian - attenuation * velocity) * dt
    velocity[obstacles] = 0  # Set velocity to 0 at obstacles

    # Update wave height
    z += velocity * dt
    z[obstacles] = 0  # Set height to 0 at obstacles

    # Boundary conditions
    #z[0, :] = z[1, :]
    #z[-1, :] = z[-2, :]
    #z[:, 0] = z[:, 1]
    #z[:, -1] = z[:, -2]

    # Periodic boundary conditions
    #z[0, :] = z[-2, :]
    #z[-1, :] = z[1, :]
    #z[:, 0] = z[:, -2]
    #z[:, -1] = z[:, 1]

    # Absorbing boundary conditions
    z[0, :] = 0
    z[-1, :] = 0
    z[:, 0] = 0
    z[:, -1] = 0

    return z, velocity

draw_obstacles = [True]  # Mutable list to store checkbox state
draw_wave_source = [False]  # Mutable list to store checkbox state

# Wave-specific update function
def update_wave_properties(val):
    """Update wave-specific properties based on slider values."""
    global frequency, amplitude, velocity_speed
    frequency = freq_slider.val
    amplitude = amp_slider.val
    velocity_speed = vel_slider.val


# Medium-specific update function
def update_medium_properties(val):
    """Update medium-specific properties based on slider values."""
    global attenuation_coefficient
    attenuation_coefficient = att_slider.val


# Mouse interaction handlers
drawing = False


def on_mouse_press(event):
    """Handle mouse press for drawing, erasing obstacles, or selecting a point."""
    global drawing, selected_point, mouse_button
    if event.inaxes == ax:  # Ensure the mouse is over the plot window
        if event.button == 1:  # Left button draws obstacles
            drawing = True
            mouse_button = 1
        elif event.button == 3:  # Right button erases obstacles
            drawing = True
            mouse_button = 3
        elif event.button == 2:  # Middle button selects a point
            x, y = int(event.xdata), int(event.ydata)
            if 0 <= x < grid_size and 0 <= y < grid_size:
                selected_point = (y, x)  # Update selected point
        update_grid(event)  # Add obstacles or wave sources immediately on mouse press


def on_mouse_release(event):
    """Handle mouse release to stop drawing or erasing obstacles."""
    global drawing, mouse_button
    drawing = False
    mouse_button = None


def update_grid(event):
    """Update the grid based on mouse position and button state."""
    if event.inaxes == ax:  # Ensure the mouse is over the plot window
        x, y = int(event.xdata), int(event.ydata)
        if 0 <= x < grid_size and 0 <= y < grid_size:
            for i in range(-brush_size + 1, brush_size):
                for j in range(-brush_size + 1, brush_size):
                    if 0 <= x + i < grid_size and 0 <= y + j < grid_size:
                        if mouse_button == 1:  # Left button draws obstacles
                            if draw_obstacles[0]:
                                obstacles[y + j, x + i] = True
                            elif draw_wave_source[0]:
                                wave_sources[y + j, x + i] = True  # Add wave sources
                        elif mouse_button == 3:  # Right button erases obstacles and wave sources
                            obstacles[y + j, x + i] = False
                            wave_sources[y + j, x + i] = False  # Remove wave sources


def on_mouse_motion(event):
    """Handle mouse motion for drawing or erasing obstacles."""
    if drawing:
        update_grid(event)  # Update the grid during mouse motion


def reset_wave(event):
    """Reset the wave simulation."""
    global time, amplitude_history
    time = 0
    amplitude_history = []  # Clear amplitude history
    z[:, :] = 0.0
    velocity[:, :] = 0.0
    obstacles[:, :] = 0
    wave_sources[:, :] = 0
    im.set_array(z)
    line.set_data([], [])  # Clear graph
    ax_graph.relim()
    ax_graph.autoscale_view()
    plt.draw()


graph_enabled = True  # Track whether the graph is enabled


def toggle_graph(event):
    """Toggle the state of graph plotting and visibility."""
    global graph_enabled
    graph_enabled = not graph_enabled
    adjust_layout()  # Adjust layout based on graph visibility

    if graph_enabled:
        ax_graph.set_visible(True)  # Show the graph
        graph_button.label.set_text("Graph: ON")
    else:
        ax_graph.set_visible(False)  # Hide the graph
        graph_button.label.set_text("Graph: OFF")

    plt.draw()  # Redraw the canvas


# Animation update function
def update(frame, im, z, velocity, obstacles, wave_sources):
    global time, amplitude_history, selected_point, graph_enabled

    # Update the wave grid
    z[:], velocity[:] = update_wave(z, velocity, obstacles, attenuation_coefficient, c=velocity_speed)

    time += 0.1

    # Oscillate the wave sources
    z[wave_sources] = amplitude * np.sin(2 * np.pi * frequency * time)

    # Track amplitude at the selected point
    if graph_enabled:
        amplitude_history.append(z[selected_point])

        # Limit graph history to the last 5 seconds
        max_history_length = int(history_duration / 0.1)  # Assuming dt = 0.1
        if len(amplitude_history) > max_history_length:
            amplitude_history = amplitude_history[-max_history_length:]

        # Update the amplitude graph
        x_data = np.arange(len(amplitude_history)) * 0.1  # Time in seconds
        line.set_data(x_data, amplitude_history)  # Update the line plot

        # Dynamically adjust the graph's axes
        ax_graph.relim()  # Recompute data limits based on current data
        ax_graph.autoscale_view()  # Apply updated limits
        fig.canvas.draw_idle()  # Forcefully redraw the canvas

    # Update the grid with obstacles visualization
    image_data = np.copy(z)
    image_data[obstacles] = -1  # Mark obstacles

    # Conditionally highlight the selected point
    if graph_enabled:
        image_data[selected_point] = 1.0  # Highlight selected point

    im.set_array(image_data)  # Update the wave grid image

    return [im, line]


# Function to update brush size from text box
brush_size = 1  # Initial brush size


def update_brush_size(text):
    global brush_size
    try:
        brush_size = int(text)
        if brush_size < 1:
            brush_size = 1
    except ValueError:
        brush_size = 1


def adjust_control_layout():
    """Adjust the positions of the controls to prevent overlap."""
    freq_slider.ax.set_position([0.25, 0.05, 0.25, 0.05])
    amp_slider.ax.set_position([0.25, 0.1, 0.25, 0.05])
    vel_slider.ax.set_position([0.65, 0.05, 0.25, 0.05])
    att_slider.ax.set_position([0.65, 0.1, 0.25, 0.05])
    reset_button_ax.set_position([0.05, 0.05, 0.1, 0.04])
    graph_button_ax.set_position([0.05, 0.1, 0.1, 0.04])
    brush_text_box.ax.set_position([0.11, 0.26, 0.04, 0.04])
    ax_radio.set_position([0.05, 0.15, 0.1, 0.1])  # Position for the checkboxes
    plt.draw()  # Redraw the canvas


def adjust_layout():
    if graph_enabled:
        ax.set_position([0.05, 0.35, 0.4, 0.55])  # Adjust the wave plot position
        ax_graph.set_position([0.55, 0.35, 0.4, 0.55])  # Adjust the graph position
        ax_graph.set_visible(True)  # Show the graph
    else:
        ax.set_position([0.1, 0.3, 0.9, 0.6])  # Center the wave plot
        ax_graph.set_visible(False)  # Hide the graph
    adjust_control_layout()  # Adjust control layout


# Set up plot and animation
fig, (ax, ax_graph) = plt.subplots(1, 2, figsize=(12, 6))
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("Wave Simulation")
im = ax.imshow(z, cmap="seismic", vmin=-1, vmax=1)

ax_graph.set_title("Amplitude at Selected Point")
ax_graph.set_xlabel("Time (s)")
ax_graph.set_ylabel("Amplitude")
line, = ax_graph.plot([], [], lw=1)

# Set up radio button controls
ax_radio = plt.axes([0.05, 0.25, 0.15, 0.15], facecolor='lightgoldenrodyellow')
radio_labels = ["Obstacles", "Wave Source"]
radio_states = [draw_obstacles[0], draw_wave_source[0]]
radio = RadioButtons(ax_radio, radio_labels)


def update_radio(label):
    if label == "Obstacles":
        draw_obstacles[0] = True
        draw_wave_source[0] = False
    elif label == "Wave Source":
        draw_obstacles[0] = False
        draw_wave_source[0] = True


radio.on_clicked(update_radio)

# Create sliders and buttons without positions
ax_controls_freq = plt.axes([0, 0, 0, 0], facecolor='lightgoldenrodyellow')
freq_slider = Slider(ax_controls_freq, 'Frequency', 0.01, 2, valinit=frequency, valstep=0.01)
freq_slider.on_changed(update_wave_properties)

ax_controls_amp = plt.axes([0, 0, 0, 0], facecolor='lightgoldenrodyellow')
amp_slider = Slider(ax_controls_amp, 'Amplitude', -10.0, 10.0, valinit=amplitude, valstep=0.1)
amp_slider.on_changed(update_wave_properties)

ax_controls_vel = plt.axes([0, 0, 0, 0], facecolor='lightgoldenrodyellow')
vel_slider = Slider(ax_controls_vel, 'Velocity', 0.1, 7.0, valinit=velocity_speed, valstep=0.1)
vel_slider.on_changed(update_wave_properties)

ax_controls_att = plt.axes([0, 0, 0, 0], facecolor='lightgoldenrodyellow')
att_slider = Slider(ax_controls_att, 'Attenuation', -1, 1, valinit=attenuation_coefficient, valstep=0.001)
att_slider.on_changed(update_medium_properties)

ax_controls_brush = plt.axes([0, 0, 0, 0], facecolor='lightgoldenrodyellow')
brush_text_box = TextBox(ax_controls_brush, 'Brush Size', initial=str(brush_size))
brush_text_box.on_submit(update_brush_size)

reset_button_ax = plt.axes([0, 0, 0, 0])
reset_button = Button(reset_button_ax, 'Reset', color='red', hovercolor='lightcoral')
reset_button.on_clicked(reset_wave)

graph_button_ax = plt.axes([0, 0, 0, 0])
graph_button = Button(graph_button_ax, 'Graph: ON', color='white', hovercolor='lightblue')
graph_button.on_clicked(toggle_graph)

adjust_control_layout()
adjust_layout()
# Mouse events
fig.canvas.mpl_connect("button_press_event", on_mouse_press)
fig.canvas.mpl_connect("button_release_event", on_mouse_release)
fig.canvas.mpl_connect("motion_notify_event", on_mouse_motion)

# Start animation
ani = FuncAnimation(fig, update, frames=200,
                    fargs=(im, z, velocity, obstacles, wave_sources),
                    interval=20, blit=False)

plt.show()
