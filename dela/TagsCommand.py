from dela.TagPresentation import TagPresentation
from dela.logger import log
from datetime import datetime
from dela.Todo import Todo
from dela.FileReader import FileReader


class TagsCommandConfig(object):
    def __init__(self, args):
        self.glob = args['<glob>'] if args['<glob>'] else '*.md'
        self.show_all = True if args['--all'] else False

class TagsCommand:
    def __init__(self, args):
        self.config = TagsCommandConfig(args)
        pass

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

        presentation = TagPresentation()
        presentation.present(result)

        
    def filter(self, todos):
        result = todos

        YYYYmmDD = int(datetime.now().strftime('%Y%m%d'))

        if (
            not self.config.show_all
        ):
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
                and (not bool(i.date) or int(i.date) <= YYYYmmDD)
            ]

        return result

