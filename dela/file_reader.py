import os, glob
from dataclasses import dataclass
import frontmatter
from dela.logger import log

@dataclass
class Line:
    file: str
    file_meta: dict
    number: int
    content: str


def get_offset_len(original_content, cropped_content):
    original_len = len(original_content.split('\n'))
    cropped_len = len(cropped_content.split('\n'))
    return original_len - cropped_len


class FileReader:
    @staticmethod
    def get_lines(g):
        files = [file for file in glob.glob(os.path.expanduser(g))]
        log.debug(f'Match files: {files}')

        for file_path in files:
            log.debug(f'Parsing file: {file_path}')

            with open(file_path, 'r') as f:
                try:
                    f_content = f.read()
                    fm = frontmatter.loads(f_content)
                    offset_len = get_offset_len(f_content, fm.content)
                    lines = fm.content.split('\n')

                    for [lnum, line] in enumerate(lines):
                        yield Line(
                            file=file_path,
                            file_meta=fm.metadata.get('dela', {}),
                            number=lnum + offset_len,
                            content=line,
                        )
                except Exception:
                    log.info(f'Broken file: {file_path}')
