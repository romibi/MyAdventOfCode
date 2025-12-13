from typing import List

from numpy import Infinity

PUZZLE_NR=1
USE_SMALL=False

class Machine:
    def __init__(self, config_string):
        self.config_string = config_string
        self.lights = 0b0
        self.buttons = []
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
            buttons = []
            for button_config in strings:
                button_value = 0b0
                button_config = button_config.strip('(').strip(')').split(',')
                for wire in button_config:
                    button_value += 0b1 << int(wire)

                # print(f"Button with wiring {bin(button_value)}")
                buttons.append(button_value)
            return buttons

        def convert_joltage_config(string):
            return None

        light_config_string, rest_config = self.config_string.split(']', 1)
        light_config_string = light_config_string[1:]
        button_config_string, joltage_config_string = rest_config.split('{',1)
        button_configs = button_config_string.strip().split(' ')
        joltage_config_string = joltage_config_string[:-1]

        print(f"the config strings are: {light_config_string},{button_configs},{joltage_config_string}")

        self.lights = convert_light_config(light_config_string)
        self.buttons = convert_button_config(button_configs)
        self.joltages = convert_joltage_config(joltage_config_string)



    def solve(self):
        count = len(self.buttons)
        button_config_count = 0b1 << count
        min_button_count = Infinity
        min_button_presses = 0
        for config_num in range(1, button_config_count):
            resulting_lights = 0b0
            current_button = 0b1
            button_count = 0
            for button in self.buttons:
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
        machine_button_presses = machine.solve()
        button_presses += machine_button_presses
    return button_presses

if __name__ == '__main__':
    main()