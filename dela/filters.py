from datetime import datetime

class TodayFilter():
    today = int(datetime.now().strftime('%Y%m%d'))

    def run(self, todo):
        return bool(todo.date) and int(todo.date) <= self.today


class StatusFilter():
    def __init__(self, statuses):
        self.statuses = statuses
    def run(self, todo):
        return not self.statuses or todo.status in self.statuses

class TagFilter():
    def __init__(self, tags):
        self.tags = tags

    def run(self, todo):
        # intersection
        return not self.tags or bool([t for t in todo.tags if t in self.tags])


class ExcludeUpcomingFilter():
    today = int(datetime.now().strftime('%Y%m%d'))

    def run(self, todo):
        return not bool(todo.date) or int(todo.date) <= self.today
