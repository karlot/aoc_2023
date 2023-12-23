import sys
import re
from rich.pretty import pprint

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

    wf_dict = {}

    workflows, parts_data = data.split("\n\n")
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
    
    parts = []
    for part_data in parts_data.splitlines():
        part = {p[0]: int(p[2:]) for p in part_data[1:-1].split(",")}
        parts.append(part)

    accepted = []
    rejected = []
    for part in parts:
        next_wf = "in"
        finished = False
        while not finished:
            # print(next_wf, part, wf_dict[next_wf])
            for r in wf_dict[next_wf]:
                # print(r[1], part[r[0]], r[2], r[3])
                if len(r) > 1:
                    # Check props
                    if r[1] == ">":
                        if part[r[0]] > r[2]:
                            if r[3] == "A":
                                accepted.append(part)
                                finished = True
                                break
                            elif r[3] == "R":
                                rejected.append(part)
                                finished = True
                                break
                            else:
                                next_wf = r[3]
                                break
                        # continue
                    else:
                        if part[r[0]] < r[2]:
                            if r[3] == "A":
                                accepted.append(part)
                                finished = True
                                break
                            elif r[3] == "R":
                                rejected.append(part)
                                finished = True
                                break
                            else:
                                next_wf = r[3]
                                break
                        # continue
                else:
                    # print(f"End of WF with rule: {r[0]}")
                    if r[0] == "A":
                        accepted.append(part)
                        finished = True
                        break
                    elif r[0] == "R":
                        rejected.append(part)
                        finished = True
                        break
                    else:
                        next_wf = r[0]
                        break
    
    ans = 0
    for p in accepted:
        ans += p["x"] + p["m"] + p["a"] + p["s"]

    print(f"Part1: {ans}")
    # print(f"Part2: {None}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
