from dela.file_reader import Line

def create_lines(file, lines):
    _lines = []
    for i, content in enumerate(lines):
        line = Line(number=i, file=file, content=content, file_meta={})
        _lines.append(line)
    return _lines

