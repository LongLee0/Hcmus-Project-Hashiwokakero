import os
import time
from collections import defaultdict, deque

def load_input(file_path):
    with open(file_path, 'r') as file:
        return [list(map(int, line.strip().split(','))) for line in file]

def convert_solution_to_symbols(grid, solution):
    symbol_grid = [['0' if cell == 0 else str(cell) for cell in row] for row in grid]

    for bridge in solution:
        start, end, count = bridge.start, bridge.end, bridge.count

        # Ngang
        if start[0] == end[0]:
            symbol = '-' if count == 1 else '='
            for j in range(min(start[1], end[1])+1, max(start[1], end[1])):
                symbol_grid[start[0]][j] = symbol

        # Dọc
        if start[1] == end[1]:
            symbol = '|' if count == 1 else '$'
            for i in range(min(start[0], end[0])+1, max(start[0], end[0])):
                symbol_grid[i][start[1]] = symbol

    return symbol_grid

def get_matrix_size(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()
    row = len(lines)
    col = len(lines[0].strip().split(",")) if row > 0 else 0
    return row, col

def choose_input_file(input_folder="Inputs", output_folder="Outputs"):
    input_files = sorted(
        [f for f in os.listdir(input_folder) if f.startswith("input-") and f.endswith(".txt")]
    )

    if not input_files:
        print("Can't find the input files.")
        exit()

    print("List of input files:")
    file_sizes = {}
    for idx, name in enumerate(input_files, 1):
        file_path = os.path.join(input_folder, name)
        row, col = get_matrix_size(file_path)
        file_sizes[name] = (row, col)
        print(f"[{idx}] {name} - {row}x{col}")

    choice = int(input("Enter a number to choose file: ")) - 1
    if choice < 0 or choice >= len(input_files):
        print("Invalid choice.")
        exit()

    input_file = os.path.join(input_folder, input_files[choice])
    output_file = os.path.join(output_folder, input_files[choice].replace("input", "output"))
    return input_file, output_file

def print_solution(solution):
    for row in solution:
        print(' , '.join(str(cell) for cell in row))


def save_solution(solution, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as file:  # thêm encoding='utf-8'
        for row in solution:
            file.write(' , '.join(str(cell) for cell in row) + '\n')

def timed_solver(solver_func, label="Thuật toán"):
    start = time.perf_counter()
    solution = solver_func()
    end = time.perf_counter()
    print(f"[✓] {label} chạy trong {end - start:.4f} giây")
    return solution

def is_connected(islands, bridges):
    graph = defaultdict(list)
    island_set = set(islands)  # Tọa độ (i, j)

    for bridge in bridges:
        if bridge.start in island_set and bridge.end in island_set:
            graph[bridge.start].append(bridge.end)
            graph[bridge.end].append(bridge.start)

    if not islands:
        return True

    start = islands[0]
    visited = set()
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                queue.append(neighbor)

    return len(visited) == len(island_set)
