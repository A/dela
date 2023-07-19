import codecs
from string import Template


class TodoPresentation:
    def __init__(self, format) -> None:
        self.template = Template(format)

    def present(self, todos):
        for todo in todos:
            self.present_one(todo)

    def present_one(self, todo):
        context = todo.__dict__
        context['tags'] = ' '.join(context['tags'])

        str = self.template.substitute(context)

        # NOTE: This 2 lines are here to add support for unicode escape
        #       characters like terminal colors, tabs, etc
        str = codecs.decode(str, 'raw-unicode-escape')
        str = str.encode('latin1').decode('utf8')

        print(str)
