import sys
from collections import defaultdict


def find_total_winnings(lines, card_strengths):
    """
    Parses lines based on defined card strengths, and returns total winnings
    When card strength is set to 1, its considered a Joker wild card
    """
    # Stores all possible hand types
    hand_types = [[],[],[],[],[],[],[]]

    # Parse all lines
    for line in lines:
        hand, bid = line.split()
        hand_int = [card_strengths[c]for c in hand]

        # Make map of each card to their count in the hand
        hand_map = defaultdict(int)
        for c in hand_int:
            hand_map[c] += 1

        # Edge case when only Jokers are in the hand
        if len(hand_map.keys()) == 1 and 1 in hand_map:
            hand_types[6].append((hand_int, int(bid)))
            continue
        
        # When checking for any maximum card number, we should not consider Joker card!
        no_joker_map = {x: y for x, y in hand_map.items() if x != 1}
        non_joker_best_card = max(no_joker_map, key=no_joker_map.get)
        if 1 in hand_map:
            hand_map[non_joker_best_card] += hand_map[1]
            del hand_map[1]

        sorted_vals = sorted(hand_map.values())
        match sorted_vals:
            case [5]:
                hand_types[6].append((hand_int, int(bid)))  # Five of a kind
            case [1, 4]:
                hand_types[5].append((hand_int, int(bid)))  # Four of a kind
            case [2, 3]:
                hand_types[4].append((hand_int, int(bid)))  # Full house
            case [1, 1, 3]:
                hand_types[3].append((hand_int, int(bid)))  # Three of a kind
            case [1, 2, 2]:
                hand_types[2].append((hand_int, int(bid)))  # Two pair
            case [1, 1, 1, 2]:
                hand_types[1].append((hand_int, int(bid)))  # One pair
            case [1, 1, 1, 1, 1]:
                hand_types[0].append((hand_int, int(bid)))  # High card
            case _:
                print(hand, hand_int, non_joker_best_card, hand_map, sorted_vals)
                print("UNHANDLED CASE!")
    
    total_ranking = []
    for ht in hand_types:
        for hand in sorted(ht):
            total_ranking.append(hand)
    
    total_winning = 0
    for r, h in enumerate(total_ranking):
        total_winning += (r + 1) * h[1]

    return total_winning


def main(filename):
    """
    # Results:
    Part1: 249726565
    Part2: 251135960
    """
    with open(filename, "r") as f:
        lines = f.readlines()

    # --- [ Part 1 ]
    #                         +-- Enumeration offset set to 2
    card_strengths = { x: i + 2 for i, x in enumerate(reversed("A K Q J T 9 8 7 6 5 4 3 2".split(" "))) }
    print(f"Part1: {find_total_winnings(lines, card_strengths)}")

    # --- [ Part 2 ]
    #                         +-- Enumeration offset set to 1, to detect JOKER sa smallest card (1)
    card_strengths = { x: i + 1 for i, x in enumerate(reversed("A K Q T 9 8 7 6 5 4 3 2 J".split(" "))) }
    print(f"Part2: {find_total_winnings(lines, card_strengths)}")
            

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Provide input file!")
        exit(1)
    main(sys.argv[1])
