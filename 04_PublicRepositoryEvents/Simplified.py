import tkinter as tk
from functools import partial
from tkinter.messagebox import showinfo
from tkinter.constants import *
import re


def parse_geometry(geometry):
    groups = re.match(
        r"(?P<row>\d+)"
        r"(\.(?P<row_weight>\d+))?"
        r"(\+(?P<height>\d+))?"
        r":"
        r"(?P<col>\d+)"
        r"(\.(?P<col_weight>\d+))?"
        r"(\+(?P<width>\d+))?"
        r"(/(?P<gravity>[NEWS]+))?",
        geometry
    ).groupdict()
    names = [
        ("row",         int,   None),
        ("row_weight",  int,      1),
        ("height",      int,      0),
        ("col",         int,   None),
        ("col_weight",  int,      1),
        ("width",       int,      0),
        ("gravity",     str, "NEWS")
    ]
    return ((c(groups[g]) if groups[g] is not None else d) for g, c, d in names)


class Application(tk.Frame):
    def __init__(self, title):
        super().__init__()
        self.pack(expand=True, fill=BOTH)
        self.createWidgets()
        self.winfo_toplevel().title(title)

    def __getattr__(self, item):
        return partial(self.__construct, self, item)

    @staticmethod
    def __construct(parent, name, widget_type, geometry, **kwargs):
        class ChildWidget(widget_type):
            def __init__(self, constructor, geometry, *args, **kwargs):
                super(ChildWidget, self).__init__(*args, **kwargs)
                self.__construct = constructor

                row, row_weight, height, col, col_weight, width, gravity = parse_geometry(geometry)
                self.grid(
                    row=row,
                    rowspan=(height + 1),
                    column=col,
                    columnspan=(width + 1),
                    sticky=gravity
                )
                self.master.rowconfigure(row, weight=row_weight)
                self.master.columnconfigure(col, weight=col_weight)

            def __getattr__(self, item):
                return partial(self.__construct, self, item)

        setattr(parent, name, ChildWidget(parent.__construct, geometry, master=parent, **kwargs))
        return getattr(parent, name)

    def createWidgets(self):
        pass


class App(Application):
    def createWidgets(self):
        self.message = "Congratulations!\nYou've found a sercet level!"
        self.F1(tk.LabelFrame, "1:0", text="Frame 1")
        self.F1.B1(tk.Button, "0:0/NW", text="1")
        self.F1.B2(tk.Button, "0:1/NE", text="2")
        self.F1.B3(tk.Button, "1:0+1/SEW", text="3")
        self.F2(tk.LabelFrame, "1:1", text="Frame 2")
        self.F2.B1(tk.Button, "0:0/N", text="4")
        self.F2.B2(tk.Button, "0+1:1/SEN", text="5")
        self.F2.B3(tk.Button, "1:0/S", text="6")
        self.Q(tk.Button, "2.0:1.2/SE", text="Quit", command=self.quit)
        self.F1.B3.bind("<Any-Key>", lambda event: showinfo(self.message.split()[0], self.message))


if __name__ == '__main__':
    app = App(title="Sample application")
    t = app.asd
    app.mainloop()
