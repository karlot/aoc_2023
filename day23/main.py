import sys

def get_points(start, end, lines):
    points = [start, end]
    for r, row in enumerate(lines):
        for c, ch in enumerate(row):
            if ch == "#": continue
            neighbors = 0
            for nr, nc in [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]:
                if 0 <= nr < len(lines) and 0 <= nc < len(lines[0]) and lines[nr][nc] != "#":
                    neighbors += 1
            if neighbors >= 3:
                points.append((r, c))
    return points


def run_dfs(start, end, points_graph):
    seen = set()
    def dfs(pt):
        if pt == end: return 0
        m = -float("inf")
        seen.add(pt)
        for nx in points_graph[pt]:
            if nx not in seen: m = max(m, dfs(nx) + points_graph[pt][nx])
        seen.remove(pt)
        return m
    return dfs(start)


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
        grid = [[c for c in line] for line in lines]

    rows = len(grid)
    cols = len(grid[0])

    # There's a map of nearby hiking trails (your puzzle input) that indicates
    # paths (.), forest (#), and steep slopes (^, >, v, and <).
        
    # You're currently on the single path tile in the top row
    # your goal is to reach the single path tile in the bottom row.
    start = (0, lines[0].index("."))
    end = (rows - 1, lines[rows - 1].index("."))

    points = get_points(start, end, lines)

    # Direction map (possibilities based on current field)
    directions = {
        "^": [(-1, 0)],
        "v": [(1, 0)],
        "<": [(0, -1)],
        ">": [(0, 1)],
        ".": [(-1, 0), (1, 0), (0, -1), (0, 1)],
    }

    # Some switches when running only single part
    run_part1 = True
    run_part2 = True

    # ---------------------------------
    # Part 1
    # ---------------------------------
    # Because of all the mist from the waterfall, the slopes are probably quite icy;
    # if you step onto a slope tile, your next step must be downhill (in the direction
    # the arrow is pointing).
    # To make sure you have the most scenic hike possible, never step onto the same
    # tile twice. What is the longest hike you can take?
    if run_part1:
        points_graph = {p: {} for p in points}
        for sr, sc in points:
            stack = [(0, sr, sc)]
            seen = {(sr, sc)}
            while stack:
                n, r, c = stack.pop()
                if n != 0 and (r, c) in points:
                    points_graph[(sr, sc)][(r, c)] = n
                    continue
                for dr, dc in directions[grid[r][c]]:
                    nr, nc = r + dr, c + dc
                    # Boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == "#": continue
                        if (nr, nc) not in seen:
                            stack.append((n + 1, nr, nc))
                            seen.add((nr, nc))

        print(f"Part1: {run_dfs(start, end, points_graph)}")

    # ---------------------------------
    # Part 2
    # ---------------------------------
    # As you reach the trailhead, you realize that the ground isn't as slippery as you expected;
    # you'll have no problem climbing up the steep slopes.
    # Now, treat all slopes as if they were normal paths (.). You still want to make sure you have
    # the most scenic hike possible, so continue to ensure that you never step onto the same tile twice.
    # What is the longest hike you can take?
    if run_part2:
        points_graph = {p: {} for p in points}
        for sr, sc in points:
            stack = [(0, sr, sc)]
            seen = {(sr, sc)}
            while stack:
                n, r, c = stack.pop()
                if n != 0 and (r, c) in points:
                    points_graph[(sr, sc)][(r, c)] = n
                    continue
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    # Boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        if grid[nr][nc] == "#": continue
                        if (nr, nc) not in seen:
                            stack.append((n + 1, nr, nc))
                            seen.add((nr, nc))

        print(f"Part2: {run_dfs(start, end, points_graph)}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
