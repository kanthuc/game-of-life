#!/usr/bin/python3

import math
from tkinter import Tk, Button, Label, Canvas, Frame
from golengine import Cell, Board

class GameGrid:
    DEFAULT_PIXELS_PER_CELL = 10
    LIVE_COLOR = "blue"
    DEAD_COLOR = "white"

    def __init__(self, canvas, board):
        self.canvas = canvas
        self.top_left = Cell(0,0)
        self.scale = 1
        self.board = board

    def draw(self, cell, color):
        x1, y1, x2, y2 = self.get_cell_bounds(cell)
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

    def draw_cell(self, cell):
        if self.board.is_alive(cell):
            self.draw(cell,GameGrid.LIVE_COLOR)
        else:
            self.draw(cell, GameGrid.DEAD_COLOR)

    def draw_frame(self, live_cells):
        self.canvas.delete("all")
        for cell in live_cells:
            self.draw_cell(cell)

    def get_cell_bounds(self, cell):
        x1 = (cell.x-self.top_left.x)*self.scale*GameGrid.DEFAULT_PIXELS_PER_CELL
        y1 = (cell.y-self.top_left.y)*self.scale*GameGrid.DEFAULT_PIXELS_PER_CELL
        x2 = (cell.x-self.top_left.x+1)*self.scale*GameGrid.DEFAULT_PIXELS_PER_CELL
        y2 = (cell.y-self.top_left.y+1)*self.scale*GameGrid.DEFAULT_PIXELS_PER_CELL
        return x1, y1, x2, y2

    def which_cell(self, x, y):
        cx = math.floor(x/GameGrid.DEFAULT_PIXELS_PER_CELL/self.scale)+self.top_left.x
        cy = math.floor(y/GameGrid.DEFAULT_PIXELS_PER_CELL/self.scale)+self.top_left.y
        return Cell(cx, cy)

class Highlighter:
    HIGHLIGHT_COLOR = "sky blue"

    def __init__(self, grid):
        self.grid = grid
        self.last_cell = None

    def draw(self, last_cell):
        self.clear()
        self.grid.draw(last_cell, Highlighter.HIGHLIGHT_COLOR)
        self.last_cell = last_cell

    def clear(self):
        if self.last_cell:
            self.grid.draw_cell(self.last_cell)

class Playback:
    def __init__(self, grid, board, canvas):
        self.grid = grid
        self.board = board
        self.canvas = canvas
        self.is_running = False

    def update(self):
        if self.is_running:
            self.board.update()
            self.grid.draw_frame(self.board.get_live_cells())
            self.canvas.after(100, self.update)

    def start(self):
        self.is_running = True
        self.update()

    def stop(self):
        self.is_running = False

    def get_run_status(self):
        return self.is_running

class MainWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Conway's Game of Life")

        self.button_frame = Frame(master)
        self.button_frame.pack(side="top")

        self.start_button = Button(self.button_frame, text="Start", command=self.start_stop)
        self.start_button.pack(side="left")

        self.clear_button = Button(self.button_frame, text="Clear", command=self.clear)
        self.clear_button.pack(side="left")

        self.next_button = Button(self.button_frame, text="→", command=self.next_frame)
        self.next_button.pack(side="left")

        canvas = Canvas(master, bg="white", height=500, width=500)
        canvas.pack(side="top", expand=True, fill="both")

        self.board = Board()
        self.grid = GameGrid(canvas, self.board)
        self.highlighter = Highlighter(self.grid)
        self.playback = Playback(self.grid, self.board, canvas)

        canvas.bind("<Motion>", self.mouse_over)
        canvas.bind("<Leave>", self.leave_canvas)
        canvas.bind("<Button-1>", self.click_canvas)

    def start_stop(self):
        if self.playback.get_run_status():
            self.playback.stop()
            self.start_button['text'] = "Start"
        else:
            self.playback.start()
            self.start_button['text'] = "Stop"

    def clear(self):
        self.board.clear_board()
        self.grid.draw_frame(self.board.get_live_cells())

    def next_frame(self):
        print(str(self.board)+"\n")
        self.board.update()
        print(str(self.board)+"\n")
        self.grid.draw_frame(self.board.get_live_cells())

    def mouse_over(self, event):
        current_cell = self.grid.which_cell(event.x, event.y)
        self.highlighter.draw(current_cell)

    def leave_canvas(self, event):
        self.highlighter.clear()

    def click_canvas(self, event):
        current_cell = self.grid.which_cell(event.x, event.y)
        self.board.toggle_cell(current_cell)
        self.grid.draw_cell(current_cell)
        print(current_cell)

def main():
    root = Tk()
    window = MainWindow(root)
    root.mainloop()

if __name__=='__main__':
    main()
