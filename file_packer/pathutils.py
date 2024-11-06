from pathlib import PurePath
import fnmatch
import os
from .reader import FilePackReader

class FilePackPath:
    """
    A pathlib-like interface for FilePackReader, allowing more convenient and intuitive handling of paths.
    """
    def __init__(self, pack_reader, path=""):
        self.pack_reader = pack_reader
        if not isinstance(pack_reader, FilePackReader):
            raise TypeError("pack_reader must be an instance of FilePackReader")
        base_path = self.pack_reader.base_path if hasattr(self.pack_reader, 'base_path') else ''
        self._path = PurePath(base_path)

    def exists(self):
        """Check if the path exists in the file pack."""
        return self.pack_reader.exists(str(self._path))

    def is_file(self):
        """Check if the path is a file in the file pack."""
        return self.pack_reader.isfile(str(self._path))

    def is_dir(self):
        """Check if the path is a directory in the file pack."""
        return self.pack_reader.isdir(str(self._path))

    def iterdir(self):
        """Iterate over the directory's contents."""
        if not self.is_dir():
            raise NotADirectoryError(f"{self._path} is not a directory")

        for entry in self.pack_reader.listdir(str(self._path)):
            yield FilePackPath(self.pack_reader, self._path / entry)

    def open(self, mode="r"):
        """Open a file in the file pack."""
        return self.pack_reader.open(str(self._path), mode)

    def read_bytes(self):
        """Read file bytes from the file pack."""
        return self.pack_reader.read_bytes(str(self._path), exclude_base_path=False)

    def read_text(self, encoding="utf-8"):
        """Read text from the file pack."""
        with self.open("r") as file:
            return file.read()

    def glob(self, pattern):
        """Return all paths matching the given pattern."""
        if not self.is_dir():
            raise NotADirectoryError(f"{self._path} is not a directory")

        for root, dirs, files in self.pack_reader.walk():
            for name in files:
                full_path = os.path.join(root, name)
                if fnmatch.fnmatch(full_path, os.path.join(str(self._path), pattern)):
                    yield FilePackPath(self.pack_reader, full_path)

    def __truediv__(self, key):
        """Override the '/' operator for path joining."""
        return FilePackPath(self.pack_reader, self._path / key)

    def __str__(self):
        return str(self._path)

    def __repr__(self):
        return f"<FilePackPath({self._path})>"
