import numpy as np
import matplotlib.pyplot as plt

# Define the objective function
def objective_function(x, y):
    return -x**2 + 4*x*y - 2*y**2

# Define the constraints
def constraint1(x, y):
    return 30 - (x + 2*y)  # x + 2y <= 30

def constraint2(x, y):
    return (x * y) - 50  # xy >= 50

def constraint3(x, y):
    return (3 * x**2 / 100) + 5 - y  # y <= (3x^2)/100 + 5

# Create a grid of values for x and y
x = np.linspace(0, 30, 200)
y = np.linspace(0, 30, 200)
X, Y = np.meshgrid(x, y)

# Calculate the objective function values
Z = objective_function(X, Y)

# Set up the plot
plt.figure(figsize=(10, 8))

# Plot the objective function as a filled contour plot (continuous colorbar)
contourf = plt.contourf(X, Y, Z, levels=20, cmap='viridis')  # More levels for smoothness
plt.clabel(contourf, inline=True, fontsize=8)
plt.colorbar(contourf, label='Objective Function Value')

# Plot the constraints as contour levels
# Constraint 1: x + 2y <= 30 (Linear)
plt.contour(X, Y, constraint1(X, Y), levels=[0], colors='red', linewidths=2, linestyles='--')

# Constraint 2: xy >= 50 (Area)
plt.contour(X, Y, constraint2(X, Y), levels=[0], colors='blue', linewidths=2, linestyles='--')

# Constraint 3: y <= (3x^2)/100 + 5 (Nonlinear)
plt.contour(X, Y, constraint3(X, Y), levels=[0], colors='green', linewidths=2, linestyles='--')

# Shade the feasible region
# Use a mask to fill the region that satisfies all constraints
feasible_region = np.logical_and.reduce((
    constraint1(X, Y) >= 0,  # Satisfies x + 2y <= 30
    constraint2(X, Y) >= 0,  # Satisfies xy >= 50
    constraint3(X, Y) >= 0   # Satisfies y <= (3x^2)/100 + 5
))

plt.contourf(X, Y, feasible_region, levels=[0.5, 1], colors='lightblue', alpha=0.5)

# Add a circle at maximum (ontained from the NLO2solution.py; it is 
# straighforward to merge the two scripts, but I intend to simplify 
# the code for individual tasks here)
circle_x, circle_y = 12.86, 8.57
plt.scatter(circle_x, circle_y, color='red', edgecolor='black', s=100, label='Max', marker='o')


# Plot formatting
plt.xlim(0, 30)
plt.ylim(0, 30)
plt.title("Objective Function and Constraints with Shaded Feasible Region")
plt.xlabel("x (units)")
plt.ylabel("y (units)")

# Create a legend for constraints
plt.plot([], [], 'r--', label='x + 2y = 30')
plt.plot([], [], 'b--', label='xy = 50')
plt.plot([], [], 'g--', label='y = (3x^2)/100 + 5')
plt.legend(loc="upper right")

# Show the plot
plt.grid(True)
plt.savefig("../figures/NLO2.png",dpi=300)
#plt.show()