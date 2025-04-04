from .logic_variable import LogicVariable
import itertools
class CNFGenerator:
    def __init__(self, grid):
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])
        self.clauses = []
        self.logic_var = LogicVariable()

    def generate_cnf(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j] > 0:
                    self.island_constraints(i, j, self.grid[i][j])

        # Gọi ràng buộc cấm cầu giao nhau
        self.no_cross_constraints()

        return self.clauses, self.logic_var

    def island_constraints(self, i, j, num_bridges):
        connected_vars = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            ni, nj = i + dx, j + dy
            while 0 <= ni < self.rows and 0 <= nj < self.cols:
                if self.grid[ni][nj] > 0:
                    if abs(ni - i) > 1 or abs(nj - j) > 1:
                        v_single = self.logic_var.get_var(i, j, ni, nj, 1)
                        v_double = self.logic_var.get_var(i, j, ni, nj, 2)
                        connected_vars.append((v_single, 1))
                        connected_vars.append((v_double, 2))
                        self.clauses.append([-v_single, -v_double])
                    break
                ni += dx
                nj += dy

        all_vars_set = set(connected_vars)

        # Ràng buộc loại bỏ các tổ hợp vượt quá yêu cầu
        for r in range(len(connected_vars) + 1):
            for comb in itertools.combinations(connected_vars, r):
                s = sum(w for (_, w) in comb)
                if s > num_bridges:
                    self.clauses.append([-v for (v, _) in comb])
                if s < num_bridges:
                    outside = all_vars_set - set(comb)
                    clause = []
                    clause.extend([-v for (v, _) in comb])
                    clause.extend([v for (v, _) in outside])
                    self.clauses.append(clause)

    def no_cross_constraints(self):
        var_items = list(self.logic_var.var_to_num.items())

        for idx1 in range(len(var_items)):
            key1, var1 = var_items[idx1]
            i1a, j1a, i1b, j1b, _ = key1

            for idx2 in range(idx1 + 1, len(var_items)):
                key2, var2 = var_items[idx2]
                i2a, j2a, i2b, j2b, _ = key2

                # Bỏ qua nếu có điểm đầu/cuối trùng nhau
                endpoints_1 = {(i1a, j1a), (i1b, j1b)}
                endpoints_2 = {(i2a, j2a), (i2b, j2b)}
                if endpoints_1 & endpoints_2:
                    continue

                # Kiểm tra nếu hai cầu giao nhau tại một ô không phải đảo
                if self.cross(i1a, j1a, i1b, j1b, i2a, j2a, i2b, j2b):
                    self.clauses.append([-var1, -var2])

    def cross(self, i1a, j1a, i1b, j1b, i2a, j2a, i2b, j2b):
        # Cầu 1: nằm ngang
        if i1a == i1b:
            y1 = i1a
            x1_start, x1_end = sorted([j1a, j1b])

            # Cầu 2: nằm dọc
            if j2a == j2b:
                x2 = j2a
                y2_start, y2_end = sorted([i2a, i2b])

                # Giao tại 1 điểm
                if x1_start < x2 < x1_end and y2_start < y1 < y2_end:
                    # Nếu không giao tại đảo thì cấm
                    if self.grid[y1][x2] == 0:
                        return True

        # Hoán vị 2 cầu để tránh bỏ sót
        if i2a == i2b and j1a == j1b:
            return self.cross(i2a, j2a, i2b, j2b, i1a, j1a, i1b, j1b)

        return False