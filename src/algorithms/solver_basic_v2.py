# -*- coding: utf-8 -*-
"""
Basic Sudoku Solver using DFS Backtracking.

This version adds event callback interface for visualization.
"""

from typing import List, Optional, Callable

Board = List[List[int]]  # 9x9 Sudoku board, where 0 means empty

class SudokuSolver:
    def __init__(self, update_callback: Optional[Callable] = None):
        """Initialize with an optional callback function for visual updates."""
        self.update_callback = update_callback  # This is the event callback for UI updates

    def solve(self, board: Board) -> Optional[Board]:
        """Solve the Sudoku board. Returns the solved board or None if unsolvable."""
        # 1. First, validate the initial board (no duplicates in rows/columns/boxes)
        if not self._is_board_valid(board):
            print("Initial board is invalid (duplicates exist).")
            return None

        # 2. Proceed with backtracking only if the initial board is legal
        if self._backtrack(board):
            return board
        print("No solution found.")
        return None

    def _is_board_valid(self, board: Board) -> bool:
        """Check if the initial board follows Sudoku rules (no duplicates in rows/columns/boxes)."""
        # Check rows
        for row in board:
            seen = set()
            for num in row:
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)

        # Check columns
        for col in range(9):
            seen = set()
            for row in range(9):
                num = board[row][col]
                if num != 0:
                    if num in seen:
                        return False
                    seen.add(num)

        # Check 3x3 boxes
        for box_row in range(3):  # 0-2 for top/middle/bottom boxes
            for box_col in range(3):  # 0-2 for left/middle/right boxes
                seen = set()
                start_r = box_row * 3
                start_c = box_col * 3
                # Iterate through each cell in the 3x3 box
                for r in range(start_r, start_r + 3):
                    for c in range(start_c, start_c + 3):
                        num = board[r][c]
                        if num != 0:
                            if num in seen:
                                return False
                            seen.add(num)
        return True

    def _backtrack(self, board: Board) -> bool:
        empty_cell = self._find_empty_cell(board)
        if not empty_cell:
            return True  # Solved

        row, col = empty_cell

        for num in range(1, 10):
            if self._is_valid(board, row, col, num):
                print(f"Placing {num} at ({row}, {col})")
                board[row][col] = num

                # Trigger visualization update (if callback exists)
                if self.update_callback:
                    self.update_callback(board, row, col, num, "fill")

                # Proceed with backtracking
                if self._backtrack(board):
                    return True

                board[row][col] = 0  # Backtrack
                print(f"Backtracking at ({row}, {col})")

                # Trigger visualization update (if callback exists)
                if self.update_callback:
                    self.update_callback(board, row, col, num, "backtrack")

        print(f"No valid number for ({row}, {col}).")
        return False

    def _find_empty_cell(self, board: Board) -> Optional[tuple]:
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return r, c
        return None

    def _is_valid(self, board: Board, row: int, col: int, num: int) -> bool:
        """Check if placing `num` at (row, col) is valid (for backtracking steps)."""
        # Check row (we can optimize by not checking the entire row, but this is clear)
        if num in board[row]:
            return False

        # Check column
        for r in range(9):
            if board[r][col] == num:
                return False

        # Check box
        box_row_start = (row // 3) * 3
        box_col_start = (col // 3) * 3
        for r in range(box_row_start, box_row_start + 3):
            for c in range(box_col_start, box_col_start + 3):
                if board[r][c] == num:
                    return False

        return True


# ---------------- Test Cases ----------------
if __name__ == "__main__":
    # Define a simple update callback function for testing
    def update_ui(board, row, col, num, action):
        """Callback function to update the UI. This will be called during each backtrack or fill step."""
        print(f"Action: {action} - Placing {num} at ({row}, {col})")
        for row in board:
            print(row)

    # Test Case 1: Valid and solvable board
    solvable_board = [
        [5, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]

    print("Starting to solve the Sudoku:")
    solver = SudokuSolver(update_callback=update_ui)
    solution = solver.solve(solvable_board)

    if solution:
        print("Solved board:")
        for row in solution:
            print(row)
    else:
        print("No solution found.")
