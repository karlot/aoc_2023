from collections import defaultdict
# from rich.pretty import pprint

input_file = "input.txt"

def main():
    cards = defaultdict(int)

    with open(input_file, "r", encoding="utf8") as f:
        lines = [line.strip() for line in f.readlines()]

    total_points = 0
    for card in lines:
        [id, nums] = card.split(":")
        cid = int(id.split()[1])
        [winning, have] = nums.split("|")
        
        cards[cid] += 1

        card_data = {
            "win": winning.split(),
            "have": have.split(),
            "hits": 0,
            "points": 0,
        }
                
        for num in card_data["have"]:
            if num in card_data["win"]:
                card_data["hits"] += 1
                card_data["points"] = 1 if card_data["points"] == 0 else card_data["points"] * 2
        
        for i in range(card_data["hits"]):
            copy_id = cid + i + 1
            cards[copy_id] += cards[cid]

        total_points += card_data["points"]

    print(f"Part1: {total_points}")
    print(f"Part2: {sum(cards.values())}")


# ------------------------------
if __name__ == "__main__":
    main()