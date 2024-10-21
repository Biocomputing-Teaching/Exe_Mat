import numpy as np
from ortools.linear_solver import pywraplp

class SimplexSolver:
    def __init__(self, A, b, c, output_file="simplex_output.tex"):
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.c = np.array(c, dtype=float)
        self.m, self.n = self.A.shape
        self.tableau = self.create_tableau()
        self.output_file = output_file
        self.init_output_file()

    def init_output_file(self):
        # Initialize the LaTeX file
        with open(self.output_file, 'w') as f:
            f.write("\\documentclass{article}\n")
            f.write("\\usepackage{amsmath, xcolor}\n")  # Added xcolor for colored text
            f.write("\\usepackage{array}\n")  # For better table formatting
            f.write("\\usepackage{caption}\n")  
            f.write("\\begin{document}\n")
            f.write("\\title{Simplex Method Intermediate Tableaus}\n")
            f.write("\\maketitle\n")

            # Add the initial problem in canonical and standard form
            f.write(self.problem_to_latex())

    def append_to_file(self, content):
        with open(self.output_file, 'a') as f:
            f.write(content)

    def problem_to_latex(self):
        """Write the initial problem in canonical and standard form."""
        # Objective function in LaTeX
        obj_str = "\\section*{Initial Problem}\n"
        obj_str += "\\textbf{Maximize:} \\\\"
        obj_str += "Z = " + " + ".join([f"{self.c[i]}\\(x_{{{i + 1}}}\\)" for i in range(self.n)]) + "\n"
        obj_str += "\\\\\n"

        # Constraints in LaTeX
        obj_str += "\\textbf{Subject to:} \\\\"
        for i in range(self.m):
            constraint = " + ".join([f"{self.A[i, j]}\\(x_{{{j + 1}}}\\)" for j in range(self.n)])
            obj_str += f"{constraint} \\leq {self.b[i]}\\\\\n"
        obj_str += "\\\\\n"

        # Canonical form (with slack variables)
        obj_str += "\\textbf{Canonical Form:} \\\\"
        for i in range(self.m):
            constraint = " + ".join([f"{self.A[i, j]}\\(x_{{{j + 1}}}\\)" for j in range(self.n)])
            obj_str += f"{constraint} + \\(s_{{{i + 1}}}\\) = {self.b[i]}\\\\\n"

        return obj_str + "\n"

    def create_tableau(self):
        # Create the initial tableau
        tableau = np.zeros((self.m + 1, self.n + self.m + 1))

        # Fill the tableau with coefficients of constraints and objective function
        tableau[:self.m, :self.n] = self.A
        tableau[:self.m, self.n:self.n + self.m] = np.eye(self.m)  # Slack variables
        tableau[:self.m, -1] = self.b  # RHS
        tableau[-1, :self.n] = -self.c  # Objective function

        return tableau

    def print_tableau(self, iteration, pivot_row=None, pivot_col=None):
        tableau_str = "\\newline\\begin{minipage}{\\textwidth}\n"
        tableau_str += f"\\captionof{{table}}{{Simplex Tableau after iteration {iteration}}}\n"
        tableau_str += "\\begin{tabular}{|c|" + "c|" * (self.tableau.shape[1]) + "}\n"
        tableau_str += "\\hline\n"

        # Add the headers: variable names (x1, x2, ..., slack variables, RHS)
        headers = [f"\\(x_{{{i + 1}}}\\)" for i in range(self.n)] + [f"\\(s_{{{i + 1}}}\\)" for i in range(self.m)] + ["RHS"]
        tableau_str += "Basic & " + " & ".join(headers) + " \\\\\n"
        tableau_str += "\\hline\n"

        # Add rows of the tableau to LaTeX format
        for i, row in enumerate(self.tableau):
            if i < self.m:
                basic_var_col = np.where(self.tableau[i, :self.n] == 1)[0]
                if len(basic_var_col) == 1:
                    basic_var = f"\\(x_{{{basic_var_col[0] + 1}}}\\)"
                else:
                    basic_var = f"\\(s_{{{i + 1}}}\\)"
                tableau_str += f"\\textcolor{{blue}}{{{basic_var}}} & "
            else:
                tableau_str += "Z & "

            for j, val in enumerate(row):
                if i == self.m and j == pivot_col:
                    # Highlight entering variable (in the objective row)
                    tableau_str += f"\\textbf{{\\textcolor{{red}}{{{val:.2f}}}}} & "
                elif i == pivot_row and j == pivot_col:
                    # Highlight pivot element
                    tableau_str += f"\\textbf{{\\textcolor{{green}}{{{val:.2f}}}}} & "
                else:
                    tableau_str += f"{val:.2f} & "
            tableau_str = tableau_str[:-2] + " \\\\\n"  # Remove trailing "&", add newline
            tableau_str += "\\hline\n"

        tableau_str += "\\end{tabular}\n\\end{minipage}\n"

        # Append the LaTeX formatted tableau to the file
        self.append_to_file(tableau_str)

    def find_pivot_column(self):
        # Find the pivot column (most negative value in the last row)
        last_row = self.tableau[-1, :-1]
        pivot_col = np.argmin(last_row)
        if last_row[pivot_col] >= 0:
            return -1  # Optimal solution reached
        return pivot_col

    def find_pivot_row(self, pivot_col):
        # Find the pivot row (minimum positive ratio of RHS to pivot column element)
        ratios = []
        for i in range(self.m):
            if self.tableau[i, pivot_col] > 0:
                ratios.append(self.tableau[i, -1] / self.tableau[i, pivot_col])
            else:
                ratios.append(np.inf)  # Invalid ratio

        pivot_row = np.argmin(ratios)
        if ratios[pivot_row] == np.inf:
            raise Exception("Linear program is unbounded.")
        return pivot_row

    def perform_pivot(self, pivot_row, pivot_col):
        # Perform row operations to pivot around the selected element
        pivot_element = self.tableau[pivot_row, pivot_col]
        self.tableau[pivot_row] /= pivot_element

        for i in range(self.m + 1):
            if i != pivot_row:
                self.tableau[i] -= self.tableau[i, pivot_col] * self.tableau[pivot_row]

    def solve(self):
        # Continue pivoting until the optimal solution is found
        iteration = 0
        while True:
            # Print and save the current tableau in LaTeX format
            pivot_col = self.find_pivot_column()
            if pivot_col == -1:
                self.append_to_file("Optimal solution reached.\n")
                break

            pivot_row = self.find_pivot_row(pivot_col)
            
            # Log the pivot details (entering and leaving variables)
            entering_var = f"\\(x_{{{pivot_col + 1}}}\\)"
            leaving_var = f"Basic var from row {pivot_row + 1}"
            self.append_to_file(f"Entering variable: {entering_var}, Leaving variable: {leaving_var}\n")

            # Print the tableau with highlighted pivot row and column
            self.print_tableau(iteration, pivot_row, pivot_col)

            # Perform the pivot operation
            self.perform_pivot(pivot_row, pivot_col)
            iteration += 1
        
        # Print the final tableau and optimal value
        self.print_tableau(iteration)

        # Calculate the optimal solution
        solution = np.zeros(self.n)
        for i in range(self.m):
            basic_var_col = np.where(self.tableau[i, :self.n] == 1)[0]
            if len(basic_var_col) == 1:
                solution[basic_var_col[0]] = self.tableau[i, -1]

        # Save the optimal solution and value in LaTeX format
        solution_str = ", ".join([f"\\(x_{{{i + 1}}} = {solution[i]:.2f}\\)" for i in range(self.n)])
        self.append_to_file(f"\\textbf{{Optimal solution:}} {solution_str}\n")
        self.append_to_file(f"\\textbf{{Optimal value (Simplex):}} {-self.tableau[-1, -1]:.2f}\n")
        
        # Solve using ortools to compare the result
        optimal_value_ortools = self.solve_with_ortools()
        self.append_to_file(f"\\textbf{{Optimal value (ORTools):}} {optimal_value_ortools:.2f}\n")
        
        # End the document
        self.append_to_file("\\end{document}")

    def solve_with_ortools(self):
        """Solve the linear program using ORTools to verify the solution."""
        solver = pywraplp.Solver.CreateSolver('GLOP')

        # Define the variables
        variables = [solver.NumVar(0, solver.infinity(), f'x{i+1}') for i in range(self.n)]

        # Add the constraints
        for i in range(self.m):
            constraint = solver.Constraint(-solver.infinity(), self.b[i])
            for j in range(self.n):
                constraint.SetCoefficient(variables[j], self.A[i][j])

        # Define the objective
        objective = solver.Objective()
        for i in range(self.n):
            objective.SetCoefficient(variables[i], self.c[i])
        objective.SetMaximization()

        # Solve the problem
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            return solver.Objective().Value()
        else:
            raise Exception("The ORTools solver did not find an optimal solution.")

# Example usage
A = [[2, 1], [1, 2]]
b = [20, 20]
c = [10, 12]

# Example usage
A = [[1,8,1,2], [3,12,-3,-3], [0,1,1,2]]
b = [9, 18, 1]
c = [1,9,1,2]

# Example usage
A = [[1, 1], [1, -2], [-2,1]]
b = [4, 2, 2]
c = [1, 2]

# Example usage
A = [[2, 1], [2, 3]]
b = [8,12]
c = [3, 1]


solver = SimplexSolver(A, b, c)
solver.solve()
