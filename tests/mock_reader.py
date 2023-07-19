class MockReader:
    def __init__(self, lines):
        self.lines = lines

    def get_lines(self, _):
        for line in self.lines:
            yield line
