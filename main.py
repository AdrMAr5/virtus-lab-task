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
            if start_i != i and line[i+1] == ',' and quotes % 2 != 0 and quotes > 1:
                print(quotes, char)
                quotes = 0
        except IndexError:
            break

    items.append(line[start_i:])
    return items


def match_headers(h1: list, h2: list, col_name: str) -> tuple:
    output_headers = set(h1).union(set(h2))
    cols_1 = [True if h1[i] in output_headers else False for i in range(len(h1))]
    cols_2 = [True if (h2[i] in output_headers and h2[i] not in h1) else False for i in range(len(h2))]
    return cols_1, cols_2


def headers_to_dict(lst: list):
    headers_dict = {}
    for i in lst:
        headers_dict[i] = None
    return headers_dict


def print_dict_in_order(merged_dict: dict, key_col: str):
    pass


def main():
    args = ['user_device.csv', 'user_usage.csv', 'use_id', 'left']
    try:
        # args = sys.argv[1:5]
        args = {'path1': args[0], 'path2': args[1], 'col_name': args[2], 'join_type': args[3]}
    except IndexError:
        print('to less arguments')
        sys.exit()

    if args['join_type'] == 'right':
        args['path1'], args['path2'] = args['path2'], args['path1']

    with open(args['path1'], 'r') as f1, open(args['path2'], 'r') as f2:
        f1_headers = headers_to_dict(parse_line( f1.readline().rstrip() ))
        f2_headers = headers_to_dict(parse_line( f2.readline().rstrip() ))
        print(f1_headers)
        print(f2_headers)

        for f1_line in f1:
            f1_line_list = parse_line(f1_line.rstrip())
            f1_items = {}
            for key1, item1 in zip(f1_headers.keys(), f1_line_list):
                f1_items[key1] = item1
            matched = False
            for f2_line in f2:
                f2_line_list = parse_line(f2_line.rstrip())
                f2_items = {}
                for key2, item2 in zip(f2_headers.keys(), f2_line_list):
                    f2_items[key2] = item2

                if f1_items[args['col_name']] == f2_items[args['col_name']]:
                    f1_items.update(f2_items)
                    print(f1_items)
                    matched = True
                    break
            if not matched:
                if args['join_type'] == 'left':
                    f2_headers.update(f1_items)
                    print(f2_headers)
                elif args['join_type'] == 'right':
                    f1_headers.update(f2_items)
                    print(f1_headers)

            f2.seek(0)


if __name__ == '__main__':
    main()
