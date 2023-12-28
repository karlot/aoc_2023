import sys
from collections import deque


def find_start(grid):
    for y, r in enumerate(grid):
        for x, c in enumerate(r):
            if c == "S":
                return (x, y)


def main(filename):
    """
    # Results:
    Part1: 
    Part2:
    """
    with open(filename) as f:
        # Commonly used for various inputs
        data = f.read()
        lines = tuple(data.splitlines())
        grid = tuple([tuple([c for c in line]) for line in lines])

    # Some switches when running only single part
    run_part1 = True
    run_part2 = False

    # ---------------------------------
    # Part 1
    # ---------------------------------
    if run_part1:
        rows = len(grid)
        cols = len(grid[0])
        start = find_start(grid)
        # print(f"Starting position: {start}")

        start_set = set()
        start_set.add(start)
        q = deque()
        q.append(start_set)

        max_steps = 64
        steps = 0
        next_set = set()
        while q:
            steps += 1
            positions = q.popleft()
            next_set = set()
            for px, py in positions:
                # Check all directions "URDL"
                for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                    nx, ny = px + dx, py + dy
                    if (ny < 0 or ny >= rows) or (nx < 0 or nx >= cols):
                        # print(f"Reached edge {(nx, ny)}!")
                        continue
                    if grid[ny][nx] == "#":
                        # print(f"Rock at {(nx, ny)}, cannot get there!")
                        continue
                    # print(f"Next position OK: {(nx, ny)}")
                    next_set.add((nx, ny))
            # print("-" * 40)
            # print(f"Next set of positions: {next_set}")
            if steps < max_steps:
                q.append(next_set)

        print(f"Part1: {len(next_set)}")

    # ---------------------------------
    # Part 2
    # ---------------------------------
    if run_part2:
        print(f"Part2: {None}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
