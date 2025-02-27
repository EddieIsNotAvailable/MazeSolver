import argparse

from maze import Maze
from graphics import Window
import sys

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--num_rows', type=int, default=12, help='Number of rows (default: 12)')
    parser.add_argument('--num_cols', type=int, default=16, help='Number of columns (default: 16)')
    parser.add_argument('--width', type=int, default=1000, help='Window width in pixels (default: 1000)')
    parser.add_argument('--height', type=int, default=600, help='Window height in pixels (default: 600)')
    parser.add_argument('--delay', type=float, default=0.02, help='Animation delay in seconds (default: 0.02)')
    parser.add_argument('--seed', type=int, default=None, help='Random seed for maze generation (default: None)')

    args = parser.parse_args()

    num_rows = args.num_rows
    num_cols = args.num_cols
    screen_x = args.width
    screen_y = args.height
    delay = args.delay
    seed = args.seed

    margin_offset = 50

    x_draw_space = (screen_x - (2 * margin_offset))
    y_draw_space = (screen_y - (2 * margin_offset))

    cell_size_x = x_draw_space / num_cols
    cell_size_y = y_draw_space / num_rows


    #Increase recursion limit to prevent errors
    sys.setrecursionlimit(10000)
    w = Window(screen_x, screen_y)
    maze = Maze(margin_offset, margin_offset, num_rows, num_cols, cell_size_x, cell_size_y, w, seed, delay)

    maze_is_solvable = maze.solve()
    if not maze_is_solvable:
        print("Maze cannot be solved!")
    else:
        print("Maze solved!")

    w.wait_for_close()


main()

