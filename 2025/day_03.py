PUZZLE_NR=1

def main():
    # input = read_input('day_03_puzzle_1_input_small.txt')
    input = read_input('day_03_puzzle_1_input.txt')

    total_joltage = calculate_total_joltage(input)

    print("")
    print(f"The total joltage is {total_joltage}")

    pass


def read_input(file):
    with open(file) as f:
        return f.readlines()


def calculate_total_joltage(input):
    result = 0
    for bank in input:
        result += calculate_joltage(bank.strip())
    return result


def calculate_joltage(bank):
    biggest_digit = -1
    biggest_digit_after = -1

    for char_num in range(0, len(bank)):
        current = int(bank[char_num])
        if biggest_digit_after > biggest_digit:
            biggest_digit = biggest_digit_after
            biggest_digit_after = -1

        if biggest_digit == -1:
            biggest_digit = current
            continue

        if current > biggest_digit_after:
            biggest_digit_after = current

    print(f"In {bank} the largest voltage is: {biggest_digit}{biggest_digit_after}")
    return biggest_digit*10+biggest_digit_after


if __name__ == '__main__':
    main()