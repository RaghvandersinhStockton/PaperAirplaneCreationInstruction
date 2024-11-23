import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Define A4 paper dimensions in cm (scaled for the plot)
width = 21  # A4 paper width in cm (scaled for the plot)
height = 29.7  # A4 paper height in cm (scaled for the plot)

# Create initial 3D coordinates for the unfolded paper (flat rectangle)
x_init = np.array([0, width, width, 0, 0])  # x-coordinates of the paper
y_init = np.array([0, 0, height, height, 0])  # y-coordinates of the paper
z_init = np.zeros_like(x_init)  # z-coordinates (flat in the beginning)

# Create the figure and 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(0, width)
ax.set_ylim(0, height)
ax.set_zlim(0, 1)

# Create the initial 3D plot for the unfolded paper
paper_line, = ax.plot(x_init, y_init, z_init, 'b-', lw=3)

# Create the line for the midline (crease)
midline, = ax.plot([width/2, width/2], [0, height], [0, 0], 'r--', lw=2)


# Function to simulate the folding of the paper in 3D
def update(frame):
    # Control the folding progress (right side moving to the left)
    fold_position = frame*(width/50)  # Controls the folding progress

    # Depth effect for 3D: simulate folding closer to the viewer
    depth_effect = fold_position*0.05  # Depth shift for 3D effect (increasing as fold progresses)

    # Update the x, y, and z coordinates for the folded paper
    x_folded = np.copy(x_init)
    y_folded = np.copy(y_init)
    z_folded = np.copy(z_init)

    if fold_position < width/2:
        # Apply perspective shift for the fold (Z-axis) as the paper folds over
        x_folded[1] = width/2 - fold_position  # Right side moves to the left
        x_folded[2] = width/2 - fold_position  # Same for top right corner
        x_folded[3] = width/2 - fold_position  # Same for bottom right corner

        # Simulate a slight Z-depth effect (making it appear as if folding in 3D)
        z_folded[1] = depth_effect
        z_folded[2] = depth_effect
        z_folded[3] = depth_effect

    # Update the plot with new x, y, z coordinates
    paper_line.set_xdata(x_folded)
    paper_line.set_ydata(y_folded)
    paper_line.set_3d_properties(z_folded)

    # Update the midline (crease) in 3D
    if fold_position < width/2:
        midline.set_xdata([width/2 - fold_position, width/2 - fold_position])
        midline.set_ydata([0, height])
        midline.set_3d_properties([depth_effect, depth_effect])
    else:
        midline.set_xdata([width/2, width/2])
        midline.set_3d_properties([0, 0])

    return paper_line, midline


# Create the animation that folds the paper in 50 frames
ani = FuncAnimation(fig, update, frames=50, interval=100, blit=True)

# Display the animation
plt.title("Folding Paper in 3D - Right Edges to Left")
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
