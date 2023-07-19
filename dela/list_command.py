from dela.todo_query import TodoQuery
from dela.logger import log


class ListCommand:
    def __init__(self, config) -> None:
        self.config = config

    def run(self):
        log.info(f'Execute list command with config: {self.config}')

        query = TodoQuery(self.config.glob).start()

        if not self.config.all:
            query.status_in(self.config.statuses)

        if self.config.tags:
            query.tag_in(self.config.tags)

        if self.config.today:
            query.today()

        if not self.config.upcoming and not self.config.all:
            query.exclude_upcoming()

        if not self.config.all:
            query.sort_by_statuses(self.config.statuses)
            query.sort_by(['date'])

        if self.config.sort_by:
            query.sort_by(self.config.sort_by)

        return query.exec()

