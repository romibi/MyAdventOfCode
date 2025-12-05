from typing import List

from numpy import Infinity

PUZZLE_NR=2


class FreshRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_id_fresh(self, item_id: object) -> bool:
        return self.start <= item_id <= self.end


def main():
    # puzzle_input = read_input('day_05_puzzle_input_small.txt')
    puzzle_input = read_input('day_05_puzzle_input.txt')

    fresh_ranges, ingredients, lowest_id, higest_id = parse_input(puzzle_input)

    if PUZZLE_NR == 1:
        fresh_count = test_ingredients(fresh_ranges, ingredients)

        print("")
        print(f"Of the available ingredients there are {fresh_count} fresh items.")
    else:
        possible_fresh_count = count_fresh_ids(fresh_ranges, lowest_id, higest_id)
        print("")
        print(f"With the given ranges there are {possible_fresh_count} IDs considered fresh.")


def read_input(file):
    with open(file) as f:
        return f.readlines()


def parse_input(puzzle_input):
    line_nr = 0
    fresh_ranges = []
    ingredients = []

    lowest_id = +Infinity
    highest_id = -Infinity

    while puzzle_input[line_nr].strip() != '':
        range_line = puzzle_input[line_nr]
        parsed_range = parse_range(range_line)

        # Added for Part 2
        lowest_id = min(lowest_id, parsed_range.start)
        highest_id = max(highest_id, parsed_range.end)

        fresh_ranges += [parsed_range]
        line_nr += 1

    if PUZZLE_NR == 2:
        return fresh_ranges, None, lowest_id, highest_id

    line_nr += 1 # ignore empty line between blocks

    while line_nr < len(puzzle_input):
        ingredient_id = puzzle_input[line_nr].strip()
        ingredients += [int(ingredient_id)]
        line_nr += 1

    return fresh_ranges, ingredients, lowest_id, highest_id


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


def count_fresh_ids_starting_from(fresh_ranges: List[FreshRange], start_ingredient):
    it_list = fresh_ranges.copy()
    for fresh_range in it_list: # For Step 2 replaced fresh_ranges with a copy to be able to remove from passed list
        if fresh_range.is_id_fresh(start_ingredient):
            fresh_count = fresh_range.end - start_ingredient + 1
            print(f"Ingredient ID {start_ingredient} and all {fresh_count} ingredients of range {fresh_range.start}-{fresh_range.end} are fresh.")
            return fresh_count
        else:
            if start_ingredient > fresh_range.end:
                fresh_ranges.remove(fresh_range)

    print(f"Ingredient ID {start_ingredient} is spoiled.")
    return 0


def count_fresh_ids(fresh_ranges: List[FreshRange], lowest_id, highest_id):
    ingredient_id = lowest_id
    fresh_count = 0
    total_range_count = highest_id-lowest_id
    while ingredient_id <= highest_id:

        range_fresh_count = count_fresh_ids_starting_from(fresh_ranges, ingredient_id)
        if range_fresh_count > 0:
            fresh_count += range_fresh_count
            ingredient_id += range_fresh_count
        else:
            ingredient_id = get_smallest_id_of_range(fresh_ranges)

        perc = (ingredient_id-lowest_id)/total_range_count
        perc_text = "["+("="*int(perc*100))+(" "*int((1-perc)*100))+"]"
        print(perc_text)
    return fresh_count


def get_smallest_id_of_range(fresh_ranges: List[FreshRange]):
    result = Infinity
    for fresh_range in fresh_ranges:
        result = min(result, fresh_range.start)
    return result


if __name__ == '__main__':
    main()