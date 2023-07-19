import re

TODO_RE = '^\s*-\s+\[(?P<status>.{1})\]\s+(?:(?P<date>\d{8})\s+)?(?P<title>.*?)(?:\s+(?P<tagline>#.*))?$'


class Todo(object):
    title = None
    date = None
    file = None
    tags = []
    status = None
    line = None

    def __init__(self, title, status, tags, file, date, line):
        self.title = title
        self.date = date
        self.status = status
        self.tags = tags
        self.file = file
        self.line = line

    @staticmethod
    def from_line(line, file, lnum):
        match = match = re.search(TODO_RE, line)

        if not match:
            return None

        gd = match.groupdict()

        return Todo(
            title=gd['title'],
            status=gd['status'].lower(),
            date=gd['date'] if 'date' in gd and gd['date'] else '',
            tags=gd['tagline'].split(' ')
            if 'tagline' in gd and gd['tagline'] is not None
            else [],
            file=file,
            line=lnum,
        )

    def __repr__(self):
        return f'title: {self.title}\ndate: {self.date}\ntags: {",".join(self.tags)}\nstatus: {self.status}\nfile: {self.file}\nline: {self.line}'
