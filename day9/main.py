import sys
# import re
# from collections import defaultdict


def main(filename):
    """
    # Results:
    """
    with open(filename, "r") as f:
        lines = f.readlines()

    reports = []
    for line in lines:
        reports.append([[int(l.strip()) for l in line.split()]])
    
    sum_of_prev_values = 0
    sum_of_next_values = 0
    for r in reports:
        level = 0
        while True:
            if all(v == 0 for v in r[level]):
                break
            r.append([])
            for i, v in enumerate(r[level]):
                if i == len(r[level]) - 1:
                    break
                r[level + 1].append(r[level][i + 1] - v)
            level += 1
        
        # Part 1:  prediction of the next value
        appended = 0
        for l in reversed(r):
            added_val = l[-1] + appended
            l.append(added_val)
            appended = added_val

        # Part 2:  extrapolate backwards  
        prepend = 0
        for l in reversed(r):
            added_val = l[0] - prepend
            l.insert(0, added_val)          # append to beginning
            prepend = added_val
            
    for r in reports:
        sum_of_next_values += r[0][-1]
        sum_of_prev_values += r[0][0]

    print(f"Part1: {sum_of_next_values}")
    print(f"Part2: {sum_of_prev_values}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
