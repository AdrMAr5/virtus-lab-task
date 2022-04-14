import sys


class InvalidModeError(Exception):
    def __init__(self, modes):
        self.expected = '/'.join(modes)
        self.message = 'Invalid join mode'

    def __str__(self):
        return f'{self.message}. Expected: {self.expected}'


class InvalidColumnError(Exception):
    def __init__(self, col):
        self.col = col
        self.message = 'Column "{0}" does not appear in any file'

    def __str__(self):
        return self.message.format(self.col)


class Parser:
    @staticmethod
    def parse_line(line: str) -> list:
        line = line.rstrip()
        start_i = 0
        items = []
        quotes = 0
        for i, char in enumerate(line):
            if char == ',' and not quotes:
                items.append(line[start_i:i])
                start_i = i + 1

            if char == '"':
                quotes += 1

            try:
                if line[i + 1] == ',' and quotes % 2 == 0:
                    quotes = 0
            except IndexError:
                break

        items.append(line[start_i:])
        return items


class Line:
    @staticmethod
    def add_to_dict(list_of_items: list, keys_dict: dict):
        new_dict = {}
        for item, key in zip(list_of_items, keys_dict.keys()):
            new_dict[key] = item
        return new_dict

    @staticmethod
    def print_line(merged_dict: dict, order: list):
        out_line = ''
        for col in order:
            out_line += ',' + merged_dict[col]
        print(out_line[1:])


class Header:
    order = []

    def __init__(self, line):
        self.line = line
        self.list = Parser.parse_line(self.line)
        self.dict = self.list_to_dict()

    def list_to_dict(self):
        headers_dict = {}
        for i in self.list:
            headers_dict[i] = 'None'
        return headers_dict

    @staticmethod
    def merge_headers_keys(h1, h2) -> dict:
        merged_headers = h1.dict
        merged_headers.update(h2.dict)
        return merged_headers

    @staticmethod
    def set_order(h1, h2, key_col):
        if key_col not in h1.list and key_col not in h2.list:
            raise InvalidColumnError(key_col)

        headers_order = [key_col]
        headers_order += [h for h in h1.list if h not in headers_order]
        headers_order += [h for h in h2.list if h not in headers_order]
        return headers_order


class Joiner:
    @staticmethod
    def join(path1: str, path2: str, key_col: str, join_type: str = 'inner'):
        try:
            modes = {'inner', 'left', 'right'}
            if join_type not in modes:
                raise InvalidModeError(modes)
            if join_type == 'right':
                path1, path2 = path2, path1

            with open(path1, 'r') as f1, open(path2, 'r') as f2:
                f1_header = Header(f1.readline())
                f2_header = Header(f2.readline())

                Header.order = Header.set_order(f1_header, f2_header, key_col)

                print(','.join(Header.order))

                for f1_line in f1:
                    f1_line_list = Parser.parse_line(f1_line)
                    f1_items = Line.add_to_dict(f1_line_list, f1_header.dict)

                    matched = False
                    for f2_line in f2:
                        f2_line_list = Parser.parse_line(f2_line)
                        f2_items = Line.add_to_dict(f2_line_list, f2_header.dict)

                        if f1_items[key_col] == f2_items[key_col]:
                            to_print_dict = f1_items
                            to_print_dict.update(f2_items)
                            Line.print_line(to_print_dict, Header.order)
                            matched = True
                            break
                    if not matched:
                        if join_type != 'inner':
                            to_print_dict = f2_header.dict
                            to_print_dict.update(f1_items)
                            Line.print_line(to_print_dict, Header.order)
                    f2.seek(0)

        except KeyError as e:
            sys.stderr.write(e.__str__())

        except FileNotFoundError as e:
            sys.stderr.write(e.__str__())

        except InvalidModeError as e:
            sys.stderr.write(e.__str__())

        except InvalidColumnError as e:
            sys.stderr.write(e.__str__())
