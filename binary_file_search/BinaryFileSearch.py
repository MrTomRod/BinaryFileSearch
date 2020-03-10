class BinaryFileSearch:
    """
    Binary search algorithm for big sorted files that cannot be read into RAM.

    Requirements:
    -------------
        - file must be sorted by the first column
            integer-sorting in bash: `sort -n --key=1 --field-separator=$'\t' --output=file.txt.sorted file.txt`
            string-sorting in bash: `LC_ALL=C sort --key=1 --field-separator=$'\t' --output=file.txt.sorted file.txt`
        - every line must begin with the sorted string/integer, followed by a separator
        - there may be multiple lines beginning with the same string/integer
            the script will return a list of lines that start with the same string/integer

    Example Usage:
    --------------
    with BinaryFileSearch("test/data/nodes.dmp") as bsf:
        lines = bfs.search(query)  # get lines that begin with :param query:
        # lines is now list of lines, the lines being split by sep:, e.g. [ [[query][l1], ...], [[query][l2]], ... ]

    Credit:
    -------
    Inspired by https://www.geeksforgeeks.org/python-program-for-binary-search/

    :param file: the sorted file to be searched
    :param sep: separator (default: "\t")
    :param string_mode: True if the sorted column consists of strings, False if integers
    """

    def __init__(self, file: str, sep: str = "\t", string_mode: bool = False):
        self.file_path = file
        self.sep = sep
        self.string_mode = string_mode

    def __enter__(self):
        self.f = open(self.file_path, 'r')
        self.f.seek(0, 2)  # 0 = offset, 2 = relative to file end => go to last char in file!
        self.length = self.f.tell()
        return self

    def __exit__(self, type, value, traceback):
        self.f.close()

    def search(self, query) -> list:
        """
        Search for query in sorted file. Returns list of all lines that begin with query.

        :param query: string/integer to search
        :returns: list of lines, the lines being separated by sep:, e.g. [ [[query][l1]], [[query][l2]], ... ]
        :raises KeyError: if the query isn't found
        :raises TypeError: if the type of the query does not match string_mode
        """

        if self.string_mode:
            if type(query) != str: raise TypeError(
                F"string_mode is on, query must be str! query: {query}, type: {type(query)}")
        else:
            if type(query) != int: raise TypeError(
                F"string_mode is off, query must be int! query: {query}, type: {type(query)}")

        # find the offset where the matching lines begin
        offset = self.__binary_search(query=query)

        # move to offset
        self.f.seek(offset)

        # return matching lines as list
        lines_that_start_with_query = []
        line = self.f.readline().strip().split(self.sep)
        if not self.string_mode: line[0] = int(line[0])
        while line[0] == query:
            lines_that_start_with_query.append(line)

            line = self.f.readline().strip().split(self.sep)
            if line == ['']:  # happens only at the last line.
                break
            if not self.string_mode: line[0] = int(line[0])

        assert len(lines_that_start_with_query) > 0
        return lines_that_start_with_query

    def __binary_search(self, query):
        """
        use this as entry-point

        :returns: offset in file where the first line that matches :param query: begins
        """

        return self.__recursive_binary_search(query=query, l=0, h=self.length)

    def __recursive_binary_search(self, query, l: int, h: int) -> int:
        """
        :param l: low  offset of the file to be searched (first iteration: 0)
        :param h: high offset of the file to be searched (first iteration: self.length)

        :returns: offset in file where the first line that matches :param query: begins
        """

        if h >= l:
            mid = l + (h - l) // 2

            line_start = mid

            # move seeker to previous newline
            while line_start >= 0:
                self.f.seek(line_start)
                if self.f.read(1) == '\n':
                    break
                line_start -= 1
            if line_start < 0:
                line_start = 0
                self.f.seek(line_start)

            # get current_id
            current_id = self.f.readline().split(self.sep, 1)[0]
            if not self.string_mode: current_id = int(current_id)

            # binary search algorithm main logic
            if query == current_id:
                # success!
                return self.__walk_back_to_first_line(query=query, current_position=line_start)

            elif query < current_id:
                return self.__recursive_binary_search(query=query, l=l, h=mid - 1)

            else:
                return self.__recursive_binary_search(query=query, l=mid + 1, h=h)

        raise KeyError("query not found: " + str(query))

    def __walk_back_to_first_line(self, query: int, current_position: int) -> int:
        """walk backwards in the file to find the first line that begins with :param query:"""
        while current_position > 0:
            self.f.seek(current_position)

            if self.f.read(1) == "\n":
                line = self.f.readline()
                id = line.split(self.sep, 1)[0]  # moves cursor forward to next line!
                if not self.string_mode: id = int(id)
                if id != query:
                    final_line = self.f.tell()  # curser should now be at start of first line
                    if self.string_mode:
                        assert self.f.readline().split(self.sep, 1)[0] == query  # next line must have proper id
                    else:
                        assert int(self.f.readline().split(self.sep, 1)[0]) == query  # next line must have proper id
                    return final_line

            current_position -= 1  # walk back

        # code should only end up here if first or second element in file was found
        assert self.f.seek(current_position) == 0
        if self.string_mode:
            current_id = self.f.readline().split(self.sep, 1)[0]
        else:
            current_id = int(self.f.readline().split(self.sep, 1)[0])

        if current_id == query:
            return 0
        else:
            return self.f.tell()

    def is_file_sorted(self) -> bool:
        """
        This helper function can be used as a sanity check.
        It tests whether your file is sorted according to Python rules.

        :returns: True if sorted; False if not sorted
        """

        if self.string_mode:
            prev = ''

            def a_smaller_than_b(a, b):
                return a < b
        else:
            self.f.seek(0)
            prev = int(self.f.readline().split(self.sep, maxsplit=1)[0]) - 1

            def a_smaller_than_b(a, b):
                return int(a) < int(b)

        self.f.seek(0)
        line = self.f.readline()
        while line:
            curr = line.split(self.sep, maxsplit=1)[0]
            if a_smaller_than_b(curr, prev):
                return False
            prev = curr
            line = self.f.readline()
        return True
