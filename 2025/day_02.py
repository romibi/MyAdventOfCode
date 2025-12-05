PUZZLE_NR=2

def main():
    # puzzle_input = read_input('day_02_puzzle_input_small.txt')
    puzzle_input = read_input('day_02_puzzle_input.txt')
    ranges = parse_input(puzzle_input)

    invalid_ids = test_ranges(ranges)

    invalid_ids_sum = sum(invalid_ids)
    print("")
    print(f"Sum of all invalid IDs: {invalid_ids_sum}")
    pass


def read_input(file):
    with open(file) as f:
        return f.readlines()


def parse_input(puzzle_input):
    out_ranges = []
    for line in puzzle_input: # although all is 1 line?
        int_ranges = []
        string_ranges = line.split(',')
        for string_range in string_ranges:
            r = [int(range_num) for range_num in string_range.split('-')]
            int_ranges += [r]
        out_ranges += int_ranges
    return out_ranges


def test_ranges(ranges):
    invalid_ids = []
    for r in ranges:
        invalid_ids += test_range(r)
    return invalid_ids


def test_range(range_to_test):
    invalid_ids = []
    # print(f"Testing Range {range_to_test[0]}-{range_to_test[1]}")
    for x in range(range_to_test[0], range_to_test[1] + 1): # inclusive ranges
        if (PUZZLE_NR==1 and (not test_id_1(x))) or (PUZZLE_NR==2 and (not test_id_2(x))):
            print(f"Range {range_to_test[0]}-{range_to_test[1]}: Invalid Id: {x}")
            invalid_ids += [x]
    return invalid_ids


def test_id_1(x):
    xstr = str(x)
    if (len(xstr) % 2) == 1: # length not divisible by 2: not one of the silly patterns
        return True

    first_half, second_half = xstr[:len(xstr) // 2], xstr[len(xstr) // 2:]

    if first_half == second_half:
        return False

    return True


def test_id_2(x):
    xstr = str(x)

    for char_num in range(1, (len(xstr)//2)+1): # up until len divided by 2 because afterwards no repeating pattern possible
        pattern = xstr[:char_num]
        if len(xstr) % len(pattern) != 0:
            continue # pattern not fitting into id length: no nice pattern -> wrong pattern or valid id
        pattern_times = len(xstr) // len(pattern)
        str_match = pattern * pattern_times
        if xstr == str_match:
            return False # it's a silly pattern, not valid
    return True # no silly pattern found


if __name__ == '__main__':
    main()