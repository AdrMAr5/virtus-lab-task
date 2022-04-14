# virtus-lab-task
Task on account of recruitment process

## Main targets
1. Script has to join two csv files using a specified column
2. Results should be printed to std out
3. Executable file with parameters to pass in
4. File cannot load all files into memory
5. csv files always have headers
6. Default join type 
7. Handling invalid parameters passed

## Instruction
To use the program you need to download the right executable file depending on which system you work. Then you should open terminal and go to directory with newly
downloaded file. To run it you should type something like this on windows:  join {path1} {path2} {column_name} {join_type}(optional) 

## Description of main issues
According to definition of csv format:
* each record is in a separate line
* last record may not have ending line break
* each line consists of the same number of fields separated by commas
* field may be enclosed with double quotes but if it's not there can't be double quotes inside
* fields containing commas, line breaks and double quotes must be enclosed with double quotes
* double quotes inside field enclosed with double quotes must be preceded with another

One challenge was to parse the lines properly. Algorithm solving this problem had to recognize fields enclosed with double quotes and also
inner commas and other double quotes. Solving this problem was possible by simply counting the number of double quotes in current field
and the fact that number of ending quote is always even and the next character is separating comma. 
Code:
```python
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
```

Next issue was to properly join files. My first idea was about using lists to store lines, but code wasn't clear and it was hard to operate on lists
when it came to settling about the order of printing. Next version included dictionaries to be able to easily acces fields in any order. At the beginning of the files
headers are loaded to dictionaries as a keys and then every line is parsed and then fields are put into dictionary as a values to matching keys.
To match the same values in specified column in two files I used simple nested loops and when same values from two files meet the line is printed and that is all for inner join.
Left and right join are almost the same but different files are the "main" file so I decided to implement right join as left join but switching the paths before reading files.
To make left join or "my right join" I just added a new bool which is set to True only when there is a match in other file, so when its value is False after finishing the inner
loop it means that there is no match and missing values are set to Null. Here is a code:
```python
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
```                    

First version of solution was simple funtions-based program. I decided to change it and make more universal so that anybody can import my module and use the code.
That is why I switched to using classes for various functionalities. Now anybody can import my code and use it to join the csv files.
Everything got fitted with some Exceptions handling so that program would inform what went wrong and what is expected.





