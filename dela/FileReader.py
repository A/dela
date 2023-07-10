import os, glob


class FileReader:
    @staticmethod
    def get_files(g):
        return [file for file in glob.glob(os.path.expanduser(g))]

    @staticmethod
    def read_file(path):
        with open(path, 'r') as f:
            return f.read().splitlines(True)
