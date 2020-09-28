import re
import sqlite3
from attu import app


def parse_reference(text):
    book_e = re.compile(ur'(?P<book>.*[^\W\d_])\s(?P<reference>\d.*)', re.U)

    match = book_e.search(text)
    if not match:
        raise ValueError('Not matched')

    result = []

    book, reference = match.groups()

    for p in reference.split(';'):
        chapter, _, verses = p.partition(':')
        chapter = int(chapter)

        for range_ in verses.split(','):
            first, _, last = range_.partition('-')
            first = int(first)

            if not last:
                result.append((book, chapter, first))
            else:
                last = int(last)
                for i in xrange(first, last + 1):
                    result.append((book, chapter, i))

    return result


class Reader(object):
    def __init__(self, path=None):
        if path is None:
            path = app.config['DB_PATH']
        self.c = sqlite3.connect(path)

    def close(self):
        self.c.close()
        del(self.c)

    def read_verse(self, book, chapter, verse):
        query_args = (book, book, book, int(chapter), int(verse))
        for row in self.c.execute(SQL_FIND_VERSE, query_args):
            return row[0]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

SQL_FIND_VERSE = """
SELECT verse_scripture
FROM lds_scriptures_books b
INNER JOIN lds_scriptures_verses v ON b.book_id == v.book_id
WHERE (b.book_title = ? or b.book_title_long = ? or b.book_title_short = ?) and
      v.chapter = ? and
      v.verse = ?
"""
