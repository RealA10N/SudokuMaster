class SudokuTable():

    def __init__(self, size=3):

        if type(size) != int or size < 2:
            raise TableInvalidSize(
                "Sudoku table size ({}) must be an integer larger then 1.".format(size))

        self._table_size = size
        self._table_full_size = size**2
        self._table = self._gen_empty_table()

    def print_table(self, palette=['─', '│', '┌', '┐', '└', '┘', ' ']):

        line_middle = ''
        for i in range(((3 + len(str(self.get_full_size()))) * self.get_full_size()) - 1):
            line_middle += palette[0]

        print(palette[2] + line_middle + palette[3])  # prints top line

        for index_row, row in enumerate(self._table):

            # print rows break
            if index_row % self.get_size() == 0 and index_row != 0:
                print(palette[1] + line_middle + palette[1])

            wip_row = ''
            for index_col, item in enumerate(row):

                item_format = [None, None]
                if item is None:
                    item_format[0] = palette[6]
                else:
                    item_format[0] = item

                if index_col % self.get_size() == 0:
                    item_format[1] = palette[1]
                else:
                    item_format[1] = palette[6]

                wip_row += '{} {} '.format(item_format[1], item_format[0])
            print(wip_row + palette[1])

        print(palette[4] + line_middle + palette[5])  # prints bottom line

    # -- G E T S -- #

    # returns list of all the rows in the table

    def get_table(self):
        return self._table

    # returns value of a specific cell in the table
    def get_cell(self, row, column):
        try:
            return self._table[row][column]
        except IndexError:
            raise ItemNotFound(
                "The cell in row {} and column {} is out of range.".format(row, column))

    # returns a list of the items in a specific row
    def get_row(self, row):
        try:
            return self._table[row]
        except IndexError:
            raise ItemNotFound("The row {} is out of range.".format(row))

    # returns a list of the items in a specific column
    def get_column(self, column):
        try:
            wip_column = list()
            for row in self._table:
                wip_column.append(row[column])
            return wip_column
        except IndexError:
            raise ItemNotFound("The column {} is out of range.".format(column))

    # returns a list of the items in a specific square
    def get_square(self, row, column):
        sq_start_row = (row // self.get_size()) * self.get_size()
        sq_start_column = (column // self.get_size()) * self.get_size()
        wip_square = list()

        for row in self.get_table()[sq_start_row: sq_start_row + self.get_size()]:
            for cell in row[sq_start_column: sq_start_column + self.get_size()]:
                wip_square.append(cell)
        return wip_square

    # returns the size of the table
    # classic sudoku table would be 3!
    def get_size(self):
        return self._table_size

    # returns the full size of the table (the size squared)
    # classic sudoku table would be 9!
    def get_full_size(self):
        return self._table_full_size

    # returns a list of the valid inputs in the table
    # classic sudoku table would be 1-9!
    def get_valid_inputs(self):
        return range(1, self.get_full_size() + 1)

    # -- S E T S -- #

    # Sets a value for a specific cell

    def set_cell(self, row, column, value):
        if not self._valid_value(value):
            raise InvalidSudokuValue(
                "The value {} is not valid in Sudoku, or in this table.".format(value))

        value_before = self.get_cell(row, column)

        try:
            self._table[row][column] = value
        except IndexError:
            raise ItemNotFound(
                "The cell in row {} and column {} is out of range.".format(row, column))

        check_results = (self.check_valid_row(row), self.check_valid_column(
            column), self.check_valid_square(row, column))
        if False in check_results:
            self._table[row][column] = value_before
            raise SudokuMistake(
                "{} can't be placed in row {} and column {}.".format(value, row, column))

    # -- P R I V A T E   F U N C T I O N S -- #

    def _valid_value(self, value):
        if value is None or value in range(1, (self.get_full_size()) + 1):
            return True
        else:
            return False

    # Generates an empty table, size given in init
    def _gen_empty_table(self):
        process_table = list()
        for row in range(self.get_full_size()):
            process_row = list()
            for column in range(self.get_full_size()):
                process_row.append(None)
            process_table.append(process_row)
        return process_table

    # -- C H E C K S -- #

    def check_valid_row(self, row_index):
        return self._check_valid_list(self.get_row(row_index))

    def check_valid_column(self, col_index):
        return self._check_valid_list(self.get_column(col_index))

    def check_valid_square(self, row_index, col_index):
        return self._check_valid_list(self.get_square(row_index, col_index))

    # checks for duplicates in a list. used to check valid row, columns and squares
    def _check_valid_list(self, in_list):
        used_before = list()
        for item in in_list:
            if item is not None:
                if item not in used_before:
                    used_before.append(item)
                else:
                    return False
        return True

    # checks every row, column and square in the table
    def check_valid_table(self):
        for cur_index in range(self.get_full_size()):

            if not self.check_valid_row(cur_index):
                return False

            if not self.check_valid_column(cur_index):
                return False

            square_row = (cur_index // self.get_size()) * self.get_size()
            square_column = (cur_index % self.get_size()) * self.get_size()
            if not self.check_valid_square(square_row, square_column):
                return False
        return True

    def solve(self):
        return self._solving_recursion(0, 0)

    def _solving_recursion(self, row, col):

        if (row, col) == (None, None):
            return True  # will happed if the last cell isn't None

        next_cell = self._get_next_cell(row, col)

        value_before = self.get_cell(row, col)
        if value_before is not None:
            return self._solving_recursion(next_cell[0], next_cell[1])

        for cur_input in self.get_valid_inputs():
            try:
                self.set_cell(row, col, cur_input)
            except SudokuMistake:
                continue

            next_result = self._solving_recursion(next_cell[0], next_cell[1])
            if next_result:
                return True  # solution found

        self.set_cell(row, col, value_before)
        return False

    # returns the position (row, col) of the next cell in the table
    # cell (0, 0) located in the top left!
    def _get_next_cell(self, row, col):

        if row >= self.get_full_size() - 1:
            if col >= self.get_full_size() - 1:
                return (None, None)  # final cell

        else:
            if col >= self.get_full_size() - 1:
                return (row + 1, 0)

        return (row, col + 1)


# # # # # # # # # # # #
# E X C E P T I O N S #
# # # # # # # # # # # #

class ItemNotFound(Exception):
    pass


class TableInvalidSize(Exception):
    pass


class InvalidSudokuValue(Exception):
    pass


class SudokuMistake(Exception):
    pass
