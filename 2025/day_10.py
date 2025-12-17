from typing import List

from numpy import Infinity

PUZZLE_NR=2
USE_SMALL=False

class ButtonPressIterator: # used for Puzzle 2
    def __init__(self, button_count, max_joltage):
        self.button_count = button_count
        self.max_joltage = max_joltage
        # todo: instead of one max_joltage per button one max_joltage that is the smallest number of the joltage slots it influences
        # todo: also add min_joltage per button which is its max_joltage minus all max_joltages of buttons that influence the same joltage slots
        # todo: also add a max button press num which can be input from outside to skip all further iterations over that sum
        # todo: ... then it might be fast enough but i doubt it ... i assume something with equations needs to be done ...
        self.current_buttons = [0] * self.button_count

    def __iter__(self):
        return self

    def __next__(self):
        self.current_buttons[0] += 1
        for button_num in range(0,self.button_count):
            if self.current_buttons[button_num] > self.max_joltage:
                self.current_buttons[button_num] = 0
                if button_num+1 >= self.button_count:
                    raise StopIteration
                self.current_buttons[button_num+1] += 1
            else:
                break
        return self.current_buttons



class Machine:
    def __init__(self, config_string):
        self.config_string = config_string
        self.lights = 0b0
        self.buttonsbin = []
        self.buttonsint = []
        self.joltages = None
        self.parse_config()

    def parse_config(self):
        def convert_light_config(string):
            config = 0b0
            val = 0b1
            for char in string:
                if char == '#':
                    config += val
                val = val << 1
            # print(f"lights config: {bin(config)}")
            return config


        def convert_button_config(strings):
            buttonsbin = []
            buttonsint = []
            for button_config in strings:
                button_value = 0b0
                button_config = button_config.strip('(').strip(')').split(',')
                for wire in button_config:
                    button_value += 0b1 << int(wire)

                # print(f"Button with wiring {bin(button_value)}")
                buttonsbin.append(button_value)
                buttonsint.append([int(x) for x in button_config])
            return buttonsbin, buttonsint

        def convert_joltage_config(string):
            joltage_config = string.strip('{').strip('}').split(',')
            return [int(x) for x in joltage_config]

        light_config_string, rest_config = self.config_string.split(']', 1)
        light_config_string = light_config_string[1:]
        button_config_string, joltage_config_string = rest_config.split('{',1)
        button_configs = button_config_string.strip().split(' ')
        joltage_config_string = joltage_config_string[:-1]

        print(f"the config strings are: {light_config_string},{button_configs},{joltage_config_string}")

        self.lights = convert_light_config(light_config_string)
        self.buttonsbin, self.buttonsint = convert_button_config(button_configs)
        self.joltages = convert_joltage_config(joltage_config_string)


    def solve_1(self):
        count = len(self.buttonsbin)
        button_config_count = 0b1 << count
        min_button_count = Infinity
        min_button_presses = 0
        # todo: iterator to iterate instead of over 0 and 1 per bit/button over 0-"max joltage" per digit/button
        for config_num in range(1, button_config_count):
            resulting_lights = 0b0
            current_button = 0b1
            button_count = 0
            for button in self.buttonsbin:
                if config_num & current_button != 0:
                    resulting_lights = resulting_lights ^ button
                    button_count += 1
                current_button = current_button << 1
            if self.lights == resulting_lights:
                min_button_count = min(min_button_count, button_count)
                if min_button_count == button_count:
                    min_button_presses = config_num
                # print(f"For machine with lights {bin(self.lights)}: config {bin(config_num)} results in lights {bin(resulting_lights)} with {button_count} button presses")
        print(f"For machine with lights {bin(self.lights)} button presses {bin(min_button_presses)} ({min_button_count}) is a way to go.")
        return min_button_count

    def solve_2(self):
        count = len(self.buttonsint)
        # button_config_count = 0b1 << count
        min_button_count = Infinity
        min_button_presses = [0] * count
        min_button_config = None

        iterator = ButtonPressIterator(count, max(self.joltages))

        # todo: iterator to iterate instead of over 0 and 1 per bit/button over 0-"max joltage" per digit/button
        for button_config in iterator:
            # resulting_lights = 0b0
            resulting_joltages = [0] * len(self.joltages)
            # current_button = 0b1
            button_count = sum(button_config)
            for button_num in range(0,len(button_config)):
                for wire in self.buttonsint[button_num]:
                    resulting_joltages[wire] += button_config[button_num]

            if self.joltages == resulting_joltages:
                min_button_count = min(min_button_count, button_count)
                if min_button_count == button_count:
                    min_button_presses = button_count
                    min_button_config = button_config.copy()
                # print(f"For machine with joltages {self.joltages}: config {button_config} results in joltages {resulting_joltages} with {button_count} button presses")
            # else:
            #     print(f"{button_config}: miss! {self.joltages} != {resulting_joltages}")
        print(f"For machine with joltages {self.joltages} button presses {min_button_config} ({min_button_count}) is a way to go.")
        return min_button_count


def main():
    if USE_SMALL:
        puzzle_input = read_input('day_10_puzzle_input_small.txt')
    else:
        puzzle_input = read_input('day_10_puzzle_input.txt')

    machines = parse_input(puzzle_input)
    button_presses = solve_machines(machines)

    print("")
    print(f"In total there are {button_presses} button presses needed.")

def read_input(file):
    with open(file) as f:
        return f.readlines()


def parse_input(puzzle_input) -> List[Machine]:
    machines: List[Machine] = []
    for line in puzzle_input:
        machine = Machine(line.strip())
        machines.append(machine)

    return machines

def solve_machines(machines):
    button_presses = 0
    for machine in machines:
        if PUZZLE_NR == 1:
            machine_button_presses = machine.solve_1()
        else:
            machine_button_presses = machine.solve_2()
        button_presses += machine_button_presses
    return button_presses

if __name__ == '__main__':
    main()