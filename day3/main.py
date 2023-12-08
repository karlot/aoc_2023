part1 = "input.txt"

with open(part1, "r", encoding="utf8") as f:
    full_document = f.readlines()

    # Build DB of part numbers and their position in schema
    part_numbers = [
        # { "part": 467, "y": 0, "x": 0, "len": 3 }
    ]

    stars = [
        # (x, y)
    ]

    max_y = len(full_document) - 1
    y = 0
    for line in full_document:
        part_state = 0
        part_num = ""

        line_cleaned = line.strip()     
        for x, c in enumerate(line_cleaned):
            if c == "*":
                stars.append((x, y))
            if c.isdigit():
                part_state = 1
                part_num += c
                if x == len(line_cleaned) - 1:
                    part_numbers.append({ "part": part_num, "y": y, "x": x - len(part_num) + 1, "len": len(part_num) })
            else:
                # Not a digit... if part number was previously found
                # close part number and store it in DB
                if part_state == 1:
                    part_numbers.append({ "part": part_num, "y": y, "x": x - len(part_num), "len": len(part_num) })
                    part_state = 0
                    part_num = ""
            
        # move y position
        if y < max_y:
            y += 1

    # Find if part numbers are valid...
    for part in part_numbers:

        # Vertical lines for checking
        lines_to_check = []
        if part["y"] == 0:
            lines_to_check = [x.strip() for x in full_document[:2]]
        elif part["y"] == len(full_document) - 1:
            lines_to_check = [x.strip() for x in full_document[-2:]]
        else:
            lines_to_check = [x.strip() for x in full_document[part["y"]-1:part["y"]+2]]

        # Horizontal characters...
        for line in lines_to_check:
            # part starts at line beginning
            if part["x"] == 0:
                part_end = part["x"] + part["len"] + 1
                part_slice = line[:part_end]
                for c in part_slice:
                    if c != "." and not c.isdigit():
                        part["valid"] = True
            # part ends at line end
            elif part["x"] + part["len"] == len(line):
                part_slice = line[part["x"] - 1:]
                for c in part_slice:
                    if c != "." and not c.isdigit():
                        part["valid"] = True
            # part in the middle of line
            else:
                part_end = part["x"] + part["len"] + 1
                part_slice = line[part["x"] - 1:part_end]
                for c in part_slice:
                    if c != "." and not c.isdigit():
                        part["valid"] = True
    
    valid_part_sum = 0
    for part in part_numbers:
        if "valid" in part and part["valid"]:
            valid_part_sum += int(part["part"])
        
    print(f"Part1: {valid_part_sum}")

    #--- part 2 ---
    cumulated_rations = 0
    for star in stars:
        (sx, sy) = star
        adjacent_parts = []
        for part in part_numbers:
            if "valid" in part:
                ydiff = sy - part["y"]
                if ydiff == -1 or ydiff == 0 or ydiff == 1:
                    # Inspected part is in correct line to be adjacent
                    part_s = part["x"]
                    part_e = part["x"] + part["len"] - 1

                    if sx < part_s - 1 or sx > part_e + 1:
                        continue

                    adjacent_parts.append(part)
        
        if len(adjacent_parts) == 2:
            gear_ratio = int(adjacent_parts[0]["part"]) * int(adjacent_parts[1]["part"])
            cumulated_rations += gear_ratio

    print(f"Part2: {cumulated_rations}")

