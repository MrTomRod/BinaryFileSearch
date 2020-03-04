import os
from unittest import TestCase
from binary_file_search.BinaryFileSearch import BinaryFileSearch


class TestBinaryFileSearch_IntMode(TestCase):
    def setUp(self) -> None:
        assert os.path.isfile("data/nodes.dmp")
        self.bs_nodes = BinaryFileSearch("data/nodes.dmp")
        self.bs_names = BinaryFileSearch("data/names.dmp")

    def tearDown(self) -> None:
        self.bs_nodes.close_file()
        self.bs_names.close_file()

    def test_nodes_first(self):
        self.assertEqual(0, self.bs_nodes._BinaryFileSearch__binary_search(query=1))
        self.assertEqual(0, self.bs_names._BinaryFileSearch__binary_search(query=1))

    def test_nodes_last(self):
        self.assertEqual(144253158, self.bs_nodes._BinaryFileSearch__binary_search(query=2590146))
        self.assertEqual(181458564, self.bs_names._BinaryFileSearch__binary_search(query=2590146))

    def test_nodes_regular(self):
        # no error should be thrown
        self.assertEqual(21624, self.bs_nodes._BinaryFileSearch__binary_search(query=453))
        self.assertEqual(7184, self.bs_nodes._BinaryFileSearch__binary_search(query=151))

    def test_nodes_nonexistent(self):
        with self.assertRaises(KeyError):
            self.bs_nodes._BinaryFileSearch__binary_search(query=4)
            self.bs_names._BinaryFileSearch__binary_search(query=4)

    def test_single_lines(self):
        self.assertEqual(1, len(self.bs_nodes.extract_lines_beginning_with(536110)))
        self.assertEqual(1, len(self.bs_names.extract_lines_beginning_with(536110)))

    def test_multiple_lines(self):
        self.assertLess(1, len(self.bs_names.extract_lines_beginning_with(2)))


class TestBinaryFileSearch_StrMode(TestCase):
    def setUp(self) -> None:
        self.bs_text = BinaryFileSearch("data/text_test.sorted", string_mode=True)

    def tearDown(self) -> None:
        self.bs_text.close_file()

    def test_nodes_first(self):
        self.assertEqual(0, self.bs_text._BinaryFileSearch__binary_search(query='A0A023GPI8'))

    def test_nodes_last(self):
        self.assertEqual(8176, self.bs_text._BinaryFileSearch__binary_search(query='A0A067XMP2'))

    def test_nodes_regular(self):
        # no error should be thrown
        self.assertEqual(7181, self.bs_text._BinaryFileSearch__binary_search(query='A0A059U906'))

    def test_nodes_nonexistent(self):
        with self.assertRaises(KeyError):
            self.bs_text._BinaryFileSearch__binary_search(query="ain't got nothin' like dat")

    def test_single_lines(self):
        self.assertEqual(1, len(self.bs_text.extract_lines_beginning_with('A0A023IWG3')))

    def test_multiple_lines(self):
        self.assertLess(1, len(self.bs_text.extract_lines_beginning_with('A0A023GS28')))


class TestBinaryFileSearch_Reopen(TestCase):
    def setUp(self) -> None:
        self.bs_reopen = BinaryFileSearch("data/text_test.sorted", string_mode=True)

    def tearDown(self) -> None:
        self.bs_reopen.close_file()

    def test_reopen_same(self):
        self.assertEqual(7181, self.bs_reopen._BinaryFileSearch__binary_search(query='A0A059U906'))

        self.bs_reopen.close_file()

        self.bs_reopen.open_file()

        self.assertEqual(7181, self.bs_reopen._BinaryFileSearch__binary_search(query='A0A059U906'))

    def test_reopen_different(self):
        self.assertEqual(7181, self.bs_reopen._BinaryFileSearch__binary_search(query='A0A059U906'))

        self.bs_reopen.close_file()

        self.bs_reopen.open_file("data/nodes.dmp", string_mode=False)

        self.assertEqual(21624, self.bs_reopen._BinaryFileSearch__binary_search(query=453))
