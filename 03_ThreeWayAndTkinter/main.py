import tkinter as tk
from tkinter.constants import *
from functools import partial


class GameOfFifteen:
    def __init__(self, height, width):
        self.__height = height
        self.__width = width
        self.__data = self.__generate_tiles()

    @property
    def width(self):
        return self.__width

    @property
    def height(self):
        return self.__height

    def __generate_tiles(self):
        result = [[None for _ in range(self.__width)] for _ in range(self.__height)]
        current_value = 1
        for i in range(self.__height):
            for j in range(self.__width):
                result[i][j] = current_value
                current_value += 1
        return result

    def __getitem__(self, item):
        i, j = item
        result = self.__data[i][j]
        if result == self.__width * self.__height:
            return None
        return result


class GameOfFifteenWidget(tk.Frame):
    def __init__(self, core, master=None):
        super().__init__(master)
        self.__core = core
        self.__master = master
        self.__top_panel = tk.Frame(self)
        self.__restart = tk.Button(self.__top_panel, text="restart", command=self.__restart)
        self.__quit = tk.Button(self.__top_panel, text="quit", command=self.__master.destroy)
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
            self.__game.rowconfigure(i, weight=1)
        for j in range(self.__core.width):
            self.__game.columnconfigure(j, weight=1)

        for i in range(self.__core.height):
            for j in range(self.__core.width):
                tile = self.__tiles[i][j]
                tile.grid(row=i, column=j, sticky=E+W+N+S)

    def __create_tiles(self):
        return [
            [
                tk.Button(self.__game, command=partial(self.__on_click, i, j))
                for j in range(self.__core.width)
            ]
            for i in range(self.__core.height)
        ]

    def __on_click(self, x, y):
        self.__redraw()

    def __redraw(self):
        for i in range(self.__core.height):
            for j in range(self.__core.width):
                tile = self.__tiles[i][j]
                text = self.__core[(i, j)]
                tile.configure(text=text)

    def __restart(self):
        self.__core = GameOfFifteen(self.__core.height, self.__core.width)


if __name__ == '__main__':
    app = GameOfFifteenWidget(GameOfFifteen(4, 4), master=tk.Tk())
    app.mainloop()
