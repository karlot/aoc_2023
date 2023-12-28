import sys
from collections import deque


def find_start(grid):
    for y, r in enumerate(grid):
        for x, c in enumerate(r):
            if c == "S":
                return (x, y)

# def draw(grid, fill_points):
#     print()
#     for gy, r in enumerate(grid):
#         for gx, c in enumerate(r):
#             if c == "#": continue
#             grid[gy][gx] = "."

#     for fx, fy in fill_points:
#         grid[fy][fx] = "O"
#     for r in grid:
#         print("".join(r))


def main(filename):
    """
    # Results:
    Part1: 3532
    Part2:
    """
    with open(filename) as f:
        # Commonly used for various inputs
        data = f.read()
        lines = tuple(data.splitlines())
        grid = [[c for c in line] for line in lines]

    # Some switches when running only single part
    run_part1 = True
    run_part2 = True

    # General
    rows = len(grid)
    cols = len(grid[0])
    start = find_start(grid)
    # print(f"Starting position: {start}")

    def steps(max_steps):
        q = deque()
        q.append({start})

        for _ in range(max_steps):
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
            q.append(next_set)
        return len(next_set)

    # ---------------------------------
    # Part 1
    # ---------------------------------
    if run_part1:
        print(f"Part1: {steps(64)}")

    # ---------------------------------
    # Part 2
    # ---------------------------------
    # Scrambled some ideas from net, and tried it out... took some time to make it work
    if run_part2:
        target_steps = 26501365

        # Get set of all plot coordinates in base matrix both "." and "S" are considered "plots"
        gps = {(i, j) for i in range(rows) for j in range(rows) if grid[i][j] in '.S'}
        
        visited = {start}   # Visited set
        new     = {start}   # New set
        cache   = {0:1}     # Cache
        k       = target_steps // rows  # quotient
        r       = target_steps % rows   # remainder

        for c in range(1, r + 2 * rows + 1):
            updated_nps = set()
            for cp in new:
                for dir in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    np = (cp[0] + dir[0], cp[1] + dir[1])
                    if np not in visited and (np[0] % rows, np[1] % rows) in gps:
                        updated_nps.add(np)

            visited = visited.union(updated_nps)
            new = updated_nps            
            cache[c] = len(new) + (cache[c - 2] if c > 1 else 0)

        d2 = cache[r + 2 * rows] + cache[r] - 2 * cache[r + rows]
        d1 = cache[r + 2 * rows] - cache[r + rows]
        total_plots = cache[r + 2 * rows] + (k - 2) * (2 * d1 + (k - 1) * d2) // 2

        print(f"Part2: {total_plots}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
