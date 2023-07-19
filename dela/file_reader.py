import os, glob
from dela.logger import log


class FileReader:
    @staticmethod
    def get_lines(g):
        files = [file for file in glob.glob(os.path.expanduser(g))]
        log.debug(f'Match files: {files}')

        for file_path in files:
            log.debug(f'Parsing file: {file_path}')

            with open(file_path, 'r') as f:
                lines = f.read().splitlines(True)
                for [lnum, line] in enumerate(lines):
                    yield [file_path, lnum, line]
