import sys
import re


def process_workflows(workflows):
    wf_dict = {}
    for wf_line in workflows.splitlines():
        wf_name, wfs = re.match(r"(.*)\{(.*)\}", wf_line).groups()
        rules = wfs.split(",")
        wf_order = []
        for rule in rules:
            if ">" in rule or "<" in rule:
                comp, dr = rule.split(":")
                cat, comp, val = comp[0], comp[1], comp[2:]
                wf_order.append((cat, comp, int(val), dr))
            else:
                wf_order.append((rule,))
        wf_dict[wf_name] = wf_order
    return wf_dict


def process_parts(parts_data):
    parts = []
    for part_data in parts_data.splitlines():
        part = {p[0]: int(p[2:]) for p in part_data[1:-1].split(",")}
        parts.append(part)
    return parts


def check_accepted(part, wf_dict):
    next_wf = "in"
    while True:
        for r in wf_dict[next_wf]:
            if len(r) > 1:
                if r[1] == ">":
                    if part[r[0]] > r[2]:
                        if r[3] == "A": return True
                        if r[3] == "R": return False
                        next_wf = r[3]
                        break
                else:
                    if part[r[0]] < r[2]:
                        if r[3] == "A": return True
                        if r[3] == "R": return False
                        next_wf = r[3]
                        break
            else:
                if r[0] == "A": return True
                if r[0] == "R": return False
                next_wf = r[0]
                break


def main(filename):
    """
    # Results:
    Part1: 449531
    Part2: 122756210763577
    """
    with open(filename) as f:
        # Commonly used for various inputs
        data = f.read()

    workflows, parts_data = data.split("\n\n")

    wf_dict = process_workflows(workflows)
    parts = process_parts(parts_data)

    ans = 0
    for p in parts:
        if check_accepted(p, wf_dict):
            ans += sum(p.values())

    print(f"Part1: {ans}")


    ## Trying part2 magic with range splittings
    ## ----------------------------------------
    def count(ranges, wf_name = "in"):
        # print("...testing...", wf_name, ranges)

        # We dont count rejects...
        if wf_name == "R": return 0

        # If we reach accept, we need to count product of 
        if wf_name == "A":
            product = 1
            for low, high in ranges.values():
                product *= high - low + 1
            # print("Reached ACCEPT", ranges.values(), product)
            return product
        
        rules = wf_dict[wf_name][:-1]
        fallback = wf_dict[wf_name][-1][0]

        ## Need to go trough this a bit....
        total = 0
        for cat, comp, val, dr in rules:
            # Get smallest and largest values in this range for given category (x, m ,a ,s)
            low, high = ranges[cat]    # ex: (1, 4000)
            # Split into true and false parts, based on comparison of the rule
            if comp == "<":
                true_half = (low, min(val - 1, high))  # make new range definition for true with with same initial "low" up to rules's "high"
                false_half = (max(val, low), high)     # make new range definition for true above rule's "low", and same initial "high"
            else:
                true_half = (max(val + 1, low), high)  # almost reverse from above
                false_half = (low, min(val, high))     # almost reverse from above

            # Check lower bound of "true" half is less or equal then higher bound
            # While we still have diff between low and high, make a copy of range, and update
            # values of specific category (x, m, a ,s) to new boundaries to check
            if true_half[0] <= true_half[1]:
                copy = dict(ranges)
                copy[cat] = true_half
                total += count(copy, dr)
            if false_half[0] <= false_half[1]:
                ranges = dict(ranges)
                ranges[cat] = false_half
            else:
                # we covered all remaining cases, so we dont need to check anything
                break
        # Once we break, we need to acount for last iteration
        else:
            total += count(ranges, fallback)
        
        # Return accumulated
        return total
    
    ranges = { key: (1, 4000) for key in "xmas" }   # {'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}
    print(f"Part2: {count(ranges)}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
