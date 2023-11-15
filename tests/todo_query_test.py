from unittest import TestCase
from dela.file_reader import Line
from dela.todo_query import TodoQuery
from tests.utils.create_lines import create_lines
from tests.mock_reader import MockReader

class TodoQueryTest(TestCase):
    def test_should_read_one_todo(self):
        lines = create_lines('todo.md', [
            '- [ ] 20230101 Todo 1 #t1 #t2',
        ])

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().exec()

        self.assertTrue(len(todos), 1)
        self.assertEqual(todos[0].title, 'Todo 1')
        self.assertEqual(todos[0].file, 'todo.md')
        self.assertEqual(todos[0].status, ' ')
        self.assertEqual(todos[0].tags, ['#t1', '#t2'])
        self.assertEqual(todos[0].date, '20230101')

    def test_should_read_multiple_todos(self):
        lines = create_lines(file='todo.md', lines=[
            '# Header',
            '- [ ] Todo 1',
            '- [ ] Todo 2',
        ])

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().exec()

        self.assertEqual([t.title for t in todos], ['Todo 1', 'Todo 2'])

    def test_should_filter_by_status(self):
        lines = create_lines('todo.md', [
            '# Header',
            '- [x] Done',
            '- [ ] Todo',
            '- [s] Someday',
        ])

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().status_in([' ', 's']).exec()

        self.assertEqual([t.title for t in todos], ['Todo', 'Someday'])

    def test_should_filter_by_tags(self):
        lines = create_lines('todo.md', [
            '# Header',
            '- [x] Done #tag',
            '- [ ] Todo',
            '- [s] Someday #tag',
        ])

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().tag_in(['#tag']).exec()

        self.assertEqual([t.title for t in todos], ['Done', 'Someday'])

    def test_should_filter_out_upcoming(self):
        lines = create_lines('todo.md', [
            '# Header',
            '- [x] 20210101 Past',
            '- [ ] 20230101 Today',
            '- [s] 20230102 Future',
            '- [ ] No date',
        ])

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().exclude_upcoming(today=20230101).exec()

        self.assertEqual(
            [t.title for t in todos], ['Past', 'Today', 'No date']
        )

    def test_should_filter_today(self):
        lines = create_lines('todo.md', [
            '# Header',
            '- [x] 20210101 Past',
            '- [ ] 20230101 Today',
            '- [s] 20230102 Future',
            '- [ ] No date',
        ])

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().today(today=20230101).exec()

        self.assertEqual([t.title for t in todos], ['Past', 'Today'])

    def test_should_sort_by_attr_date(self):
        lines = create_lines('todo.md', [
            '# Header',
            '- [x] 20210101 Past',
            '- [ ] 20230101 Today',
            '- [s] 20230102 Future',
            '- [ ] No date',
        ])

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().sort_by(['date'], reverse=True).exec()

        self.assertEqual(
            [t.title for t in todos], ['Future', 'Today', 'Past', 'No date']
        )

    def test_should_sort_by_multiple_attributes(self):
        lines = [
            Line(number=1, file='c.md', content='# Header', file_meta={}),
            Line(number=2, file='c.md', content='- [x] 20210101 Past', file_meta={}),
            Line(number=1, file='a.md', content='- [ ] 20230101 Today', file_meta={}),
            Line(number=2, file='a.md', content='- [s] 20230102 Someday', file_meta={}),
            Line(number=1, file='b.md', content='- [ ] No date', file_meta={}),
        ]

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().sort_by(['file', 'line'], reverse=False).exec()

        self.assertEqual(
            [[t.file, t.line] for t in todos],
            [
                ['a.md', 1], 
                ['a.md', 2], 
                ['b.md', 1], 
                ['c.md', 2], 
            ]
        )

    def test_sort_by_statuses(self):
        lines = create_lines('todo.md', [
            '# Header',
            '- [ ] Backlog',
            '- [n] Next',
            '- [s] Someday',
            '- [~] In progress',
        ])

        TodoQuery.reader = MockReader(lines)   # type: ignore
        query = TodoQuery('*.md').start()
        query = query.status_in(['~', 'n', ' ', 's'])
        query = query.sort_by_statuses(['~', 'n', ' ', 's'])
        todos = query.exec()

        self.assertEqual([t.title for t in todos], ['In progress', 'Next', 'Backlog', 'Someday'])

    def test_complex_query(self):
        lines = create_lines('todo.md', [
            '# Header',
            '- [x] 20210101 Past',
            '- [ ] 20230101 Match #tag1 #tag2',
            '- [s] 20230102 Future #tag1 #tag2',
            '- [ ] Match #tag2',
        ])

        TodoQuery.reader = MockReader(lines)   # type: ignore
        query = TodoQuery('*.md').start()
        query = query.tag_in(['#tag2', '#tag1'])
        query = query.exclude_upcoming(today=20230101)
        query = query.status_in([' ', 's'])
        todos = query.exec()

        self.assertEqual([t.title for t in todos], ['Match', 'Match'])
