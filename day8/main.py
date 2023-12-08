import sys
import re
from math import gcd
# from collections import defaultdict

def parse_map(lines):
    steps, map_lines = lines[0], lines[2:]
    
    map_def = {}
    for line in map_lines:
        loc, path_str = [l.strip() for l in line.split("=")]
        map_def[loc] = re.search(r"(\w+), (\w+)", path_str).groups()

    # Return steps from first line, and map of paths
    return steps.strip(), map_def


def main(filename):
    """
    # Results:
    Part1: 21797
    Part2: None
    """
    with open(filename, "r") as f:
        lines = f.readlines()

    # Get steps and maps paths
    steps, map_def = parse_map(lines)

    # --- [ Part 1 ]
    current, destination = "AAA", "ZZZ"
    curr_step, total_steps = 0, 0

    while(current != destination):
        current = map_def[current][0] if steps[curr_step] == "L" else map_def[current][1]
        total_steps += 1
        curr_step += 1
        # Loop over steps
        if (curr_step == len(steps)): curr_step = 0

    print(f"Part1: {total_steps}")


    # --- [ Part 2 ]
    # Each path takes various times to complete to "Z" designation, and then loops back to beginning
    # But there are in this sample 6 different paths, and each loops back in different intervals
    # Since we cant iterate trough that much samples in our case 23.977.527.174.353 steps with brute force,
    # we try to find lowest common multiple of all path-cycles combined.
    def lcm(paths):
        a = 1
        for p in paths:
            a = (p * a) // gcd(p, a)
        return a

    current_positions = [x for x in map_def.keys() if x.endswith("A")]
    path_result_steps = []
    for start in current_positions:
        curr_step, total_steps = 0, 0
        current = start
        while(not current.endswith("Z")):
            current = map_def[current][0] if steps[curr_step] == "L" else map_def[current][1]
            total_steps += 1
            curr_step += 1
            # Loop over steps
            if (curr_step == len(steps)): curr_step = 0
        # Append number of steps for this path
        path_result_steps.append(total_steps)
    
    # Calculate LCM over all paths
    total_steps = lcm(path_result_steps)
    print(f"Part2: {total_steps}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
