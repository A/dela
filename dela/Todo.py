import re

TODO_RE = '^\s*-\s+\[(?P<status>.{1})\]\s+(?:(?P<date>\d{8})\s+)?(?P<title>.*?)(?:\s+(?P<tagline>#.*))?$'


class Todo(object):
    STATUSES_DONE = ['x', 'X']
    STATUSES_ARCHIVED = ['a', 'A']
    STATUSES_CLOSED = ['c', 'C', '-']
    STATUSES_IN_PROGRESS = ['~']

    title = None
    date = None
    file = None
    tags = []
    status = None

    def __init__(self, title, status, tags, file, date):
        self.title = title
        self.date = date
        self.status = status
        self.tags = tags
        self.file = file

    @staticmethod
    def from_line(line, file):
        """
        format: - [ ] [YYYYmmDD] Todo #tag #tag
        """
        match = match = re.search(TODO_RE, line)

        if not match:
            return None

        gd = match.groupdict()

        return Todo(
            title=gd['title'],
            status=gd['status'],
            date=gd['date'] if 'date' in gd else None,
            tags=gd['tagline'].split(' ')
            if 'tagline' in gd and gd['tagline'] is not None
            else [],
            file=file,
        )

    def __repr__(self):
        return f'title: {self.title}\ndate: {self.date}\ntags: {",".join(self.tags)}\nstatus: {self.status}\nfile: {self.file}'
