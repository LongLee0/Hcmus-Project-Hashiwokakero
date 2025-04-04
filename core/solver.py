from pysat.solvers import Glucose3
from core.bridge import Bridge
from core.Astar import AStarCNFSolver
from core.utils import is_connected

class Solver:
    def __init__(self, clauses, logic_var, grid):
        self.clauses = clauses
        self.logic_var = logic_var
        self.grid = grid

    def solve_with_pysat(self):
        solver = Glucose3()
        for clause in self.clauses:
            solver.add_clause(clause)

        islands = [(i, j) for i, row in enumerate(self.grid) for j, cell in enumerate(row) if cell > 0]
        attempt = 0

        while solver.solve():
            attempt += 1
            model = solver.get_model()
            bridges = self.extract_bridges(model, verbose=False)

            print(f"[✓] Tìm được lời giải lần {attempt}, kiểm tra liên thông...")

            if is_connected(islands, bridges):
                print("[✓] Lời giải liên thông hợp lệ.")
                return bridges

            print("[x] Lời giải không liên thông, thử lại...")
            solver.add_clause([-lit for lit in model if lit > 0])

        print("[x] Không tìm được lời giải liên thông.")
        return None

    def solve_with_a_star_cnf(self):
        print("[+] Đang giải bằng A* trên CNF (logic-level)...")
        rejected = set()
        attempt = 0

        while True:
            astar_solver = AStarCNFSolver(self.clauses, self.logic_var, verbose=(attempt == 0), exclude_assignments=rejected)
            assignment = astar_solver.solve()
            attempt += 1

            if not assignment:
                print("[x] Không tìm được lời giải liên thông.")
                return None

            model = [var if val else -var for var, val in assignment.items()]
            bridges = self.extract_bridges(model, verbose=False)
            islands = [(i, j) for i, row in enumerate(self.grid) for j, cell in enumerate(row) if cell > 0]

            if is_connected(islands, bridges):
                print("[✓] Lời giải liên thông hợp lệ.")
                return bridges
            else:
                print(f"[x] Lời giải {attempt} không liên thông, thử lại...")
                rejected.add(frozenset(assignment.items()))

    def solve_with_brute_force(self):
        print("[+] Đang giải bằng brute-force...")
        variables = list(self.logic_var.var_to_num.values())
        islands = [(i, j) for i, row in enumerate(self.grid) for j, cell in enumerate(row) if cell > 0]

        def check_model(model):
            assigned = set(model)
            return all(any(lit in assigned for lit in clause) for clause in self.clauses)

        def backtrack(index, assignment):
            if index == len(variables):
                model = [var if val else -var for var, val in zip(variables, assignment)]
                if check_model(model):
                    bridges = self.extract_bridges(model, verbose=False)
                    if is_connected(islands, bridges):
                        return bridges
                return None

            for val in [True, False]:
                assignment.append(val)
                result = backtrack(index + 1, assignment)
                if result:
                    return result
                assignment.pop()
            return None

        result = backtrack(index=0, assignment=[])

        if result:
            return result
        else:
            print("[x] Brute-force không tìm được lời giải hoặc không liên thông.")
            return None

    def solve_with_backtracking(self):
        print("[+] Đang giải bằng backtracking (có cắt tỉa + kiểm tra liên thông)...")
        variables = list(self.logic_var.var_to_num.values())
        islands = [(i, j) for i, row in enumerate(self.grid) for j, cell in enumerate(row) if cell > 0]

        def is_partial_valid(assignment_dict):
            for clause in self.clauses:
                clause_satisfied = False
                undecided = False
                for lit in clause:
                    var = abs(lit)
                    if var in assignment_dict:
                        val = assignment_dict[var]
                        if (lit > 0 and val) or (lit < 0 and not val):
                            clause_satisfied = True
                            break
                    else:
                        undecided = True
                if not clause_satisfied and not undecided:
                    return False
            return True

        def backtrack(index, assignment_dict):
            if index == len(variables):
                model = [var if assignment_dict[var] else -var for var in variables]
                bridges = self.extract_bridges(model, verbose=False)
                if is_connected(islands, bridges):
                    return model
                else:
                    return None

            var = variables[index]
            for val in [True, False]:
                assignment_dict[var] = val
                if is_partial_valid(assignment_dict):
                    result = backtrack(index + 1, assignment_dict)
                    if result:
                        return result
                del assignment_dict[var]
            return None

        result = backtrack(0, {})

        if result:
            return self.extract_bridges(result)
        else:
            print("[x] Backtracking không tìm được lời giải hoặc không liên thông.")
            return None

    def extract_bridges(self, model, verbose=True):
        bridges = []
        # if verbose:
        #     print("\nKết quả solver:")
        for var in model:
            if var > 0:
                decoded = self.logic_var.decode_var(var)
                if decoded:
                    i1, j1, i2, j2, bridge_count = decoded
                    if verbose:
                        direction = 'dọc' if j1 == j2 else 'ngang'
                        type_bridge = 'đôi' if bridge_count == 2 else 'đơn'
                        #print(f"Biến {var}: cầu {type_bridge} {direction} từ ({i1},{j1}) đến ({i2},{j2})")
                    bridges.append(Bridge((i1, j1), (i2, j2), bridge_count))
        return bridges