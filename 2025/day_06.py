import re

PUZZLE_NR=2

def main():
    # puzzle_input = read_input('day_06_puzzle_input_small.txt')
    puzzle_input = read_input('day_06_puzzle_input.txt')

    math_ops = get_math_operators(puzzle_input)
    if PUZZLE_NR==1:
        grand_total = do_math_1(puzzle_input, math_ops)
    else:
        grand_total = do_math_2(puzzle_input, math_ops)

    print("")
    print(f"The grand total is {grand_total}")


def read_input(file):
    with open(file) as f:
        return f.readlines()


def get_math_operators(puzzle_input):
    math_op_string = puzzle_input[len(puzzle_input)-1].strip()
    math_ops = re.split(r" +", math_op_string)
    del puzzle_input[-1]
    return math_ops


def do_math_1(puzzle_input, math_ops):
    intermediate_results = re.split(r" +", puzzle_input[0].strip())
    intermediate_results = [int(x) for x in intermediate_results]
    del puzzle_input[0]

    for line in puzzle_input:
        numbers = re.split(r" +", line.strip())
        numbers = [int(x) for x in numbers]
        for n in range(0,len(numbers)):
            if math_ops[n] == "+":
                intermediate_results[n] += numbers[n]
            elif math_ops[n] == "*":
                intermediate_results[n] *= numbers[n]

    return sum(intermediate_results)


def do_math_2(puzzle_input, math_ops):
    math_puzzle_nr = 0
    # not sure if i've saved the file wrong (editor trimmed spaces at end of line) or it the puzzle output just is like this
    # this line (explicitly not trimming) did not help:
    #line_width = len(puzzle_input[0].replace("\n", "")) # do not use strip. space at the end might be relevant
    # lets loop to find the biggest value
    line_width = 0
    for line in puzzle_input:
        line_width = max(line_width, len(line.rstrip()))

    total_sum = 0
    intermediate_result = -1

    for n in range(0, line_width):
        number_string = ""
        for line in puzzle_input:
            if len(line)>n:
                number_string += line[n]

        if number_string.strip() == '':
            print(f" = {intermediate_result}")
            total_sum += intermediate_result
            # next math puzzle
            intermediate_result = -1
            math_puzzle_nr += 1
            continue

        parsed_number = int(number_string)
        if intermediate_result == -1:
            intermediate_result = parsed_number
            print(f"Result of {parsed_number}",end="")
        elif math_ops[math_puzzle_nr] == "+":
            intermediate_result += parsed_number
            print(f" + {parsed_number}", end="")
        elif math_ops[math_puzzle_nr] == "*":
            intermediate_result *= parsed_number
            print(f" * {parsed_number}", end="")

    print(f" = {intermediate_result}")
    total_sum += intermediate_result
    return total_sum



if __name__ == '__main__':
    main()