from __future__ import annotations

from tkinter import Canvas, Tk, BOTH

class Point:
    def __init__(self, x: int | float, y: int | float):
        self.x = x
        self.y = y

class Line:
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas: Canvas, fill_color: str = "black"):
        canvas.create_line(self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill_color, width=2)



class Window:
    def __init__(self, width: int, height: int):
        self.root = Tk()
        self.root.title("Maze Generator")
        self.canvas = Canvas(self.root, bg="white", width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)
        self.running = False

        # Delete window when close() is called
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def close(self):
        self.running = False

    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
        print("Window closed...")

    def draw_line(self, line: Line, fill_color: str = "black"):
        line.draw(self.canvas, fill_color)
