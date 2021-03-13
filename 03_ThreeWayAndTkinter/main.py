import tkinter as tk
from functools import partial
from itertools import product
from random import choice
from tkinter import messagebox
from tkinter.constants import *


class GameOfFifteen:
    def __init__(self, height, width, complexity=50):
        self.__height = height
        self.__width = width
        self.__empty_cell_value = height * width
        self.__out_of_bounds = "out of bounds"
        self.__desk = self.__generate_tiles()
        self.__current_complexity = complexity
        self.__shuffle()

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    @property
    def complexity(self):
        return self.__current_complexity

    def restart(self, complexity=50):
        self.__desk = self.__generate_tiles()
        self.__current_complexity = complexity
        self.__shuffle()

    def turn(self, x, y):
        if self.__index_out_of_bounds(x, y):
            return False
        offsets = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        values = [self[(i, j)] for i, j in offsets]
        index = values.index(None) if None in values else None
        if index is None:
            return False
        i, j = offsets[index]
        self.__desk[x][y], self.__desk[i][j] = self.__desk[i][j], self.__desk[x][y]
        return True

    def is_finished(self):
        for i, j in self.__iterate():
            if self.__target(i, j) != self.__desk[i][j]:
                return False
        return True

    def __generate_tiles(self):
        return [[self.__target(i, j) for j in range(self.__width)] for i in range(self.__height)]

    def __shuffle(self):
        iterations = self.__current_complexity
        [(x, y)] = [t for t in self.__iterate() if self[t] is None]
        while iterations > 0:
            new_x, new_y = choice([(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)])
            if not self.turn(new_x, new_y):
                continue
            x, y = new_x, new_y
            if not self.is_finished():
                iterations -= 1

    def __target(self, i, j):
        return i * self.__width + j + 1

    def __index_out_of_bounds(self, i, j):
        return i < 0 or j < 0 or i >= self.__height or j >= self.__width

    def __iterate(self):
        return product(range(self.__height), range(self.__width))

    def __getitem__(self, item):
        i, j = item
        if self.__index_out_of_bounds(i, j):
            return self.__out_of_bounds
        result = self.__desk[i][j]
        if result == self.__empty_cell_value:
            return None
        return result


class GameOfFifteenWidget(tk.Frame):
    def __init__(self, game, master=None):
        super().__init__(master)
        self.__game = game
        self.__master = master
        self.__top_panel = tk.Frame(self)
        self.__new = tk.Button(self.__top_panel, text="New", command=partial(self.__restart, False))
        self.__exit = tk.Button(self.__top_panel, text="Exit", command=self.__master.destroy)
        self.__desk = tk.Frame(self)
        self.__tiles = self.__create_tiles()
        self.__pack_widgets()
        self.__redraw()
        self.winfo_toplevel().title("15")

    def __pack_widgets(self):
        self.pack(expand=True, fill=BOTH)
        self.__top_panel.pack(side="top", expand=False, fill=X)
        self.__new.pack(side="left")
        self.__exit.pack(side="right")
        self.__desk.pack(side="bottom", expand=True, fill=BOTH)

        for i in range(self.__game.height):
            self.__desk.rowconfigure(i, weight=1, uniform="cells")
        for j in range(self.__game.width):
            self.__desk.columnconfigure(j, weight=1, uniform="cells")

    def __create_tiles(self):
        def create(i, j): return tk.Button(self.__desk, command=partial(self.__on_click, i, j))
        return [[create(i, j) for j in range(self.__game.width)] for i in range(self.__game.height)]

    def __on_click(self, x, y):
        turn_status = self.__game.turn(x, y)
        if not turn_status:
            return
        self.__redraw()
        if self.__game.is_finished():
            messagebox.showinfo("15!", "You win!")
            self.__restart(True)

    def __redraw(self):
        for i, j in product(range(self.__game.height), range(self.__game.width)):
            tile = self.__tiles[i][j]
            value = self.__game[(i, j)]
            tile.configure(text=value)
            if value is None:
                tile.grid_forget()
            else:
                tile.grid(row=i, column=j, sticky=E+W+N+S)

    def __restart(self, victory):
        complexity = self.__game.complexity
        if victory:
            complexity *= 2
        else:
            complexity = max(complexity // 2, 1)
        self.__game.restart(complexity=complexity)
        self.__redraw()


if __name__ == '__main__':
    GameOfFifteenWidget(GameOfFifteen(4, 4, complexity=50), master=tk.Tk()).mainloop()
