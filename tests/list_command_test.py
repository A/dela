from unittest import TestCase
from importlib import reload
from dela.list_comand_config import ListCommandConfig
from dela.list_command import ListCommand
from dela.todo_query import TodoQuery
from tests.mock_reader import MockReader
from tests.utils.create_lines import create_lines


def createBlankConfig():
    return ListCommandConfig(
        {
            '<glob>': None,
            '--format': None,
            '--all': None,
            '--statuses': None,
            '--tags': None,
            '--today': None,
            '--upcoming': None,
            '--sort_by': None,
        }
    )


class ListCommandTest(TestCase):
    def test_todo_list_1(self):
        lines = create_lines('todo.md', [
            '- [ ] 20230101 Listed',
            '- [x] 20230101 Excluded',
            '- [~] 20230101 Listed',
            '- [n] 20230101 Listed',
            '- [x] 20230101 excluded',
        ])

        config = createBlankConfig()
        config.statuses = ['~', 'n', ' ']

        TodoQuery.reader = MockReader(lines)   # type: ignore
        result = ListCommand(config).run()
        self.assertEqual(
            [t.title for t in result], ['Listed', 'Listed', 'Listed']
        )

    def test_todo_list_2(self):
        lines = create_lines('todo.md', [
            '- [ ] Listed 2 #t',
            '- [x] Excluded',
            '- [~] Listed 1 #t', # 1st by status order
            '- [n] Listed',
            '- [x] excluded #t',
        ])

        config = createBlankConfig()
        config.statuses = ['~', 'n', ' ']
        config.tags = ['#t']

        TodoQuery.reader = MockReader(lines)   # type: ignore
        result = ListCommand(config).run()
        self.assertEqual(
            [t.title for t in result], ['Listed 1', 'Listed 2']
        )
