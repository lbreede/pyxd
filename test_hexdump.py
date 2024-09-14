import argparse
import logging
import os
import subprocess
import time

from tqdm import trange

import hexdump

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(message)s", level=logging.DEBUG)

FILENAME = "lorem.txt"
TEST_DIR = "test"


def test_hexdump(min_cols: int = 1, max_cols: int = 256) -> None:
    with open(FILENAME, "rb") as fp:
        data = fp.read()

    logger.info("🧪 Testing hexdump from %i to %i", min_cols, max_cols)
    results = []
    start = time.time()
    for cols in trange(min_cols, max_cols + 1):
        for groupsize in range(1, cols + 1):
            results.append(test_single_hexdump(data, cols, groupsize, False))
            results.append(test_single_hexdump(data, cols, groupsize, True))
    logger.info("Time taken: %.2f seconds", time.time() - start)
    if all(results):
        logger.info("🎉 All tests passed")
        os.rmdir(TEST_DIR)
    else:
        logger.error("❌ Some tests failed")


def run_single_hexdump(data: bytes, cols: int, groupsize: int, uppercase: bool) -> str:
    case = "upper" if uppercase else "lower"
    file = f"{TEST_DIR}/pyxd-{cols}-{groupsize}-{case}.txt"
    with open(file, "w", encoding="utf-8") as fp:
        hexdump.hexdump(data, cols, groupsize, uppercase, fp=fp)
    return file


def run_single_xxd(cols: int, groupsize: int, uppercase: bool) -> str:
    case = "upper" if uppercase else "lower"
    args = ["xxd", "-c", str(cols), "-g", str(groupsize)]
    if uppercase:
        args.append("-u")
    args.append(FILENAME)
    file = f"{TEST_DIR}/xxd-{cols}-{groupsize}-{case}.txt"
    with open(file, "w", encoding="utf-8") as fp:
        subprocess.run(args, check=True, stdout=fp)
    return file


def test_single_hexdump(
    data: bytes, cols: int, groupsize: int, uppercase: bool
) -> bool:
    if not os.path.isdir(TEST_DIR):
        os.makedirs(TEST_DIR)

    file_a = run_single_hexdump(data, cols, groupsize, uppercase)
    file_b = run_single_xxd(cols, groupsize, uppercase)

    return _compare_files(file_a, file_b)


def _compare_files(file_a: str, file_b: str) -> bool:
    with open(file_a, "r", encoding="utf-8") as fp1:
        with open(file_b, "r", encoding="utf-8") as fp2:
            for line1, line2 in zip(fp1, fp2):
                if line1 != line2:
                    logger.error("Mismatch between %r and %r", file_a, file_b)
                    logger.error("File A: %r", line1.strip())
                    logger.error("File B: %r", line2.strip())
                    return False
    os.remove(file_a)
    os.remove(file_b)
    return True


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n", "--min-cols", type=int, default=1, help="Minimum number of columns"
    )
    parser.add_argument(
        "-x", "--max-cols", type=int, default=256, help="Maximum number of columns"
    )
    test_hexdump(**vars(parser.parse_args()))


if __name__ == "__main__":
    main()
