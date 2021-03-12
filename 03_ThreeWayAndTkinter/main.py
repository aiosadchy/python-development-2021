import tkinter as tk
from tkinter import messagebox
from tkinter.constants import *
from functools import partial
from itertools import product


class GameOfFifteen:
    def __init__(self, height, width):
        self.__height = height
        self.__width = width
        self.__empty_cell_value = height * width
        self.__out_of_bounds = "out of bounds"
        self.__data = self.__generate_tiles()

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def restart(self):
        self.__data = self.__generate_tiles()

    def turn(self, x, y):
        offsets = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        values = [self[(i, j)] for i, j in offsets]
        index = values.index(None) if None in values else None
        if index is None:
            return False
        i, j = offsets[index]
        self.__data[x][y], self.__data[i][j] = self.__data[i][j], self.__data[x][y]
        return True

    def is_finished(self):
        for i, j in product(range(self.__height), range(self.__width)):
            if self.__target(i, j) != self.__data[i][j]:
                return False
        return True

    def __generate_tiles(self):
        return [[self.__target(i, j) for j in range(self.__width)] for i in range(self.__height)]

    def __target(self, i, j):
        return i * self.__width + j + 1

    def __getitem__(self, item):
        i, j = item
        if i < 0 or j < 0 or i >= self.__height or j >= self.__width:
            return self.__out_of_bounds
        result = self.__data[i][j]
        if result == self.__empty_cell_value:
            return None
        return result


class GameOfFifteenWidget(tk.Frame):
    def __init__(self, core, master=None):
        super().__init__(master)
        self.__core = core
        self.__master = master
        self.__top_panel = tk.Frame(self)
        self.__restart = tk.Button(self.__top_panel, text="New", command=self.__core.restart)
        self.__quit = tk.Button(self.__top_panel, text="Exit", command=self.__master.destroy)
        self.__game = tk.Frame(self)
        self.__tiles = self.__create_tiles()
        self.__pack_widgets()
        self.__redraw()

    def __pack_widgets(self):
        self.pack(expand=True, fill=BOTH)
        self.__top_panel.pack(side="top", expand=False, fill=X)
        self.__restart.pack(side="left")
        self.__quit.pack(side="right")
        self.__game.pack(side="bottom", expand=True, fill=BOTH)

        for i in range(self.__core.height):
            self.__game.rowconfigure(i, weight=1, uniform="cells")
        for j in range(self.__core.width):
            self.__game.columnconfigure(j, weight=1, uniform="cells")

    def __create_tiles(self):
        def create(i, j): return tk.Button(self.__game, command=partial(self.__on_click, i, j))
        return [[create(i, j) for j in range(self.__core.width)] for i in range(self.__core.height)]

    def __on_click(self, x, y):
        turn_status = self.__core.turn(x, y)
        if not turn_status:
            return
        self.__redraw()
        if self.__core.is_finished():
            messagebox.showinfo("15!", "You win!")
            self.__core.restart()

    def __redraw(self):
        for i, j in product(range(self.__core.height), range(self.__core.width)):
            tile = self.__tiles[i][j]
            value = self.__core[(i, j)]
            tile.configure(text=value)
            if value is None:
                tile.grid_forget()
            else:
                tile.grid(row=i, column=j, sticky=E+W+N+S)


if __name__ == '__main__':
    app = GameOfFifteenWidget(GameOfFifteen(3, 7), master=tk.Tk())
    app.mainloop()
