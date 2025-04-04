import heapq
from collections import Counter, defaultdict, deque

class AStarCNFState:
    def __init__(self, assignment, clauses, total_vars, logic_var):
        self.assignment = assignment
        self.clauses = clauses
        self.total_vars = total_vars
        self.logic_var = logic_var
        self.cost = len(assignment)
        self._satisfied_cache = set()

    def is_goal(self):
        return all(self.satisfies(clause, idx) for idx, clause in enumerate(self.clauses))

    def satisfies(self, clause, idx=None):
        if idx is not None and idx in self._satisfied_cache:
            return True

        for literal in clause:
            var = abs(literal)
            if var in self.assignment:
                val = self.assignment[var]
                if (literal > 0 and val) or (literal < 0 and not val):
                    if idx is not None:
                        self._satisfied_cache.add(idx)
                    return True
        return False

    def heuristic(self):
        score = 0
        for idx, clause in enumerate(self.clauses):
            if self.satisfies(clause, idx):
                continue

            unassigned = [lit for lit in clause if abs(lit) not in self.assignment]
            assigned_false = [lit for lit in clause if abs(lit) in self.assignment and ((lit > 0 and not self.assignment[abs(lit)]) or (lit < 0 and self.assignment[abs(lit)]))]

            if len(unassigned) == 0:
                score += 50
            elif len(unassigned) == 1:
                score += 8
            elif len(unassigned) == 2:
                score += 4
            else:
                score += 1

            if len(assigned_false) == len(clause) - 1 and len(unassigned) == 1:
                score += 10

        return score

    def propagate_unit_clauses(self):
        changed = True
        while changed:
            changed = False
            for idx, clause in enumerate(self.clauses):
                if self.satisfies(clause, idx):
                    continue

                unassigned = [lit for lit in clause if abs(lit) not in self.assignment]
                if len(unassigned) == 1:
                    lit = unassigned[0]
                    var = abs(lit)
                    val = lit > 0

                    if var in self.assignment:
                        if self.assignment[var] != val:
                            return False
                    else:
                        self.assignment[var] = val
                        changed = True
        return True

    def expand(self):
        successors = []
        score = Counter()

        for idx, clause in enumerate(self.clauses):
            if self.satisfies(clause, idx):
                continue
            for lit in clause:
                var = abs(lit)
                if var not in self.assignment:
                    decoded = self.logic_var.decode_var(var)
                    weight = 1
                    if decoded:
                        _, _, _, _, bridge_count = decoded
                        weight = bridge_count
                    score[var] += weight

        if not score:
            return []

        next_var = score.most_common(1)[0][0]

        for val in [True, False]:
            new_assign = self.assignment.copy()
            new_assign[next_var] = val
            new_state = AStarCNFState(new_assign, self.clauses, self.total_vars, self.logic_var)
            if new_state.propagate_unit_clauses():
                successors.append(new_state)

        return successors

    def __lt__(self, other):
        return (self.cost + self.heuristic()) < (other.cost + other.heuristic())


class AStarCNFSolver:
    def __init__(self, clauses, logic_var, verbose=False, exclude_assignments=None):
        self.clauses = clauses
        self.logic_var = logic_var
        self.total_vars = logic_var.counter - 1
        self.verbose = verbose
        self.exclude_assignments = exclude_assignments or set()

    def solve(self):
        start = AStarCNFState({}, self.clauses, self.total_vars, self.logic_var)
        start.propagate_unit_clauses()
        pq = [(start.cost + start.heuristic(), start)]
        visited = set()
        step = 0

        while pq:
            _, current = heapq.heappop(pq)
            step += 1

            key = frozenset(current.assignment.items())
            if key in visited or key in self.exclude_assignments:
                continue
            visited.add(key)

            # if self.verbose and step % 100 == 0:
            #     print(f"[Step {step}] Gán {len(current.assignment)} biến | heuristic = {current.heuristic()} | queue size = {len(pq)}")

            if current.is_goal():
                #print(f"[✓] Đã tìm thấy lời giải tại bước {step}.")
                return current.assignment

            for next_state in current.expand():
                k = frozenset(next_state.assignment.items())
                if k not in visited and k not in self.exclude_assignments:
                    heapq.heappush(pq, (next_state.cost + next_state.heuristic(), next_state))

        print("[x] Không tìm được lời giải.")
        return None
