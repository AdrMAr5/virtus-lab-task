def parse_line(line):
    start_i = 0
    items = []
    quotes = 0
    for i, char in enumerate(line):
        if char == '"':
            quotes += 1

        elif char == ',' and not quotes:
            items.append(line[start_i:i])
            start_i = i+1
            if line[start_i] == '"':
                quotes = 1
        try:
            if start_i != i and line[i+1] == ',' and quotes%2 != 0:      # if
                quotes = 0
        except IndexError:
            break

    items.append(line[start_i:])
    return items


def parse_line2(line):
    start = 0
    items = []
    in_quotes = line[0] == '"'
    while start < len(line):

        if in_quotes:
            while True:
                next_separator = line[start:].index('",').next()
                if next_separator != line[start:].index('"",'):
                    break
        else:
            next_separator = line[start:].index(',')
        items.append(line[start])


def main():
    with open('user_device.csv', 'r') as f1, open('user_usage.csv', 'r') as f2:
        col_name = 'use_id'
        f1_headers = f1.readline()
        f2_headers = f2.readline()
        for f1_line in f1:
            f1_line_items = parse_line(f1_line.rstrip())
            for f2_line in f2:

                f2_line_items = parse_line(f2_line.rstrip())

                if f1_line_items[0] == f2_line_items[-1]:
                    print(f1_line_items, f2_line_items)
            f2.seek(0)


if __name__ == '__main__':
    main()



