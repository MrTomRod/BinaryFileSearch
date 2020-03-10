from unittest import TestCase
from binary_file_search.BinaryFileSearch import BinaryFileSearch


class TestBinaryFileSearch_StrMode(TestCase):
    def setUp(self) -> None:
        self.bfs: BinaryFileSearch
        self.bfs = BinaryFileSearch("data/text_test.sorted", string_mode=True).__enter__()
        assert self.bfs.is_file_sorted()

    def tearDown(self) -> None:
        self.bfs.__exit__(None, None, None)

    def test_wrong_query_type(self):
        with self.assertRaises(TypeError):
            self.bfs.search(query=1)

    def test_nonexistent(self):
        with self.assertRaises(KeyError):
            self.bfs.search(query="ain't got nothin' like dat")

    def test_bad_file(self):
        with self.assertRaises(FileNotFoundError):
            with BinaryFileSearch('very!bad!path') as bfs:
                pass

    def test_first(self):
        with open('data/text_test.sorted')as f:
            print(repr(f.read()))
        self.assertEqual([['aa', 'first']], self.bfs.search(query='aa'))

    def test_last(self):
        self.assertEqual([['zz', 'last']], self.bfs.search(query='zz'))

    def test_regular(self):
        # no error should be thrown
        self.assertEqual([['aaa', 'third']], self.bfs.search(query='aaa'))

    def test_single_lines(self):
        self.assertEqual(1, len(self.bfs.search('aaa')))

    def test_multiple_lines(self):
        self.assertEquals(2, len(self.bfs.search('bA')))

    def test_multiple_searches(self):
        self.assertEqual([['bA', 'fourth_1'], ['bA', 'fourth_2']], self.bfs.search(query='bA'))
        self.assertEqual([['aaA', 'second']], self.bfs.search(query='aaA'))


class TestBinaryFileSearch_IntMode(TestCase):
    def setUp(self) -> None:
        self.bfs: BinaryFileSearch
        self.bfs = BinaryFileSearch("data/int_test.sorted", sep=',', string_mode=False).__enter__()
        assert self.bfs.is_file_sorted()

    def tearDown(self) -> None:
        self.bfs.__exit__(None, None, None)

    def test_wrong_query_type(self):
        with self.assertRaises(TypeError):
            self.bfs.search(query='1')

    def test_nonexistent(self):
        with self.assertRaises(KeyError):
            self.bfs._BinaryFileSearch__binary_search(query=0)

    def test_first(self):
        self.assertEqual([[1, 'one']], self.bfs.search(query=1))

    def test_last(self):
        self.assertEqual([[1000000, 'million']], self.bfs.search(query=1000000))

    def test_regular(self):
        # no error should be thrown
        self.assertEqual([[4, 'four']], self.bfs.search(query=4))
        self.assertEqual([[3, 'three']], self.bfs.search(query=3))

    def test_single_lines(self):
        self.assertEqual(1, len(self.bfs.search(4)))

    def test_multiple_lines(self):
        self.assertLess(1, len(self.bfs.search(40)))
