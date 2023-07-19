from unittest import TestCase
from dela.list_comand_config import ListCommandConfig
from dela.list_command import ListCommand
from dela.todo_query import TodoQuery
from tests.mock_reader import MockReader


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
        lines = [
            ['todo.md', 1, '- [ ] 20230101 Listed'],
            ['todo.md', 1, '- [x] 20230101 Excluded'],
            ['todo.md', 1, '- [~] 20230101 Listed'],
            ['todo.md', 1, '- [n] 20230101 Listed'],
            ['todo.md', 1, '- [x] 20230101 excluded'],
        ]

        config = createBlankConfig()
        config.statuses = ['~', 'n', ' ']

        TodoQuery.reader = MockReader(lines)   # type: ignore
        result = ListCommand(config).run()
        self.assertEqual(
            [t.title for t in result], ['Listed', 'Listed', 'Listed']
        )

    def test_todo_list_2(self):
        lines = [
            ['todo.md', 1, '- [ ] Listed 2 #t'],
            ['todo.md', 2, '- [x] Excluded'],
            ['todo.md', 3, '- [~] Listed 1 #t'], # 1st by status order
            ['todo.md', 4, '- [n] Listed'],
            ['todo.md', 5, '- [x] excluded #t'],
        ]

        config = createBlankConfig()
        config.statuses = ['~', 'n', ' ']
        config.tags = ['#t']

        TodoQuery.reader = MockReader(lines)   # type: ignore
        result = ListCommand(config).run()
        self.assertEqual(
            [t.title for t in result], ['Listed 1', 'Listed 2']
        )
