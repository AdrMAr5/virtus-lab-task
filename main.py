import sys
from csv_joiner import Joiner


class ArgumentsException(Exception):
    def __init__(self, arguments_quantity, message='Invalid quantity of arguments. Expected 4, given:'):
        self.quantity = arguments_quantity
        self.message = message

    def __str__(self):
        return f'{self.message} {self.quantity}'


def main():
    try:
        args = ['user_device.csv', 'user_usage.csv', 'use_id', 'inne']
        # args = sys.argv

        if len(args) != 4:
            raise ArgumentsException(len(args))

        Joiner.join(*args)

    except ArgumentsException as e:
        sys.stderr.write(e.__str__())


if __name__ == '__main__':
    main()
