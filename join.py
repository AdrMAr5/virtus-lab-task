import sys
from csv_joiner import Joiner


def main():
    try:
        args = ['D:/projekty python/virtus-lab-task/files/user_device.csv', 'D:/projekty python/virtus-lab-task/files/user_usage.csv']
        args = sys.argv

        Joiner.join(*args[1:])

    except TypeError as e:
        sys.stderr.write(e.__str__())


if __name__ == '__main__':
    main()
