from dela.FileReader import FileReader
from dela.Todo import Todo
from dela.logger import log

class TodoRepoContext:
    _all = []
    _result = []


class TodoRepo:
    def __init__(self, glob):
        self.glob = glob
        self.context = TodoRepoContext()
        self.context._all = self._read_fs()

    def _read_fs(self):
        files = FileReader.get_files(self.glob)
        log.debug(f'Match files: {files}')

        result = []
        for file_path in files:
            log.debug(f'Parsing file: {file_path}')

            local = []

            for line in FileReader.read_file(file_path):
                todo = Todo.from_line(line, file_path)
                if todo:
                    local.append(todo)

            if len(local):
                log.info(f'Parsed file: {file_path}')
                log.info(f'Found {len(local)} todo(s)')
                log.info(f'Todos: {local}')
                
            result += local

        return result

    def all(self):
        self.context._result = self.context._all
        return self
    
    def filter(self, filter_fn):
        self.context._result = [t for t in self.context._result if filter_fn(t)]
        return self

    def sort(self, comparator):
        self.context._result = comparator(self.context._result)
        return self

    def exec(self):
        result = self.context._result
        self.context._result = []
        return result
