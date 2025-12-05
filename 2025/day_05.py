from typing import List

PUZZLE_NR=1


class FreshRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_id_fresh(self, item_id: object) -> bool:
        return self.start <= item_id <= self.end


def main():
    # input = read_input('day_05_puzzle_1_input_small.txt')
    input = read_input('day_05_puzzle_1_input.txt')

    fresh_ranges, ingredients = parse_input(input)
    fresh_count = test_ingredients(fresh_ranges, ingredients)

    print("")
    print(f"Of the available ingredients there are {fresh_count} fresh items.")


def read_input(file):
    with open(file) as f:
        return f.readlines()


def parse_input(input):
    line_nr = 0
    fresh_ranges = []
    ingredients = []
    while input[line_nr].strip() != '':
        range_line = input[line_nr]
        parsed_range = parse_range(range_line)
        fresh_ranges += [parsed_range]
        line_nr += 1

    line_nr += 1 # ignore empty line between blocks

    while line_nr < len(input):
        ingredient_id = input[line_nr].strip()
        ingredients += [int(ingredient_id)]
        line_nr += 1

    return fresh_ranges, ingredients


def parse_range(range_str):
    range_split = range_str.strip().split('-')
    return FreshRange(int(range_split[0]), int(range_split[1]))


def test_ingredients(fresh_ranges: List[FreshRange], ingredients):
    fresh_count = 0
    for ingredient in ingredients:
        if test_ingredient(fresh_ranges, ingredient):
            fresh_count += 1

    return fresh_count


def test_ingredient(fresh_ranges: List[FreshRange], ingredient):
    for fresh_range in fresh_ranges:
        if fresh_range.is_id_fresh(ingredient):
            print(f"Ingredient ID {ingredient} is fresh because it falls into range {fresh_range.start}-{fresh_range.end}.")
            return True

    print(f"Ingredient ID {ingredient} is spoiled.")
    return False

if __name__ == '__main__':
    main()