#!/usr/bin/env python3


class Indexer:
    def __init__(self, sep=" -", max_depth=None, new_indent=1, new_shift=1):
        self.spaces = -1
        self.level = -1
        self.levels_depths = []
        self.levels_counters = []

        self.custom_sep = sep
        self.max_depth = max_depth
        self.new_shift = new_shift
        self.new_indent = new_indent

        self.new_index = {}

    # @staticmethod
    def indent_spaces(self, string):
        stripped = string.lstrip(" ")
        try:
            if not stripped[0].isspace():
                return len(string) - len(stripped)
            else:
                raise ValueError(
                    f"Bad indent in line:\n{string}\n{len(self.levels_depths)}"
                )
        except IndexError:
            return "empty"

    def get_line(self, line):
        # skip empty lines
        if not line:
            return

        sp = self.indent_spaces(line)
        if sp == "empty":
            return

        if sp > self.spaces:
            self.level += 1
            self.levels_depths += [sp]
            self.levels_counters += [0]
        elif sp < self.spaces:
            self.level = self.levels_depths.index(sp)
            self.levels_depths = self.levels_depths[0 : (self.level + 1)]
            self.levels_counters = self.levels_counters[0 : (self.level + 1)]

        self.levels_counters[self.level] += 1
        self.spaces = sp

        idx_prefix = ".".join([str(x) for x in self.levels_counters])
        idx_desc = line.lstrip(" ")
        self.new_index.update({idx_prefix: idx_desc})

    def format_line(self, key):
        idx_prefix = key
        idx_desc = self.new_index[key]

        rep_line = (
            " " * self.new_shift
            + " " * self.new_indent * idx_prefix.count(".")
            + idx_prefix
            + self.custom_sep
            + " "
            + idx_desc
        )

        return rep_line


def is_key_prefix(pattern, key):
    equal = pattern == key
    prefix = key.startswith(pattern)
    return equal or prefix


if __name__ == "__main__":
    import argparse
    import inspect
    import sys

    _usage = """
    Print index:
    -----------

     print_idx [starts_with [max_depth]]

     max_depth:
         optional,
    """
    usage = inspect.cleandoc(_usage)

    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument("file", type=str)
    parser.add_argument(
        "-s",
        "--starts-with",
        type=str,
        default="",
        help="the pattern that index key has to match",
    )
    parser.add_argument(
        "-d",
        "--max-depth",
        type=int,
        default=None,
        help="the maximum depth printed, counted from the level of starts_with argument",
    )
    parser.add_argument("-i", "--new-indent", type=int, default=2)

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    starts_with = args.starts_with
    max_depth = args.max_depth
    idx = Indexer(") ", max_depth=max_depth, new_indent=args.new_indent)

    with open(args.file, "r") as file:
        # skip first line
        first_line = next(file)

        for line in file.readlines():
            line = line[:-1]  # strip newline
            idx.get_line(line)

    # PRINT SELECTED INDEX
    print(first_line)
    for key in idx.new_index.keys():
        if is_key_prefix(starts_with, key):
            depth = key.count(".") - starts_with.count(".")

            if max_depth is not None and depth > max_depth:
                continue
            else:
                print(idx.format_line(key))
