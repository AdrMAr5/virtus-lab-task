import sys
from csv_joiner import Joiner


class ArgumentsException(Exception):
    def __init__(self, arguments_quantity, message='Invalid quantity of arguments. Expected 4, given:'):
        self.quantity = arguments_quantity
        self.message = message

    def __str__(self):
        return f'{self.message} {self.quantity}'


def main():
    args = ['user_device.csv', 'user_usage.csv', 'use_id']
    # args = sys.argv

    if len(args) != 4:
        raise ArgumentsException(len(args))

    Joiner.join(*args)


if __name__ == '__main__':
    main()
