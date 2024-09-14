import os
import subprocess
import hexdump
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

FILENAME = "hello.txt"
TEST_DIR = "test"


def test_hexdump():
    with open(FILENAME, "r", encoding="utf-8") as fp:
        data = fp.read()

    max_cols = 256
    logger.info("Testing hexdump with maximum of %i", max_cols)
    results = []
    for cols in range(1, max_cols + 1):
        for groupsize in range(1, cols + 1):
            _hexdump(data, cols, groupsize, False)
            results.append(_compare_files())
            _cleanup()
            _hexdump(data, cols, groupsize, True)
            results.append(_compare_files())
            _cleanup()
    if all(results):
        logger.info("All tests passed")


def _hexdump(data: str, cols: int, groupsize: bytes, uppercase: bool) -> str:
    output = hexdump.hexdump(data, cols, groupsize, uppercase)
    if not os.path.isdir(TEST_DIR):
        os.makedirs(TEST_DIR)
    with open(f"{TEST_DIR}/pyxd.txt", "w", encoding="utf-8") as fp:
        fp.write(output)

    args = ["xxd", "-c", str(cols), "-g", str(groupsize)]
    if uppercase:
        args.append("-u")
    args.append(FILENAME)

    with open(f"{TEST_DIR}/xxd.txt", "w", encoding="utf-8") as fp:
        subprocess.run(args, check=True, stdout=fp)


def _compare_files() -> bool:
    with open("test/pyxd.txt", "r", encoding="utf-8") as fp1:
        with open("test/xxd.txt", "r", encoding="utf-8") as fp2:
            for line1, line2 in zip(fp1, fp2):
                if line1 != line2:
                    return False
    return True


def _cleanup() -> None:
    if os.path.isdir(TEST_DIR):
        for file in os.listdir(TEST_DIR):
            os.remove(os.path.join(TEST_DIR, file))
        os.rmdir(TEST_DIR)


def main() -> None:
    test_hexdump()


if __name__ == "__main__":
    main()
