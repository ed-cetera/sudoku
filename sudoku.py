#!/usr/bin/env python3

import sys


class Error(Exception):
    """Base class for custom exceptions."""
    pass


class GridStringError(Error):
    """Exception raised for errors in the string representation of a Sudoku grid."""
    pass


class VertexValueError(Error):
    """Exception raised for invalid values on the Sudoku grid."""
    pass


class Sudoku:
    """Sudoku grid."""

    def __init__(self, grid_string=""):
        self.grid = [[None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None],
                     [None, None, None, None, None, None, None, None, None]]
        if not isinstance(grid_string, str):
            raise GridStringError()
        if grid_string == "":
            return
        if len(grid_string) != 81:
            raise GridStringError()
        position = 0
        for (line, row) in [(ln, rw) for ln in range(0, 9) for rw in range(0, 9)]:
            if grid_string[position] == ".":
                self.grid[line][row] = None
            elif int(grid_string[position]) in range(1, 10):
                self.grid[line][row] = int(grid_string[position])
            else:
                raise GridStringError()
            position += 1

    def __str__(self):
        # Verify correct vertex values
        for (line, row) in [(ln, rw) for ln in range(0, 9) for rw in range(0, 9)]:
            if self.grid[line][row] not in range(1, 10) and self.grid[line][row] is not None:
                raise VertexValueError()
        # Generate output string
        output_string = ""
        for (line, row) in [(ln, rw) for ln in range(0, 9) for rw in range(0, 9)]:
            if self.grid[line][row] is None:
                output_string += "."
            else:
                output_string += str(self.grid[line][row])
        return output_string

    def formatted_str(self):
        """Return formatted string for printing the grid."""
        # Verify correct vertex values
        for (line, row) in [(ln, rw) for ln in range(0, 9) for rw in range(0, 9)]:
            if self.grid[line][row] not in range(1, 10) and self.grid[line][row] is not None:
                raise VertexValueError()
        # Generate output string
        output_string = ""
        for line in range(0, 9):
            for row in range(0, 9):
                if self.grid[line][row] is None:
                    output_string += "."
                else:
                    output_string += str(self.grid[line][row])
                if row != 8:
                    output_string += " "
                elif line != 8:
                    output_string += "\n"
                if row in [2, 5]:
                    output_string += "| "
            if line in [2, 5]:
                output_string += "------+-------+------\n"
        return output_string

    def valid(self):
        """Check whether the current grid is valid and return bool."""
        # Verify correct vertex values
        for (line, row) in [(ln, rw) for ln in range(0, 9) for rw in range(0, 9)]:
            if self.grid[line][row] not in range(1, 10) and self.grid[line][row] is not None:
                raise VertexValueError()
        # Check for duplicate values in lines
        for line in range(0, 9):
            seen = []
            for row in range(0, 9):
                if self.grid[line][row] is None:
                    pass
                elif self.grid[line][row] in seen:
                    return False
                else:
                    seen.append(self.grid[line][row])
        # Check for duplicate values in rows
        for row in range(0, 9):
            seen = []
            for line in range(0, 9):
                if self.grid[line][row] is None:
                    pass
                elif self.grid[line][row] in seen:
                    return False
                else:
                    seen.append(self.grid[line][row])
        # Check for duplicate values in subgrids
        for (subgrid_line, subgrid_row) in [(subg_ln, subg_rw) for subg_ln in range(0, 3) for subg_rw in range(0, 3)]:
            seen = []
            for (line, row) in [(ln, rw) for ln in range(0, 3) for rw in range(0, 3)]:
                if self.grid[3*subgrid_line + line][3*subgrid_row + row] is None:
                    pass
                elif self.grid[3*subgrid_line + line][3*subgrid_row + row] in seen:
                    return False
                else:
                    seen.append(self.grid[3*subgrid_line + line][3*subgrid_row + row])
        # No duplicates found
        return True


def grids_from_stdin():
    """Read stdin, return list of Sudoku instances, one per 81 correct input characters."""
    grids = []
    filtered_stdin_data = "".join([char for char in sys.stdin.read() if char in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "."]])
    while len(filtered_stdin_data) >= 81:
        grids.append(Sudoku(filtered_stdin_data[:81]))
        filtered_stdin_data = filtered_stdin_data[81:]
    return grids

# Main
input_grids = grids_from_stdin()
