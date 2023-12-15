import sys

def main(filename):
    """
    # Results:
    """
    with open(filename) as f:
        # lines = [l.strip() for l in f.readlines()]
        patterns = [part.split("\n") for part in f.read().strip().split("\n\n")]

    cum = 0
    for id, part in enumerate(patterns):
        # if id == 12:
        #     for i, p in enumerate(part):
        #         print(i, p)
            rows_len = len(part)

            # Check vertical
            vsym = False
            sym_row = None
            for ir in range(rows_len):
                if ir == rows_len - 1: break            # When last
                if part[ir] != part[ir + 1]: continue   # If we dont match with next, skip
                vsym = True
                sym_row = ir + 1
                # print(sym_row, ir + 1, rows_len - ir -1)
                for offset in range(min(ir + 1, rows_len - ir -1)):
                    # print(part[ir - offset], part[ir + 1 + offset])
                    if part[ir - offset] != part[ir + 1 + offset]:
                        vsym = False
                        break
                if vsym:
                    break
            if vsym:
                print(f"{id} Vertical on row: {sym_row}")
                cum += 100 * sym_row
                continue
            
            # Check horizontal
            hsym = False
            sym_col = None
            tpart = list(zip(*[[c for c in r] for r in part]))
            # for i, p in enumerate(tpart):
            #     print(i, p)

            cols_len = len(tpart)
            for ic in range(cols_len):
                if ic == cols_len - 1: break            # When last
                # print(ic, tpart[ic], tpart[ic + 1], tpart[ic] == tpart[ic + 1])
                if tpart[ic] != tpart[ic + 1]: continue # If we dont match with next, skip
                hsym = True
                sym_col = ic + 1
                for offset in range(min(ic + 1, cols_len - ic -1)):
                    # print(tpart[ic - offset], tpart[ic + 1 + offset])
                    if tpart[ic - offset] != tpart[ic + 1 + offset]:
                        hsym = False
                        break
                if hsym:
                    break
            if hsym:
                print(f"{id} Horizontal on col: {sym_col}")
                cum += sym_col
                continue

            print(f"{id} is not symetric!")
        

    print(f"Part1: {cum}")
    print(f"Part2: {None}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
