import os
from pathlib import Path


def delete_dir_tree(directory: Path) -> None:
    """
    Recursively delete a whole directory and its content.
    Since there is no built-in function for this in the pathlib API and we want to keep it consistent, we have to use a self-written function.

    :param directory: The directory that should be removed
    """

    dir = directory

    for file in dir.iterdir():
        if file.is_dir():
            delete_dir_tree(file)
        else:
            file.unlink()
    dir.rmdir()


def pf(calling_class, file_path: str) -> str:
    """

    :param calling_class: the class of which this method is called
    :param file_path: path to file
    :return: joined path
    """
    return os.path.join(calling_class.path, file_path)
