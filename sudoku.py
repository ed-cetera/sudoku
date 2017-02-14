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
        if not isinstance(grid_string, str):
            raise GridStringError()
        self.grid = [[None for _dummy in range(9)] for _dummy in range(9)]
        if grid_string == "":
            return
        if len(grid_string) != 81:
            raise GridStringError()
        position = 0
        for (line, row) in [(ln, rw) for ln in range(9) for rw in range(9)]:
            if grid_string[position] == ".":
                pass
            elif int(grid_string[position]) in range(1, 10):
                self.grid[line][row] = int(grid_string[position])
            else:
                raise GridStringError()
            position += 1

    def verify_vertex_values(self):
        """Verify that the current grid has only valid vertex values."""
        for (line, row) in [(ln, rw) for ln in range(9) for rw in range(9)]:
            if self.grid[line][row] not in range(1, 10) and self.grid[line][row] is not None:
                raise VertexValueError()

    def __str__(self):
        # Verify correct vertex values
        self.verify_vertex_values()
        # Generate output string
        output_string = ""
        for (line, row) in [(ln, rw) for ln in range(9) for rw in range(9)]:
            if self.grid[line][row] is None:
                output_string += "."
            else:
                output_string += str(self.grid[line][row])
        return output_string

    def formatted_str(self):
        """Return formatted string for printing the grid."""
        # Verify correct vertex values
        self.verify_vertex_values()
        # Generate output string
        output_string = ""
        for line in range(9):
            for row in range(9):
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

    def candidate_map(self):
        """Return two-dimensional list of sets composed of possible candidates for each vertex."""
        candidates = [[set(range(1, 10)) for _dummy in range(9)] for _dummy in range(9)]
        vertex_value_unknown = [[True for _dummy in range(9)] for _dummy in range(9)]
        for (line, row) in [(ln, rw) for ln in range(9) for rw in range(9)]:
            if self.grid[line][row] in range(1, 10):
                candidates[line][row] = set([self.grid[line][row]])
                vertex_value_unknown[line][row] = False
                for i in range(9):
                    if i != row:
                        candidates[line][i].discard(self.grid[line][row])
                    if i != line:
                        candidates[i][row].discard(self.grid[line][row])
                    if line - line%3 + i//3 != line or row - row%3 + i%3 != row:
                        candidates[line - line%3 + i//3][row - row%3 + i%3].discard(self.grid[line][row])
        # Further reduce candidate map
        reduce_cadidate_map_further = True
        while reduce_cadidate_map_further:
            reduce_cadidate_map_further = False
            total_number_of_candidates = sum([len(candidates[ln][rw]) for ln in range(9) for rw in range(9)])
            for number in range(1, 10):
                for i in range(9):
                    # Check for single possible vertex for *number* in candidate map line *i*
                    seen_in_j = []
                    for j in range(9):
                        if number in candidates[i][j]:
                            seen_in_j.append(j)
                    if len(seen_in_j) == 1 and vertex_value_unknown[i][seen_in_j[0]]:
                        candidates[i][seen_in_j[0]] = set([number])
                        vertex_value_unknown[i][seen_in_j[0]] = False
                        # Discard other candidates for *number* in corresponding row and subsquare
                        for j in range(9):
                            if j != i:
                                candidates[j][seen_in_j[0]].discard(number)
                            if i - i%3 + j//3 != i:
                                candidates[i - i%3 + j//3][seen_in_j[0] - seen_in_j[0]%3 + j%3].discard(number)
                    # otherwise add check wheter all candidates for *number* are in the same subsquare
                    elif 1 < len(seen_in_j) < 4:
                        subsquares = set()
                        for j in seen_in_j:
                            subsquares.add(3*(i//3) + j//3)
                        if len(subsquares) == 1:
                            subsquare = subsquares.pop()
                            for j in range(9):
                                if 3*(subsquare//3) + j//3 != i:
                                    candidates[3*(subsquare//3) + j//3][3*(subsquare%3) + j%3].discard(number)
                    # Check for single possible vertex for *number* in candidate map row *i*
                    seen_in_j = []
                    for j in range(9):
                        if number in candidates[j][i]:
                            seen_in_j.append(j)
                    if len(seen_in_j) == 1 and vertex_value_unknown[seen_in_j[0]][i]:
                        candidates[seen_in_j[0]][i] = set([number])
                        vertex_value_unknown[seen_in_j[0]][i] = False
                        # Discard other candidates for *number* in corresponding line and subsquare
                        for j in range(9):
                            if j != i:
                                candidates[seen_in_j[0]][j].discard(number)
                            if i - i%3 + j%3 != i:
                                candidates[seen_in_j[0] - seen_in_j[0]%3 + j//3][i - i%3 + j%3].discard(number)
                    # otherwise add check wheter all candidates for *number* are in the same subsquare
                    elif 1 < len(seen_in_j) < 4:
                        subsquares = set()
                        for j in seen_in_j:
                            subsquares.add(3*(j//3) + i//3)
                        if len(subsquares) == 1:
                            subsquare = subsquares.pop()
                            for j in range(9):
                                if 3*(subsquare%3) + j%3 != i:
                                    candidates[3*(subsquare//3) + j//3][3*(subsquare%3) + j%3].discard(number)
                    # Check for single possible vertex for *number* in candidate map subsquare *i*
                    seen_in_j = []
                    for j in range(9):
                        if number in candidates[3*(i//3) + j//3][3*(i%3) + j%3]:
                            seen_in_j.append(j)
                    if len(seen_in_j) == 1 and vertex_value_unknown[3*(i//3) + seen_in_j[0]//3][3*(i%3) + seen_in_j[0]%3]:
                        candidates[3*(i//3) + seen_in_j[0]//3][3*(i%3) + seen_in_j[0]%3] = set([number])
                        vertex_value_unknown[3*(i//3) + seen_in_j[0]//3][3*(i%3) + seen_in_j[0]%3] = False
                        # Discard other candidates for *number* in corresponding line and row
                        for j in range(9):
                            if j not in [3*(i%3), 3*(i%3) + 1, 3*(i%3) + 2]:
                                candidates[3*(i//3) + seen_in_j[0]//3][j].discard(number)
                            if j not in [3*(i//3), 3*(i//3) + 1, 3*(i//3) + 2]:
                                candidates[j][3*(i%3) + seen_in_j[0]%3].discard(number)
                    # otherwise add check wheter all candidates for *number* are in the same line/row
                    elif 1 < len(seen_in_j) < 4:
                        lines = set()
                        rows = set()
                        for j in seen_in_j:
                            lines.add(3*(i//3) + j//3)
                            rows.add(3*(i%3) + j%3)
                        if len(lines) == 1:
                            line = lines.pop()
                            for row in [rw for rw in range(9) if rw not in [3*(i%3), 3*(i%3) + 1, 3*(i%3) + 2]]:
                                candidates[line][row].discard(number)
                        elif len(rows) == 1:
                            row = rows.pop()
                            for line in [ln for ln in range(9) if ln not in [3*(i//3), 3*(i//3) + 1, 3*(i//3) + 2]]:
                                candidates[line][row].discard(number)
            if sum([len(candidates[ln][rw]) for ln in range(9) for rw in range(9)]) < total_number_of_candidates:
                reduce_cadidate_map_further = True
        return candidates

    def valid(self):
        """Check whether the current grid is valid and return bool."""
        # Verify correct vertex values
        self.verify_vertex_values()
        # Check for duplicate values in lines
        for line in range(9):
            seen = []
            for row in range(9):
                if self.grid[line][row] is None:
                    pass
                elif self.grid[line][row] in seen:
                    return False
                else:
                    seen.append(self.grid[line][row])
        # Check for duplicate values in rows
        for row in range(9):
            seen = []
            for line in range(9):
                if self.grid[line][row] is None:
                    pass
                elif self.grid[line][row] in seen:
                    return False
                else:
                    seen.append(self.grid[line][row])
        # Check for duplicate values in subgrids
        for (subgrid_line, subgrid_row) in [(subg_ln, subg_rw) for subg_ln in range(3) for subg_rw in range(3)]:
            seen = []
            for (line, row) in [(ln, rw) for ln in range(3) for rw in range(3)]:
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

def solve_puzzle(grid):
    """Solve the given puzzle, return solutions as list of Sudoku instances."""
    solutions = []
    if not grid.valid():
        return solutions
    # Backtracking, iterating over (first) smallest list of candidates for empty vertices
    candidates = grid.candidate_map()
    min_number_of_candidates = min([9] + [len(candidates[ln][rw]) for ln in range(9) for rw in range(9) if grid.grid[ln][rw] is None])
    for (line, row) in [(ln, rw) for ln in range(9) for rw in range(9)]:
        if grid.grid[line][row] is None and len(candidates[line][row]) == min_number_of_candidates:
            for guess in candidates[line][row]:
                grid.grid[line][row] = guess
                for solution in solve_puzzle(grid):
                    solutions.append(solution)
            grid.grid[line][row] = None
            break
    else:
        solutions.append(Sudoku(grid.__str__()))
    return solutions

# Main
input_grids = grids_from_stdin()
for grid in input_grids:
    solutions = solve_puzzle(grid)
    print("p", grid, sep="")
    for solution in solutions:
        print("s", solution, sep="")
