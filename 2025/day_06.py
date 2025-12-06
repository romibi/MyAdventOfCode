import re

PUZZLE_NR=1

def main():
    # puzzle_input = read_input('day_06_puzzle_input_small.txt')
    puzzle_input = read_input('day_06_puzzle_input.txt')

    math_ops = get_math_operators(puzzle_input)
    grand_total = do_math(puzzle_input, math_ops)

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


def do_math(puzzle_input, math_ops):
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

if __name__ == '__main__':
    main()