import sys
import codecs
from string import Template

# os.system("color")


class TodoPresentation:
    def __init__(self, format) -> None:
        self.template = Template(format)

    def present(self, todo):
        str = self.template.substitute(todo.__dict__)
        # NOTE: This 2 lines are here to add support for unicode escape
        #       characters like terminal colors, tabs, etc
        str = codecs.decode(str, 'raw-unicode-escape')
        str = str.encode('latin1').decode('utf8')
        print(str)
