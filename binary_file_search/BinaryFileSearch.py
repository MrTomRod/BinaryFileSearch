import os


class BinaryFileSearch:
    """
    Binary search algorithm for big sorted files that cannot be read into RAM.

    Requirements:
    -------------
        - file must be sorted by the first column
            (bash example: sort --key=1 --field-separator=\t --output=file.txt.sorted file.txt)
        - every line must begin with the sorted string/integer, followed by a separator
        - there may be multiple lines beginning with the same string/integer
            (the script will return a list of lines that start with the same string/integer)

    Example Usage:
    --------------
    bfs = BinaryFileSearch(file_path, sep="\t")
    lines = bfs.extract_lines_beginning_with(query)  # get lines that begin with :param query:

    Tip: run bfs.close_file() after usage!

    Credit:
    -------
    Inspired by https://www.geeksforgeeks.org/python-program-for-binary-search/

    :param file: the sorted file to be searched
    :param sep: separator (default: "\t")
    :param string_mode: True if the sorted column consists of strings, False if integers
    :param query: string/integer to search

    :returns: list of lines, the lines being separated by :param sep:, e.g. [ [[query][l1]], [[query][l2]], ... ]
    :rtype: int
    :raises KeyError: if the number isn't found
    """

    def __init__(self, file: str, sep: str = "\t", string_mode: bool = False):
        assert os.path.isfile(file), "Error: file does not exist: '{}'".format(file)
        self.file_path = file
        self.f = None
        self.length = None
        self.sep = None
        self.string_mode = None

        self.open_file(file=file, sep=sep, string_mode=string_mode)

    def open_file(self, file=None, sep: str = None, string_mode: bool = None):
        self.close_file()
        if file == None: file = self.file_path
        if sep == None: sep = self.sep
        if string_mode == None: string_mode = self.string_mode
        assert os.path.isfile(file), "Error: file does not exist: '{}'".format(file)
        self.file_path = file
        self.f = open(file, 'rt')
        self.f.seek(0, 2)  # 0 = offset, 2 = relative to file end => go to last char in file!
        self.length = self.f.tell()
        self.sep = sep
        self.string_mode = string_mode

    def extract_lines_beginning_with(self, query) -> list:
        if self.string_mode:
            assert type(query) == str, "string_mode is on, query type must be str! query: {}, type: {}".format(query,
                                                                                                               type(
                                                                                                                   query))
        else:
            assert type(query) == int, "string_mode is off, query type must be int! query: {}, type: {}".format(query,
                                                                                                                type(
                                                                                                                    query))

        # find the offset where the matching lines begin
        offset = self.__binary_search(query=query)

        # move to offset
        self.f.seek(offset)

        # return matching lines as list
        lines_that_start_with_query = []
        line = self.f.readline().strip().split("\t")
        if not self.string_mode: line[0] = int(line[0])
        while line[0] == query:
            lines_that_start_with_query.append(line)

            line = self.f.readline().strip().split("\t")
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

    def get_file(self):
        return self.f

    def close_file(self):
        if self.f and not self.f.closed:
            self.f.close()
