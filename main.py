def main():
    with open('user_device.csv', 'r') as f1, open('user_usage.csv', 'r') as f2:
        for f1_line, f2_line in zip(f1, f2):
            f1_line_items, f2_line_items = f1_line.rstrip().split(','), f2_line.rstrip().split(',')
            print(f1_line_items, f2_line_items)


if __name__ == '__main__':
    main()
