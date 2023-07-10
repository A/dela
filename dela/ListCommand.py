import operator
from datetime import datetime
from dela.TodoPresentation import TodoPresentation
from dela.logger import log
from dela.FileReader import FileReader
from dela.Todo import Todo


class ListCommandConfig(object):
    def __init__(self, args):
        self.glob = args['<glob>'] if args['<glob>'] else '*.md'
        self.format = (
            args['--format']
            if args['--format']
            else '\u001b[30m- \u001b[0m\u001b[01m[$status]\u001b[0m \u001b[31m$file:\u001b[0m $title \u001b[0m\u001b[34m$tags\u001b[0m'
        )
        self.filter_by_status = args['--status'] if args['--status'] else None
        self.show_all = True if args['--all'] else False
        self.sort_by = args['--sort_by'] if args['--sort_by'] else None
        self.only_today = True if args['--today'] else False
        self.only_done = True if args['--done'] else False
        self.only_someday = True if args['--someday'] else False
        self.filter_by_tags = args['--tag'] if args['--tag'] else None

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)


class ListCommand:
    def __init__(self, args) -> None:
        self.config = ListCommandConfig(args)

    def run(self):
        log.info(f'Execute list command with config: {self.config}')

        files = FileReader.get_files(self.config.glob)
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

        result = self.filter(result)
        result = self.sort(result)

        presentation = TodoPresentation(self.config.format)
        for i in result:
            presentation.present(i)

    def filter(self, todos):
        result = todos

        if not self.config.show_all and not self.config.only_done and not self.config.only_someday:
            result = [
                i
                for i in result
                if i.status
                not in [
                    *Todo.STATUSES_DONE,
                    *Todo.STATUSES_ARCHIVED,
                    *Todo.STATUSES_CLOSED,
                    *Todo.STATUSES_SOMEDAY,
                ]
            ]

        if self.config.only_someday:
            result = [i for i in result if i.status in Todo.STATUSES_SOMEDAY]

        if self.config.only_done:
            result = [i for i in result if i.status not in Todo.STATUSES_DONE]

        if self.config.filter_by_status is not None:
            result = [
                i for i in result if i.status == self.config.filter_by_status
            ]

        if self.config.filter_by_tags:
            result = [
                i for i in result if bool(set(i.tags) & set(self.config.filter_by_tags))
            ]

        if self.config.only_today:
            YYYYmmDD = datetime.now().strftime('%Y%m%d')
            result = [i for i in result if i.date == YYYYmmDD]

        return result

    def sort(self, todos):
        result = todos

        if self.config.sort_by:
            result = sorted(
                todos,
                reverse=True,
                key=lambda x: getattr(x, self.config.sort_by) # type: ignore
            )

        return result
