import os


def file_exists(filename: str) -> bool:
    return os.path.isfile(filename)
