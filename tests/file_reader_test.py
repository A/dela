from unittest import TestCase

from dela.file_reader import FileReader


class FileReaderTest(TestCase):
    def test_parsing(self):
        offset = 8 # frontmatter offset, to check if it points to proper line number
        file = 'tests/__stubs__/metadata_today.md'
        lines = FileReader.get_lines(file)
        lines = list(lines)

        for i, line in enumerate(lines):
            self.assertEqual(line.file, file)
            self.assertEqual(line.number, i + offset)
            self.assertEqual(line.file_meta, {
                'date': 'today',
                'tags': ['workout']
            })

        self.assertEqual(len(lines), 4)
