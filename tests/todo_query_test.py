from unittest import TestCase
from dela.todo_query import TodoQuery
from tests.mock_reader import MockReader


class TodoQueryTest(TestCase):
    def test_should_read_one_todo(self):
        lines = [
            ['todo.md', 1, '- [ ] 20230101 Todo 1 #t1 #t2'],
        ]

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().exec()

        self.assertTrue(len(todos), 1)
        self.assertEqual(todos[0].title, 'Todo 1')
        self.assertEqual(todos[0].file, 'todo.md')
        self.assertEqual(todos[0].status, ' ')
        self.assertEqual(todos[0].tags, ['#t1', '#t2'])
        self.assertEqual(todos[0].date, '20230101')

    def test_should_read_multile_todos(self):
        lines = [
            ['todo.md', 1, '# Header'],
            ['todo.md', 2, '- [ ] Todo 1'],
            ['todo.md', 3, '- [ ] Todo 2'],
        ]

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().exec()

        self.assertEqual([t.title for t in todos], ['Todo 1', 'Todo 2'])

    def test_should_filter_by_status(self):
        lines = [
            ['todo.md', 1, '# Header'],
            ['todo.md', 2, '- [x] Done'],
            ['todo.md', 3, '- [ ] Todo'],
            ['todo.md', 4, '- [s] Someday'],
        ]

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().status_in([' ', 's']).exec()

        self.assertEqual([t.title for t in todos], ['Todo', 'Someday'])

    def test_should_filter_by_tags(self):
        lines = [
            ['todo.md', 1, '# Header'],
            ['todo.md', 2, '- [x] Done #tag'],
            ['todo.md', 3, '- [ ] Todo'],
            ['todo.md', 4, '- [s] Someday #tag'],
        ]

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().tag_in(['#tag']).exec()

        self.assertEqual([t.title for t in todos], ['Done', 'Someday'])

    def test_should_filter_out_upcoming(self):
        lines = [
            ['todo.md', 1, '# Header'],
            ['todo.md', 2, '- [x] 20210101 Past'],
            ['todo.md', 3, '- [ ] 20230101 Today'],
            ['todo.md', 4, '- [s] 20230102 Future'],
            ['todo.md', 5, '- [ ] No date'],
        ]

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().exclude_upcoming(today=20230101).exec()

        self.assertEqual(
            [t.title for t in todos], ['Past', 'Today', 'No date']
        )

    def test_should_filter_today(self):
        lines = [
            ['todo.md', 1, '# Header'],
            ['todo.md', 2, '- [x] 20210101 Past'],
            ['todo.md', 3, '- [ ] 20230101 Today'],
            ['todo.md', 4, '- [s] 20230102 Future'],
            ['todo.md', 5, '- [ ] No date'],
        ]

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().today(today=20230101).exec()

        self.assertEqual([t.title for t in todos], ['Past', 'Today'])

    def test_should_sort_by_attr_date(self):
        lines = [
            ['todo.md', 1, '# Header'],
            ['todo.md', 2, '- [x] 20210101 Past'],
            ['todo.md', 3, '- [ ] 20230101 Today'],
            ['todo.md', 4, '- [s] 20230102 Future'],
            ['todo.md', 5, '- [ ] No date'],
        ]

        TodoQuery.reader = MockReader(lines)   # type: ignore
        todos = TodoQuery('*.md').start().sort_by(['date'], reverse=True).exec()

        self.assertEqual(
            [t.title for t in todos], ['Future', 'Today', 'Past', 'No date']
        )

    def test_should_sort_by_multiple_attributes(self):
        lines = [
            ['c.md', 1, '# Header'],
            ['c.md', 2, '- [x] 20210101 Past'],
            ['a.md', 1, '- [ ] 20230101 Today'],
            ['a.md', 2, '- [s] 20230102 Future'],
            ['b.md', 1, '- [ ] No date'],
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
        lines = [
            ['todo.md', 1, '# Header'],
            ['todo.md', 2, '- [ ] Backlog'],
            ['todo.md', 3, '- [n] Next'],
            ['todo.md', 4, '- [s] Someday'],
            ['todo.md', 5, '- [~] In progress'],
        ]

        TodoQuery.reader = MockReader(lines)   # type: ignore
        query = TodoQuery('*.md').start()
        query = query.status_in(['~', 'n', ' ', 's'])
        query = query.sort_by_statuses(['~', 'n', ' ', 's'])
        todos = query.exec()

        self.assertEqual([t.title for t in todos], ['In progress', 'Next', 'Backlog', 'Someday'])

    def test_complext_query(self):
        lines = [
            ['todo.md', 1, '# Header'],
            ['todo.md', 2, '- [x] 20210101 Past'],
            ['todo.md', 3, '- [ ] 20230101 Match #tag1 #tag2'],
            ['todo.md', 4, '- [s] 20230102 Future #tag1 #tag2'],
            ['todo.md', 5, '- [ ] Match #tag2'],
        ]

        TodoQuery.reader = MockReader(lines)   # type: ignore
        query = TodoQuery('*.md').start()
        query = query.tag_in(['#tag2', '#tag1'])
        query = query.exclude_upcoming(today=20230101)
        query = query.status_in([' ', 's'])
        todos = query.exec()

        self.assertEqual([t.title for t in todos], ['Match', 'Match'])
