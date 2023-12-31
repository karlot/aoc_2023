import sys

# Directions
UP    = [(-1,  0)]
DOWN  = [( 1,  0)]
LEFT  = [( 0, -1)]
RIGHT = [( 0,  1)]
UDLR =  [*UP, *DOWN, *LEFT, *RIGHT]

def get_points(start, end, lines):
    points = [start, end]
    rows = len(lines)
    cols = len(lines[0])
    for y, row in enumerate(lines):
        for x, ch in enumerate(row):
            if ch == "#": continue
            neighbors = 0
            for dy, dx in UDLR:
                ny, nx = y + dy, x + dx
                if 0 <= ny < rows and 0 <= nx < cols and lines[ny][nx] != "#":
                    neighbors += 1
            if neighbors >= 3:
                points.append((y, x))
    return points


def run_dfs(start, end, points_graph):
    seen = set()
    def dfs(position):
        if position == end: return 0
        m = -float("inf")
        seen.add(position)
        for nx in points_graph[position]:
            if nx not in seen: m = max(m, dfs(nx) + points_graph[position][nx])
        seen.remove(position)
        return m
    return dfs(start)


def main(filename):
    """
    # Results:
    Part1: 2134
    Part2: 6298
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

    # Get all points for the graph (where we can branch)
    points = get_points(start, end, lines)

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
        # Direction map (possibilities based on current field)
        directions = {"^": UP, "v": DOWN, "<": LEFT, ">": RIGHT, ".": UDLR}
        points_graph = {p: {} for p in points}
        for sy, sx in points:
            stack = [(0, sy, sx)]
            seen = {(sy, sx)}
            while stack:
                n, y, x = stack.pop()
                if n != 0 and (y, x) in points:
                    points_graph[(sy, sx)][(y, x)] = n
                    continue
                for dy, dx in directions[grid[y][x]]:  # We check limited set based on current field type
                    ny, nx = y + dy, x + dx
                    # Boundaries
                    if 0 <= ny < rows and 0 <= nx < cols:
                        if grid[ny][nx] == "#": continue
                        if (ny, nx) not in seen:
                            stack.append((n + 1, ny, nx))
                            seen.add((ny, nx))

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
        for sy, sx in points:
            stack = [(0, sy, sx)]
            seen = {(sy, sx)}
            while stack:
                n, y, x = stack.pop()
                if n != 0 and (y, x) in points:
                    points_graph[(sy, sx)][(y, x)] = n
                    continue
                for dy, dx in UDLR:     # We check all directions ignoring the slopes
                    ny, nx = y + dy, x + dx
                    # Boundaries
                    if 0 <= ny < rows and 0 <= nx < cols:
                        if grid[ny][nx] == "#": continue
                        if (ny, nx) not in seen:
                            stack.append((n + 1, ny, nx))
                            seen.add((ny, nx))

        print(f"Part2: {run_dfs(start, end, points_graph)}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
