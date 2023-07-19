from datetime import datetime
from operator import attrgetter
from dela.file_reader import FileReader
from dela.todo import Todo
from dela.logger import log


class TodoQueryContext:
    _all = []
    _result = []


class TodoQuery:
    reader = FileReader

    def __init__(self, glob):
        self.glob = glob
        self.context = TodoQueryContext()
        self.context._all = self._read_fs()

    def _read_fs(self):
        result = []
        for [path, lnum, line] in self.reader.get_lines(self.glob):
            todo = Todo.from_line(line, path, lnum)
            if todo:
                result.append(todo)

        return result

    def start(self):
        self.context._result = self.context._all
        return self

    def filter(self, filter_fn):
        """
        Generic filter against current result
        """
        self.context._result = [
            t for t in self.context._result if filter_fn(t)
        ]
        return self

    def status_in(self, statuses):
        """
        Filter out all todos with a status not in `statuses`
        """
        self.filter(lambda todo: todo.status in statuses)
        return self

    def tag_in(self, tags):
        """
        Filter out all todos haven't tags intersect with given `tags`
        """
        self.filter(lambda todo: bool([t for t in todo.tags if t in tags]))
        return self

    def exclude_upcoming(self, today=int(datetime.now().strftime('%Y%m%d'))):
        """
        Filter out all upcoming todos
        """
        self.filter(
            lambda todo: not bool(todo.date) or int(todo.date) <= today
        )
        return self

    def today(self, today=int(datetime.now().strftime('%Y%m%d'))):
        """
        Filter out all todos except today ones
        """
        self.filter(lambda todo: bool(todo.date) and int(todo.date) <= today)
        return self

    def sort(self, comparator):
        self.context._result = comparator(self.context._result)
        return self

    def sort_by(self, attr, reverse=False):
        self.context._result = sorted(
            self.context._result,
            key=attrgetter(*attr if list == type(attr) else attr),
            reverse=reverse,
        )
        return self

    def sort_by_statuses(self, statuses_order, reverse=False):
        order = {key: i for i, key in enumerate(statuses_order, start=1)}
        self.context._result = sorted(
            self.context._result,
            key=lambda t: order[getattr(t, 'status')],
            reverse=reverse,
        )
        return self

    def exec(self):
        result = self.context._result
        self.context._result = []
        return result
