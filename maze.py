import time
import random

from graphics import Point, Window
from cell import Cell

class Maze:
    def __init__(
        self,
        draw_offset_x: int | float,
        draw_offset_y: int | float,
        num_rows: int, num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        window: Window = None,
        seed: random.seed = None,
        draw_delay: float = .05
    ):

        if seed:
            random.seed(seed)
        self.cells: list[list[Cell]] | None = None
        self.window = window
        self.draw_offset_x = draw_offset_x
        self.draw_offset_y = draw_offset_y
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.draw_delay = draw_delay

        self.create_cells()
        self.break_entrance_and_exit()
        self.break_walls(0, 0)
        self.reset_cells_visited()


    def create_cells(self):
        self.cells = []
        for i in range(self.num_cols):
            row: list[Cell] = []
            for j in range(self.num_rows):
                row.append(Cell(self.window))
            self.cells.append(row)

        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.draw_cell(i,j)



    def draw_cell(self, i, j):
        x1 = self.draw_offset_x + (i * self.cell_size_x)
        y1 = self.draw_offset_y + (j * self.cell_size_y)
        top_left = Point(x1, y1)
        bottom_right = Point(x1 + self.cell_size_x, y1 + self.cell_size_y)
        self.cells[i][j].draw(top_left, bottom_right)
        self.animate()

    def animate(self):
        self.window.redraw()
        time.sleep(self.draw_delay)

    def break_entrance_and_exit(self):
        self.cells[0][0].has_top_wall = False
        self.cells[self.num_cols-1][self.num_rows-1].has_bottom_wall = False

    def break_walls(self, i, j):
        self.cells[i][j].visited = True

#TODO: Perhaps add while True to this. Dont understand why would put it as of now.
        while True:
            valid_adj_list = []

            if i > 0 and not self.cells[i-1][j].visited:
                valid_adj_list.append((i-1, j))
            if j > 0 and not self.cells[i][j-1].visited:
                valid_adj_list.append((i, j-1))
            if i < self.num_cols - 1 and not self.cells[i+1][j].visited:
                valid_adj_list.append((i+1, j))
            if j < self.num_rows - 1 and not self.cells[i][j+1].visited:
                valid_adj_list.append((i, j+1))

            if len(valid_adj_list) == 0:
                self.draw_cell(i, j)
                return

            next_idx = random.choice(valid_adj_list)

            next_i, next_j = next_idx
            if next_i == i+1:
                self.cells[i][j].has_right_wall = False
                self.cells[next_i][j].has_left_wall = False
            elif next_i == i-1:
                self.cells[i][j].has_left_wall = False
                self.cells[next_i][j].has_right_wall = False
            elif next_j == j+1:
                self.cells[i][j].has_bottom_wall = False
                self.cells[i][next_j].has_top_wall = False
            elif next_j == j-1:
                self.cells[i][j].has_top_wall = False
                self.cells[i][next_j].has_bottom_wall = False

            self.break_walls(next_i, next_j)

    def reset_cells_visited(self):
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self.cells[i][j].visited = False

    def solve(self) -> bool:
        return self.solve_r(0, 0)

    def solve_r(self, i: int, j: int) -> bool:
        self.animate()
        self.cells[i][j].visited = True

        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        curr_cell = self.cells[i][j]

        #Try the directions
        # left
        if (
            i > 0
            and not curr_cell.has_left_wall
            and self.try_path(curr_cell, i-1, j)
        ):
            return True

        # right
        if (
            i < self.num_cols - 1
            and not curr_cell.has_right_wall
            and self.try_path(curr_cell, i+1, j)
        ):
            return True

        # up
        if (
            j > 0
            and not curr_cell.has_top_wall
            and self.try_path(curr_cell, i, j-1)
        ):
            return True

        # down
        if (
            j < self.num_rows - 1
            and not curr_cell.has_bottom_wall
            and self.try_path(curr_cell, i, j+1)
        ):
            return True

        #No valid paths
        return False



    def try_path(self, curr_cell: Cell, newi: int, newj: int) -> bool:
        dest_cell = self.cells[newi][newj]

        if dest_cell.visited:
            return False

        curr_cell.draw_move(dest_cell)

        if self.solve_r(newi, newj):
            return True
        else:
            curr_cell.draw_move(dest_cell, True)
            return False
