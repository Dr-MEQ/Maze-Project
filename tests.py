import unittest
from maze_window import Maze, Window

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 15
        num_rows = 15
        win = Window(800, 600)
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertEqual(
            len(m1._cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._cells[0]),
            num_rows,
        )

    def test_break_entrance_and_exit(self):
        num_cols = 15
        num_rows = 15
        win = Window(800, 600)
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        self.assertFalse(m1._cells[0][0].has_top_wall)
        self.assertFalse(m1._cells[num_cols - 1][num_rows - 1].has_bottom_wall)

    def test_reset_cells_visited(self):
        num_cols = 15
        num_rows = 15
        win = Window(800, 600)
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10, win)
        for column in m1._cells:
            for cell in column:
                self.assertFalse(cell.visited)

if __name__ == "__main__":
    unittest.main()
