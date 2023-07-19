class MockPresentation:
    result = []

    def __init__(self, _):
        pass

    def present(self, result):
        self.result = result
