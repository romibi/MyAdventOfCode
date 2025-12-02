def main():
    # input = read_input('day_02_puzzle_1_input_small.txt')
    input = read_input('day_02_puzzle_1_input.txt')
    ranges = parse_input(input)

    invalid_ids = test_ranges(ranges)

    invalid_ids_sum = sum(invalid_ids)
    print("")
    print(f"Sum of all invalid IDs: {invalid_ids_sum}")
    pass


def read_input(file):
    with open(file) as f:
        return f.readlines()


def parse_input(input):
    out_ranges = []
    for line in input: # although all is 1 line?
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


def test_range(arange):
    invalid_ids = []
    for x in range(arange[0], arange[1]+1): # inclusive ranges
        if not test_id(x):
            print(f"Range {arange[0]}-{arange[1]}: Invalid Id: {x}")
            invalid_ids += [x]
    return invalid_ids


def test_id(x):
    xstr = str(x)
    if (len(xstr) % 2) == 1: # length not divisible by 2: not one of the silly patterns
        return True

    first_half, second_half = xstr[:len(xstr) // 2], xstr[len(xstr) // 2:]

    if first_half == second_half:
        return False

    return True


if __name__ == '__main__':
    main()