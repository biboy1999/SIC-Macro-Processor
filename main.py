from functools import reduce
from pprint import pprint
from re import compile
from collections import deque

sic_parse = compile(r"^(\s+|\S*)\s?(\S+)\s*(\s*|\S*)$")


def parse_line(line):
    if line.startswith("."):
        return []
    symbol, op, args = sic_parse.findall(line)[0]
    # clean whitespace
    symbol = symbol.strip()
    op = op.strip()
    args = args.strip()

    return {"symbol": symbol, "op": op, "args": args}

def process_line(content: deque):
    # macro_symbol = ""
    level = []
    name_table = []
    def_table = {}
    arg_table = {}
    while content:
        line = content.popleft()
        if line["op"] == "MACRO":
            level.append(line["symbol"])
            name_table.append(line["symbol"])
            def_table[line["symbol"]] = []
            arg_table[line["symbol"]] = {}
            for idx, arg in enumerate(line["args"].split(",")):
                arg_table[line["symbol"]][arg] = ""
                arg_table[line["symbol"]][idx] = arg

        elif line["op"] == "MEND":
            level.pop()
            pass
        elif level:
            def_table[level[-1]].append(line)
            pass
        elif line["op"] in name_table:
            macro_lines = def_table[line["op"]]
            for idx,arg in enumerate(line["args"].split(",")):
                key = arg_table[line["op"]][idx]
                arg_table[line["op"]][key] = arg

            arg_replaced_lines = []
            for mline in macro_lines:
                for arg in arg_table[line["op"]]:
                    if isinstance(arg, str):
                        mline["args"] = mline["args"].replace(arg,arg_table[line["op"]][arg])
                arg_replaced_lines.append(mline)
            
            content.extendleft(reversed(arg_replaced_lines))
            content[0]["symbol"] = line["symbol"]

        else:
            outfile.write("{}\t{}\t{}\n".format(
                line["symbol"], line["op"], line["args"]))


if __name__ == "__main__":
    with open("output.txt", "w") as outfile:
        with open("input.txt", "r") as infile:
            content = infile.read()
            content = [line for line in content.splitlines() if line.strip()]
            content = [parse_line(i) for i in content]
            content = [i for i in content if i]
            content = deque(content)
            process_line(content)
