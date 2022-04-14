import sys
from csv_joiner import Joiner, Parser


class ArgumentsException(Exception):
    def __init__(self, arguments_quantity, message='Invalid quantity of arguments. Expected 4, given:'):
        self.quantity = arguments_quantity
        self.message = message

    def __str__(self):
        return f'{self.message} {self.quantity}'


def main():
    try:
        # args = ['user_device.csv', 'user_usage.csv', 'use_id', 'inner']
        args = sys.argv

        if len(args) != 5:
            raise ArgumentsException(len(args))

        Joiner.join(*args[1:])

    except ArgumentsException as e:
        sys.stderr.write(e.__str__())


if __name__ == '__main__':
    # main()
    for i in ['314,752,81,""vcbc""', '43.03,0.47,2076.45,22884',
                 '22893,29672,ios,10.1,"iPhone9,3",3', '317,222,29,"""."',
                 '312,102,32,"r,,,""bb"', '314,752,81,""vcbc""']:
        print(Parser.parse_line(i))
