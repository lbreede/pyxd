import argparse
import sys
import math


def read_file(infile: str) -> str:
    if infile == "-":
        return sys.stdin.read()
    with open(infile, "r", encoding="utf-8") as fp:
        return fp.read()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", type=str, nargs="?", default="-")
    parser.add_argument(
        "-c",
        "--cols",
        type=int,
        default=16,
        help="Format <cols> octets per line. Default 16 (-i: 12, -ps: 30, -b: 6). Max 256.",
    )
    parser.add_argument("-g", "--groupsize", type=int, default=2)
    parser.add_argument(
        "-u",
        action="store_true",
        help="Use upper-case hex letters. Default is lower-case.",
    )
    return parser.parse_args()


def hexdump(data: str, cols: int, groupsize: bytes, uppercase: bool) -> str:
    length = len(data)
    width = 10 + cols * 2 + math.ceil(cols / groupsize)

    output = ""
    for i in range(0, length, cols):
        row_data = data[i : i + cols]

        row = f"{i:08x}: "

        for j in range(0, len(row_data), groupsize):
            row += (
                "".join(
                    f"{ord(x):02X}" if uppercase else f"{ord(x):02x}"
                    for x in row_data[j : j + groupsize]
                )
                + " "
            )

        row += " " * (width - len(row))
        row += " " + row_data.replace("\n", ".").replace("\r", ".")
        output += row + "\n"
    return output


def main() -> None:
    args = parse_args()
    data = read_file(args.infile)

    cols = min(args.cols, 256)
    groupsize = min(args.groupsize, cols)
    dump = hexdump(data, cols, groupsize, args.u)
    print(dump)


if __name__ == "__main__":
    main()
