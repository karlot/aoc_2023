import sys
from itertools import combinations
import sympy

def main(filename):
    """
    # Results:
    Part1: 20434
    Part2: 1025127405449117
    """
    if filename == "example.txt":
        lo = 7
        hi = 27
    else:
        lo = 200000000000000
        hi = 400000000000000

    with open(filename) as f:
        # Commonly used for various inputs
        data = f.read()
        lines = tuple(data.splitlines())
        # grid = tuple([tuple([c for c in line]) for line in lines])

    # Process input
    hailstones = [tuple(map(int, line.replace(" @", ",").split(", "))) for line in lines]

    # Some switches when running only single part
    run_part1 = True
    run_part2 = True

    # ---------------------------------
    # Part 1
    # ---------------------------------
    if run_part1:
        total = 0
        for h1, h2 in combinations(hailstones, 2):
            a1, b1, c1 = h1[4], -h1[3], (h1[4] * h1[0] - h1[3] * h1[1])
            a2, b2, c2 = h2[4], -h2[3], (h2[4] * h2[0] - h2[3] * h2[1])
            if a1 * b2 == b1 * a2: continue     # parallel

            x = (c1 * b2 - c2 * b1) / (a1 * b2 - a2 * b1)
            y = (c2 * a1 - c1 * a2) / (a1 * b2 - a2 * b1)
            # Check within target range
            if lo <= x <= hi and lo <= y <= hi:
                if all((x - h[0]) * h[3] >= 0 and (y - h[1]) * h[4] >= 0 for h in (h1, h2)):
                    total += 1
                        
        print(f"Part1: {total}")

    # ---------------------------------
    # Part 2
    # ---------------------------------
    if run_part2:
        unknowns = sympy.symbols('x y z dx dy dz t1 t2 t3')
        x, y, z, dx, dy, dz, *time = unknowns

        equations = []  # build system of 9 equations with 9 unknowns
        for t, h in zip(time, hailstones[0:3]):
            equations.append(sympy.Eq(x + t*dx, h[0] + t*h[3]))
            equations.append(sympy.Eq(y + t*dy, h[1] + t*h[4]))
            equations.append(sympy.Eq(z + t*dz, h[2] + t*h[5]))

        solution = sympy.solve(equations, unknowns).pop()
        print(f"Part2: {sum(solution[:3])}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
