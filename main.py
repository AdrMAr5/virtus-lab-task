import sys


def parse_line(line: str) -> list:
    start_i = 0
    items = []
    quotes = 0
    for i, char in enumerate(line):
        if char == ',' and not quotes:
            items.append(line[start_i:i])
            start_i = i+1

        if char == '"':
            quotes += 1

        try:
            if line[i+1] == ',' and quotes % 2 == 0:
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
        headers_dict[i] = 'None'
    return headers_dict


def add_to_dict(list_of_items: list, keys_dict: dict):
    new_dict = {}
    for item, key in zip(list_of_items, keys_dict.keys()):
        new_dict[key] = item
    return new_dict


def print_dict_in_order(merged_dict: dict, order: list):
    out_line = ''
    for col in order:
        out_line += ',' + merged_dict[col]
    print(out_line[1:])


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
        f1_headers_list = parse_line(f1.readline().rstrip())
        f1_headers = headers_to_dict(f1_headers_list)
        f2_headers_list = parse_line(f2.readline().rstrip())
        f2_headers = headers_to_dict(f2_headers_list)
        merged_headers = f1_headers
        merged_headers.update(f2_headers)
        headers_order = [args['col_name']]
        headers_order += [h for h in f1_headers_list if h not in headers_order]
        headers_order += [h for h in f2_headers_list if h not in headers_order]

        print(','.join(headers_order))

        for f1_line in f1:
            f1_line_list = parse_line(f1_line.rstrip())
            f1_items = add_to_dict(f1_line_list, f1_headers)

            matched = False
            for f2_line in f2:
                f2_line_list = parse_line(f2_line.rstrip())
                f2_items = add_to_dict(f2_line_list, f2_headers)

                if f1_items[args['col_name']] == f2_items[args['col_name']]:
                    new = f1_items
                    new.update(f2_items)
                    print_dict_in_order(new, headers_order)
                    matched = True
                    break
            if not matched:
                if args['join_type'] != 'inner':
                    new = f2_headers
                    new.update(f1_items)
                    print_dict_in_order(new, headers_order)

            f2.seek(0)


if __name__ == '__main__':
    main()
    # print(parse_line('22782,26980,ios,10.2,"iPhon"",e7,2",2'))
    # print('22782,26980,ios,10.2,"iPhon,e7,2",2')
