
# Simple Interactive Wave Simulation

This project is an interactive wave simulation tool built using Python's `matplotlib` library. It allows users to visualize and manipulate the behavior of waves in a 2D grid, with support for customizable parameters, obstacles, wave sources, and amplitude tracking.

This simulation runs well on Spyder IDE.
https://www.spyder-ide.org/

## Features

### 1. **Wave Simulation**
- Simulates a 2D wave equation with damping and velocity adjustments.
- Supports oscillating wave sources and interactions with obstacles.
- Provides real-time visualization of wave dynamics.

### 2. **Interactive GUI Elements**
- **Sliders:** Adjust wave frequency, amplitude, velocity, and attenuation.
- **Radio Buttons:** Toggle between drawing obstacles or wave sources.
- **Text Box:** Modify brush size for obstacle and wave source placement.
- **Buttons:** Reset the simulation or toggle amplitude tracking graph visibility.

### 3. **Visualization**
- Displays the wave grid using a `seismic` colormap.
- Tracks and graphs the amplitude history at a user-selected point.

### 4. **Mouse Interaction**
- **Left-click:** Draw obstacles or wave sources.
- **Right-click:** Erase obstacles or wave sources.
- **Middle-click:** Select a point for amplitude tracking.

### 5. **Animation**
- Uses `FuncAnimation` to update wave grid and amplitude history in real time.

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/tuohimetsa/Simple-Interactive-Wave-Simulation.git
    ```

2. Navigate to the project directory:
    ```bash
    cd Simple-Interactive-Wave-Simulation
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

### Controls

#### Sliders
- **Frequency:** Adjusts the oscillation frequency of wave sources.
- **Amplitude:** Changes the amplitude of the wave sources.
- **Velocity:** Modifies the wave propagation speed.
- **Attenuation:** Controls the damping coefficient.

#### Buttons
- **Reset:** Resets the wave grid and clears all obstacles and wave sources.
- **Graph Toggle:** Enables or disables the amplitude tracking graph.

#### Mouse
- **Left-click:** Add obstacles or wave sources (depending on the selected mode).
- **Right-click:** Remove obstacles or wave sources.
- **Middle-click:** Select a point for amplitude tracking.

#### Text Box
- **Brush Size:** Sets the size of the brush for adding or removing obstacles and wave sources.

#### Radio Buttons
- **Obstacles:** Enables obstacle-drawing mode.
- **Wave Source:** Enables wave source-drawing mode.

---

## Customization

You can customize various parameters by modifying the script:
- **Grid Size:** Adjust the `grid_size` variable.
- **History Duration:** Change `history_duration` to control how much amplitude history is displayed.
- **Initial Parameters:** Modify `frequency`, `amplitude`, `velocity_speed`, and `attenuation_coefficient` for different initial settings.

---

## Dependencies

- Python 3.7+
- `matplotlib`
- `numpy`

---

## Contributing

Contributions are welcome! If you have ideas for features or improvements, feel free to open an issue or submit a pull request.

### How to Contribute
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Description of changes"
   ```
4. Push your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

---

This is a work in progress. Also learning to use git properly.
Feel free to reach out with questions or suggestions.

---

