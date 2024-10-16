from scipy.optimize import minimize

# Define the objective function
def objective(xy):
    x, y = xy
    return -(-x**2 + 4*x*y - 2*y**2)  # Minimization function, so return negative

# Define the constraints
def constraint1(xy):
    x, y = xy
    return 30 - (x + 2*y)  # x + 2y <= 30

def constraint2(xy):
    x, y = xy
    return (x * y) - 50  # xy >= 50

def constraint3(xy):
    x, y = xy
    return (3 * x**2 / 100) + 5 - y  # y <= (3x^2)/100 + 5

# Initial guess
initial_guess = [15, 1]

# Define constraints
constraints = [{'type': 'ineq', 'fun': constraint1},
               {'type': 'ineq', 'fun': constraint2},
               {'type': 'ineq', 'fun': constraint3}]

# Perform the optimization
result = minimize(objective, initial_guess, constraints=constraints)

# Display the results
optimal_x, optimal_y = result.x
print(f"Optimal values: x = {optimal_x:.2f}, y = {optimal_y:.2f}")
print(f"Maximum profit: {-result.fun:.2f}")
