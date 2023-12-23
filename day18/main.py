import sys
import re

class Lagoon:
    def __init__(self, lines) -> None:
        self.lines = lines

    def process_path(self, part=1) -> None:
        self.path = []
        self.points = []
        self.path_length = 0
        self.min_x, self.min_y = 0, 0
        self.max_x, self.max_y = 0, 0

        x, y = 0, 0
        for line in self.lines:
            d, m, c = re.match(r"([UDRL]) (\d+) \(#(\w+)\)", line).groups()
            if part == 2:
                m = int(c[0:5], 16)
                d = ("R", "D", "L", "U")[int(c[5])]
            m = int(m)
            self.path_length += m
            match d:
                case "U":
                    y -= m
                    if y < self.min_y: self.min_y = y
                case "D":
                    y += m
                    if y > self.max_y: self.max_y = y
                case "L":
                    x -= m
                    if x < self.min_x: self.min_x = x
                case "R":
                    x += m
                    if x > self.max_x: self.max_x = x
                case _:   assert 1, "Unexpected direction!"
            self.path.append((d, m, c))
            self.points.append((x, y))

        self.gy = abs(self.min_y) + self.max_y + 1
        self.gx = abs(self.min_x) + self.max_x + 1
        self.points = [(x + abs(self.min_x), y + abs(self.min_y)) for (x, y) in self.points]


    def dig_by_fill(self):
        grid = [["." for _ in range(self.gx)] for _ in range(self.gy)]
        x, y = abs(self.min_x), abs(self.min_y)

        trench_volume = 0
        for d, m, c in self.path:
            trench_volume += m
            match d:
                case "U":
                    for _ in range(m):
                        y -= 1
                        grid[y][x] = "#"
                case "D":
                    for _ in range(m):
                        y += 1
                        grid[y][x] = "#"
                case "L":
                    for _ in range(m):
                        x -= 1
                        grid[y][x] = "#"
                case "R":
                    for _ in range(m):
                        x += 1
                        grid[y][x] = "#"

        # Dimensions
        rows, cols = len(grid), len(grid[0])

        # Flood fill
        def flood_fill(g, y, x):
            stack = [(y, x)]
            flooded = 0
            while stack:
                y, x = stack.pop()
                if 0 <= y < rows and 0 <= x < cols and g[y][x] == ".":
                    g[y][x] = "#"
                    flooded += 1

                    # Add neighbors to the stack
                    for py, px in [(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)]:
                        stack.append((py, px))    
            return flooded

        # Find starting point for fill (somewhere inside)
        # Find first "#" from left side of the grid, and see it is surrounded by "."
        # This means point on right side is first seem "inside" point we can use for
        # fill algorithm
        start_x, start_y = 0, 0
        for y, r in enumerate(grid):
            found = False
            for x, c in enumerate(r):
                if y == 0 or x == 0: continue
                if x == cols - 1: continue
                if c == "#" and grid[y][x-1] == "." and grid[y][x+1] == ".":
                    start_x = x + 1
                    start_y = y
                    found = True
                    # print(f"Found inside point: {start_x=} {start_y=}")
                    break
            if found:
                break

        # Dig inside trench
        total_volume = flood_fill(grid, start_y, start_x) + trench_volume
        return total_volume


    # For Part2 some math based solution (need to combine this two)
    # https://en.wikipedia.org/wiki/Shoelace_formula
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    def gauss_calc_points(self):
        n = len(self.points)
        # Polygon area is not really correct, since our lines are not "zero-width", so assumption is that 
        # polygon lines are basically passing rough mid of the single-width border of the lagoon.
        polygon_area = 0.5 * abs(sum(self.points[i][0] * self.points[(i + 1) % n][1] - self.points[(i + 1) % n][0] * self.points[i][1] for i in range(n)))

        # Combining polygon area, with Pick's theorem gives us amount of whole unit points (without border-width)
        inbound_area = polygon_area - (self.path_length / 2) + 1

        # Returning inbound-area from picks theorem with our border volume, should give final result
        return int(inbound_area + self.path_length)


def main(filename):
    """
    # Results:
    Part1: 40131
    Part2: 104454050898331
    """
    with open(filename) as f:
        # Commonly used for various inputs
        data = f.read()
        lines = tuple(data.splitlines())

    # Init the lagoon with lines from input
    dig = Lagoon(lines)

    # Part1 (done by fill-algorithm)
    dig.process_path(part=1)
    print(f"Part1: {dig.dig_by_fill()}")

    # Part2 (done by Shoelace formula & Pick's theorem)
    dig.process_path(part=2)
    print(f"Part2: {dig.gauss_calc_points()}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
