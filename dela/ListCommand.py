from dela.TodoPresentation import TodoPresentation
from dela.TodoRepo import TodoRepo
from dela.comparators import SortByAttribute, SortByStatus
from dela.filters import ExcludeUpcomingFilter, StatusFilter, TagFilter, TodayFilter
from dela.logger import log


class ListCommandConfig(object):
    def __init__(self, args):
        self.glob = args['<glob>'] if args['<glob>'] else '*.md'
        self.format = (
            args['--format']
            if args['--format']
            else '\u001b[30m- \u001b[0m\u001b[01m[$status]\u001b[0m \u001b[31m$file:\u001b[0m $title \u001b[0m\u001b[34m$tags\u001b[0m \u001b[31m$date\u001b[0m'
        )
        self.all = True if args['--all'] else False
        self.statuses = args['--statuses'].replace('=', '').split(',') if args['--statuses'] else []
        self.tags = args['--tags'].replace('=', '').split(',') if args['--tags'] else []
        self.today = True if args['--today'] else False
        self.upcoming = True if args['--upcoming'] else False
        self.sort_by = args['--sort_by'] if args['--sort_by'] else None

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)


class ListCommand:
    def __init__(self, args) -> None:
        self.args = args;
        self.config = ListCommandConfig(args)

    def run(self):
        log.info(f'Execute list command with config: {self.config}')

        query = TodoRepo(self.config.glob).all()

        if not self.config.all:
            query.filter(StatusFilter(self.config.statuses).run)

        query.filter(TagFilter(self.config.tags).run)

        if self.config.today:
            query.filter(TodayFilter().run)

        if not self.config.upcoming and not self.config.all:
            query.filter(ExcludeUpcomingFilter().run)

        if not self.config.all:
            query.sort(SortByStatus(self.config.statuses).run)
            query.sort(SortByAttribute("date").run)


        if self.config.sort_by:
            query.sort(SortByAttribute(self.config.sort_by).run)

        result = query.exec()

        presentation = TodoPresentation(self.config.format)
        presentation.present(result)
