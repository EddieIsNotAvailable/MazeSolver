from __future__ import annotations

from graphics import Point, Line, Window


class Cell:
    def __init__(self, window: Window):
        self.window = window
        self.visited = False
        self.has_top_wall = True
        self.has_right_wall = True
        self.has_bottom_wall = True
        self.has_left_wall = True
        self.top_left = None
        self.bottom_right = None

    def draw(self, top_left: Point, bottom_right: Point):
        self.top_left = top_left
        self.bottom_right = bottom_right

        top_right = Point(bottom_right.x, top_left.y)
        bottom_left = Point(top_left.x, bottom_right.y)

        wall_absense_color = "white"

        top_line = Line(top_left, top_right)
        if self.has_top_wall:
            self.window.draw_line(top_line)
        else:
            self.window.draw_line(top_line, wall_absense_color)

        right_line = Line(top_right, bottom_right)
        if self.has_right_wall:
            self.window.draw_line(right_line)
        else:
            self.window.draw_line(right_line, wall_absense_color)

        bottom_line = Line(bottom_left, bottom_right)
        if self.has_bottom_wall:
            self.window.draw_line(bottom_line)
        else:
            self.window.draw_line(bottom_line, wall_absense_color)

        left_line = Line(top_left, bottom_left)
        if self.has_left_wall:
            self.window.draw_line(left_line)
        else:
            self.window.draw_line(left_line, wall_absense_color)

    def get_center_pt(self) -> Point:
        top_left = self.top_left
        bottom_right = self.bottom_right
        x_center = top_left.x + ((bottom_right.x - top_left.x)/2)
        y_center = top_left.y + ((bottom_right.y - top_left.y)/2)
        return Point(x_center, y_center)

    def draw_move(self, to_cel: Cell, undo=False):
        line = Line(self.get_center_pt(), to_cel.get_center_pt())
        color = "gray" if undo else "red"

        self.window.draw_line(line, color)
