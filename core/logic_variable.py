class LogicVariable:
    def __init__(self):
        self.var_to_num = {}
        self.num_to_var = {}
        self.counter = 1  # Biến logic bắt đầu từ 1 theo PySAT

    def __repr__(self):
        return f"LogicVariable({self.var_to_num})"

    def get_var(self, i1, j1, i2, j2, k):
        key = (min(i1, i2), min(j1, j2), max(i1, i2), max(j1, j2), k)
        if key not in self.var_to_num:
            self.var_to_num[key] = self.counter
            self.num_to_var[self.counter] = key
            self.counter += 1
        return self.var_to_num[key]

    def decode_var(self, num):
        return self.num_to_var.get(abs(num), None)



