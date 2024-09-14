import argparse
import math
import sys


def read_file(infile: str) -> bytes:
    if infile == "-":
        return sys.stdin.buffer.read()
    with open(infile, "rb") as fp:
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


def hexdump(
    data: bytes, cols: int, groupsize: int, uppercase: bool, fp=sys.stdout
) -> None:
    # length = len(data)
    width = 10 + cols * 2 + math.ceil(cols / groupsize)

    for i in range(0, len(data), cols):
        row_data = data[i : i + cols]

        row = f"{i:08x}: "
        # print(row_data)

        # print(row_data)
        for j in range(0, len(row_data), groupsize):
            row += (
                "".join(
                    f"{x:02X}" if uppercase else f"{x:02x}"
                    for x in row_data[j : j + groupsize]
                )
                + " "
            )

        row += " " * (width - len(row))
        row += " " + row_data.replace(b"\x00", b".").replace(b"\x0a", b".").decode(
            "utf-8"
        )
        fp.write(row + "\n")
        # print(row)


def main() -> None:
    args = parse_args()
    data = read_file(args.infile)

    cols = min(args.cols, 256)
    groupsize = min(args.groupsize, cols)
    hexdump(data, cols, groupsize, args.u)


if __name__ == "__main__":
    main()
