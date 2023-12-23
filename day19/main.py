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
    Part2:
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
    # print(f"Part2: {None}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
