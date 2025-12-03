PUZZLE_NR=2

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
        if PUZZLE_NR == 1:
            result += calculate_joltage_1(bank.strip())
        else: # PUZZLE_NR == 2
            result += calculate_joltage_2(bank.strip())

    return result


def calculate_joltage_1(bank):
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


def calculate_joltage_2(bank):
    digits = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    for char_num in range(0, len(bank)):
        current = int(bank[char_num])

        if digits[11] != -1:
            for d in range(0, 11):
                if digits[d+1] > digits[d]:
                    for dp in range(d, 11):
                        digits[dp] = digits[dp+1]
                    digits[11] = -1
                    break

        do_continue = False
        for d in range(0, 12):
            if digits[d] == -1:
                digits[d] = current
                do_continue = True
                break

        if do_continue:
            continue

        if current > digits[11]:
            digits[11] = current

    joltage = "".join(str(i) for i in digits)

    print(f"In {bank} the largest voltage is: {joltage}")
    return int(joltage)


if __name__ == '__main__':
    main()