import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from tqdm import tqdm  # Import tqdm for progress bar

print("2D heat equation solver")

# Constants and grid size
plate_length = 50  # mm
max_iter_time = 1000  # s
alpha = 4
delta_x = 0.5  # mm
delta_t = (delta_x ** 2) / (4 * alpha)
gamma = (alpha * delta_t) / (delta_x ** 2)
#gamma = 0.05

u_initial = 20

# Boundary conditions
condition_type_top = "uniform" # uniform  # sinusoidal
condition_type_bottom = "sinusoidal" 
condition_type_left = "uniform" 
condition_type_right = "uniform" 
u_top = 30.0
u_left = 30.0
u_bottom = 100.0
u_right = 30.0

# Heat source/sink settings
heat_source = "False"
heat_sink = "True"
source_position = (15, 25)  # Position where heat is added 
source_strength = 50.0  # Amount of heat  
# Initialize the temperature grid
u = np.empty((max_iter_time, plate_length, plate_length))
# Set the initial temperature distribution
u.fill(u_initial)

# Function to apply boundary conditions
def apply_boundary_conditions(u, condition_type_top, condition_type_bottom, 
                               condition_type_left, condition_type_right):

    x, y = source_position

    """
    Apply boundary conditions to the grid for all time steps.
    """
    if condition_type_top == "uniform":
        u[:, -1, :] = u_top  # Top boundary (uniform temperature)
    elif condition_type_top == "sinusoidal":
        x = np.arange(plate_length)
        u[:, -1, :] =  u_top + u_top * np.sin(np.pi * x / plate_length)  # Top boundary (sinusoidal)
    
    if condition_type_bottom == "uniform":
        u[:, 0, :] = u_bottom  # Bottom boundary (uniform temperature)
    elif condition_type_bottom == "sinusoidal":
        x = np.arange(plate_length)
        u[:, 0, :] = u_bottom + u_bottom * np.sin(np.pi * x / plate_length)  # Bottom boundary (sinusoidal)

    if condition_type_left == "uniform":
        u[:, :, 0] = u_left  # Left boundary (uniform temperature)
    elif condition_type_left == "sinusoidal":
        y = np.arange(plate_length)
        u[:, :, 0] = u_left + u_left * np.sin(np.pi * y / plate_length)  # Left boundary (sinusoidal)

    if condition_type_right == "uniform":
        u[:, :, -1] = u_right  # Right boundary (uniform temperature)
    elif condition_type_right == "sinusoidal":
        y = np.arange(plate_length)
        u[:, :, -1] = u_right + u_right * np.sin(np.pi * y / plate_length)  # Right boundary (sinusoidal)

    return u



# Function to add or remove heat source/sink
def apply_heat_source_sink(u, k, heat_source, heat_sink, position, strength):
    x, y = position
    
    if heat_source == "True":
        x, y = position
        u[k, x, y] += strength
    if heat_sink == "True":
        x, y = position
        u[k, x, y] -= strength

    return u

# Function to calculate temperature distribution
def calculate(u, heat_source, heat_sink):
        
    for k in tqdm(range(max_iter_time - 1), desc="Calculating temperature distribution"):
        u = apply_heat_source_sink(u, k, heat_source, heat_sink, source_position, source_strength)

        u[k + 1, 1:-1, 1:-1] = gamma * (u[k, 2:, 1:-1] + u[k, :-2, 1:-1] + u[k, 1:-1, 2:] + u[k, 1:-1, :-2] - 4 * u[k, 1:-1, 1:-1]) + u[k, 1:-1, 1:-1]

                # Apply boundary conditions
        u = apply_boundary_conditions(u, condition_type_top, 
                               condition_type_bottom, 
                               condition_type_left, 
                               condition_type_right)
    

    return u

# Visualization function for heatmap
def plotheatmap(u_k, k):
    plt.clf()

    plt.title(f"Temperature at t = {k*delta_t:.3f} unit time")
    plt.xlabel("x")
    plt.ylabel("y")

    # This is to plot u_k (u at time-step k)
    plt.pcolormesh(u_k, cmap=plt.cm.jet, vmin=0, vmax=200)
    plt.colorbar().set_label('Temperature (°C)')

    return plt


u = calculate(u, heat_source, heat_sink)

# Animation function
def animate(k):
    plotheatmap(u[k], k)

# Set up the animation
fig = plt.figure()
anim = animation.FuncAnimation(fig, animate, frames=max_iter_time, interval=1, repeat=False)

# Save the animation as a GIF
writergif = PillowWriter()
print("Saving to heat_equation_solution.gif ...")
anim.save("heat_equation_solution.gif", writer=writergif)
