from .utils import range_to_row_columns


class Range:
    def __init__(self, range_input):
        if isinstance(range_input, str):
            self.__init_str(range_input)
        elif isinstance(range_input, dict):
            self.__init_dict(range_input)
        else:
            raise TypeError("range_input should be str or dict")

    def __init_str(self, range_str):
        range_dict = range_to_row_columns(range_str)
        self.__init_from_range_dict(range_dict)

    def __init_dict(self, range_dict):
        if "startRowIndex" in range_dict and "startColumnIndex" in range_dict:
            start_column = range_dict["startColumnIndex"]
            assert start_column >= 0
            end_column = range_dict.get("endColumnIndex", start_column + 1)
            assert end_column > start_column
            start_row = range_dict["startRowIndex"]
            assert start_row >= 0
            end_row = range_dict.get("endRowIndex", start_row + 1)
            assert end_row > start_row
            self.__init_from_range_dict(
                {
                    "start_column": start_column,
                    "start_row": start_row,
                    "end_column": end_column,
                    "end_row": end_row,
                }
            )
        else:
            raise TypeError("did not recognize dictionary structure")

    def __init_from_range_dict(self, range_dict):
        self.start_column = range_dict["start_column"]
        self.end_column = range_dict["end_column"]
        self.start_row = range_dict["start_row"]
        self.end_row = range_dict["end_row"]

    def __eq__(self, other_range):
        if isinstance(other_range, Range):
            return (
                self.start_column == other_range.start_column
                and self.end_column == other_range.end_column
                and self.start_row == other_range.start_row
                and self.end_row == other_range.end_row
            )
        else:
            return False

    def is_within(self, other_range):
        if isinstance(other_range, Range):
            return (
                self.start_column >= other_range.start_column
                and self.end_column <= other_range.end_column
                and self.start_row >= other_range.start_row
                and self.end_row <= other_range.end_row
            )
        else:
            return False
