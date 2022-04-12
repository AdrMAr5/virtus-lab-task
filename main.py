import sys


def parse_line(line: str) -> list:
    start_i = 0
    items = []
    quotes = 0
    for i, char in enumerate(line):
        # print(quotes)
        if char == ',' and not quotes:
            items.append(line[start_i:i])
            start_i = i+1

        if char == '"':
            quotes += 1

        try:
            if start_i != i and line[i+1] == ',' and quotes%2 != 0 and quotes>1:
                print(quotes, char)
                quotes = 0
        except IndexError:
            break

    items.append(line[start_i:])
    return items


def match_headers(h1: list, h2: list) -> tuple:
    output_headers = set(h1).union(set(h2))
    cols_1 = [True if h1[i] in output_headers else False for i in range(len(h1))]
    cols_2 = [True if (h2[i] in output_headers and h2[i] not in h1) else False for i in range(len(h2))]
    return cols_1, cols_2


def main():
    args = ['/plik.csv', 'plik2.csv', 'use_id', 'inner']
    try:
        #args = sys.argv[1:5]
        args = {'path1': args[0], 'path2': args[1], 'col_name': args[2], 'join_type': args[3]}
    except IndexError:
        print('to less arguments')
        sys.exit()

    with open('user_device.csv', 'r') as f1, open('user_usage.csv', 'r') as f2:
        f1_headers = parse_line(f1.readline().rstrip())
        f2_headers = parse_line(f2.readline().rstrip())
        cols1_to_print, cols2_to_print = match_headers(f1_headers, f2_headers)

        key_ind1 = f1_headers.index(args['col_name'])
        key_ind2 = f2_headers.index(args['col_name'])
        output_line = [f1_headers[i] if cols1_to_print[i] else '' for i in range(len(f1_headers))]
        output_line += [f2_headers[i] if cols2_to_print[i] else '' for i in range(len(f2_headers))]
        print(','.join(output_line))
        for f1_line in f1:
            f1_line_items = parse_line(f1_line.rstrip())

            for f2_line in f2:
                f2_line_items = parse_line(f2_line.rstrip())

                if f1_line_items[key_ind1] == f2_line_items[key_ind2]:
                    try:
                        output_line = [f1_line_items[i] if cols1_to_print[i] else '' for i in range(len(f1_line_items))]
                        output_line += [f2_line_items[i] if cols2_to_print[i] else '' for i in range(len(f2_line_items))]
                        print(','.join(output_line))
                    except IndexError:
                        print('ddddddddddddddddddddddddddddddddddddddddd')

            f2.seek(0)


if __name__ == '__main__':
    main()
