from core.utils import load_input, print_solution, save_solution, convert_solution_to_symbols, choose_input_file, timed_solver
from core.cnf_generator import CNFGenerator
from core.solver import Solver

def main():
    input_file, output_file = choose_input_file()
    grid = load_input(input_file)

    print("Loaded grid:")
    for row in grid:
        print(row)

    cnf_gen = CNFGenerator(grid)
    clauses, logic_var = cnf_gen.generate_cnf()

    print("\nChọn thuật toán giải:")
    print("1. PySAT")
    print("2. A*")
    print("3. Brute-force")
    print("4. Backtracking")

    algo_choice = input("Nhập số (1 , 2, 3 hoặc 4): ").strip()

    solver = Solver(clauses, logic_var, grid)

    if algo_choice == "1":
        solution = timed_solver(solver.solve_with_pysat, "PySAT")
    elif algo_choice == "2":
        solution = timed_solver(solver.solve_with_a_star_cnf, "A*")
    elif algo_choice == "3":
        solution = timed_solver(solver.solve_with_brute_force, "Brute-force")
    elif algo_choice == "4":
        solution = timed_solver(solver.solve_with_backtracking, "Backtracking")
    else:
        print("Lựa chọn không hợp lệ.")
        return

    if solution:
        symbol_grid = convert_solution_to_symbols(grid, solution)
        print("\nSolution found:")
        print_solution(symbol_grid)
        save_solution(symbol_grid, output_file)
    else:
        print("\nNo solution found.")

if __name__ == "__main__":
    main()
