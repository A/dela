from operator import attrgetter


class SortByStatus:
    def __init__(self, order):
        self.order = {key: i for i, key in enumerate(order)}

    def run(self, todos):
        return sorted(todos, key=lambda t: self.order[getattr(t, 'status')])

class SortByAttribute:
    def __init__(self, attr):
        self.attr = attr

    def run(self, todos):
        return sorted(todos, key=attrgetter(self.attr), reverse=True)
