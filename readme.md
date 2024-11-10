# 2D Heat Equation Solver

This Python script solves the 2D heat equation on a rectangular plate with customizable boundary conditions, heat sources, and sinks. It simulates the temperature distribution over time and saves the output as an animated heatmap GIF.

![Alt text](result.png)

## Parameters
----------

Key configurable parameters:

-   `plate_length`: Side length of the plate grid.
-   `max_iter_time`: Maximum number of time steps.
-   `alpha`: Thermal diffusivity.
-   `u_initial`: Initial temperature of the plate.
-   `condition_type_top/bottom/left/right`: Boundary conditions (either "uniform" or "sinusoidal").
-   `u_top/left/bottom/right`: Temperatures for each boundary.
-   `heat_source`, `heat_sink`: Enable/disable heat sources or sinks.
-   `source_position`: Position of the heat source/sink on the grid.
-   `source_strength`: Strength of the heat source/sink.

## Output
------

-   **`heat_equation_solution.gif`**: Animated GIF showing temperature evolution.

## Requirements
------------

-   Python 3
-   `numpy`
-   `matplotlib`
-   `tqdm`