import tkinter as tk
import time
import math
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        if seed is not None:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for i in range(self.num_cols):
            column = []
            for j in range(self.num_rows):
                x1 = self.x1 + i * self.cell_size_x
                y1 = self.y1 + j * self.cell_size_y
                x2 = x1 + self.cell_size_x
                y2 = y1 + self.cell_size_y
                cell = Cell(x1, y1, x2, y2, self.win)
                column.append(cell)
            self._cells.append(column)
        
        # Draw all cells after they have been added to the list
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        cell = self._cells[i][j]
        cell.draw()
        self._animate()

    def _animate(self):
        self.win.redraw()
        time.sleep(0.01)

    def _break_entrance_and_exit(self):
        # Remove the top wall of the top-left cell
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        
        # Remove the bottom wall of the bottom-right cell
        self._cells[self.num_cols - 1][self.num_rows - 1].has_bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i, j):
        cell = self._cells[i][j]
        cell.visited = True

        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        random.shuffle(directions)

        for di, dj in directions:
            ni, nj = i + di, j + dj

            if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows and not self._cells[ni][nj].visited:
                if di == -1:
                    cell.has_left_wall = False
                    self._cells[ni][nj].has_right_wall = False
                elif di == 1:
                    cell.has_right_wall = False
                    self._cells[ni][nj].has_left_wall = False
                elif dj == -1:
                    cell.has_top_wall = False
                    self._cells[ni][nj].has_bottom_wall = False
                elif dj == 1:
                    cell.has_bottom_wall = False
                    self._cells[ni][nj].has_top_wall = False

                self._draw_cell(i, j)
                self._break_walls_r(ni, nj)

    def _reset_cells_visited(self):
        for column in self._cells:
            for cell in column:
                cell.visited = False

    def solve(self):
        return self._solve_r(0, 0)

    def _solve_r(self, i, j):
        self._animate()
        cell = self._cells[i][j]
        cell.visited = True

        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        for di, dj in directions:
            ni, nj = i + di, j + dj

            if 0 <= ni < self.num_cols and 0 <= nj < self.num_rows and not self._cells[ni][nj].visited:
                if (di == -1 and not cell.has_left_wall) or (di == 1 and not cell.has_right_wall) or (dj == -1 and not cell.has_top_wall) or (dj == 1 and not cell.has_bottom_wall):
                    self._cells[i][j].draw_move(self._cells[ni][nj])
                    if self._solve_r(ni, nj):
                        return True
                    self._cells[i][j].draw_move(self._cells[ni][nj], undo=True)

        return False


class Cell:
    def __init__(self, x1, y1, x2, y2, win):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.visited = False
        self._x1 = x1
        self._x2 = x2
        self._y1 = y1
        self._y2 = y2
        self._win = win

    def draw(self):
        if self.has_left_wall:
            self._win.canvas.create_line(self._x1, self._y1, self._x1, self._y2)
        else:
            self._win.canvas.create_line(self._x1, self._y1, self._x1, self._y2, fill="#d9d9d9")
        if self.has_right_wall:
            self._win.canvas.create_line(self._x2, self._y1, self._x2, self._y2)
        else:
            self._win.canvas.create_line(self._x2, self._y1, self._x2, self._y2, fill="#d9d9d9")
        if self.has_top_wall:
            self._win.canvas.create_line(self._x1, self._y1, self._x2, self._y1)
        else:
            self._win.canvas.create_line(self._x1, self._y1, self._x2, self._y1, fill="#d9d9d9")
        if self.has_bottom_wall:
            self._win.canvas.create_line(self._x1, self._y2, self._x2, self._y2)
        else:
            self._win.canvas.create_line(self._x1, self._y2, self._x2, self._y2, fill="#d9d9d9")

    def draw_move(self, to_cell, undo=False):
        color = "gray" if undo else "red"
        x1 = (self._x1 + self._x2) // 2
        y1 = (self._y1 + self._y2) // 2
        x2 = (to_cell._x1 + to_cell._x2) // 2
        y2 = (to_cell._y1 + to_cell._y2) // 2
        self._win.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y,
            self.point2.x, self.point2.y,
            fill=fill_color, width=2
        )

class Window:
    def __init__(self, width, height):
        self.root = tk.Tk()
        self.root.title("My Window")
        self.canvas = tk.Canvas(self.root, width=width, height=height)
        self.canvas.pack()
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()

    def close(self):
        self.running = False
        self.root.destroy()

    def draw_line(self, line, fill_color):
        line.draw(self.canvas, fill_color)


# Example usage:
win = Window(900, 900)

# Create a maze with a fixed seed for debugging
seed = math.sqrt(time.time())
maze = Maze(50, 50, 20, 20, 40, 40, win, seed)

# Solve the maze
maze.solve()

win.wait_for_close()
