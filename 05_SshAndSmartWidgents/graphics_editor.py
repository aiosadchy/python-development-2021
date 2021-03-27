import tkinter as tk
import tkinter.colorchooser
from tkinter.constants import *


# tk.StringVar does not work for some reason, so I use this as a workaround
class Filename:
    def __init__(self, value, *labels):
        self.__value = value
        self.__labels = list(labels)
        self.__update_labels()

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value
        self.__update_labels()

    def __update_labels(self):
        for label in self.__labels:
            label.config(text=self.__value)


class GraphicsEditor(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)

        self.__text_frame = tk.LabelFrame(master=self)
        self.__text = tk.Text(master=self.__text_frame)

        self.__editor_frame = tk.Frame(master=self)
        self.__canvas = tk.Canvas(master=self.__editor_frame, height=512, width=512)
        self.__canvas.bind("<Button-1>", self.__on_click)
        self.__canvas.bind("<ButtonRelease-1>", self.__on_release)
        self.__canvas.bind("<Motion>", self.__on_drag)

        self.pack(expand=True, fill=BOTH)
        self.__text_frame.pack(side=LEFT, expand=True, fill=BOTH)
        self.__text.pack(expand=True, fill=BOTH)
        self.__editor_frame.pack(side=RIGHT, expand=True, fill=BOTH)
        self.__canvas.pack(expand=True, fill=BOTH)

        self.__filename = Filename("untitled.txt", self.__text_frame)
        self.__NEW = "new"
        self.__EDIT = "edit"
        self.__current_shape = None

        # FIXME
        # self.master.resizable(False, False)

    def __on_click(self, event):
        x0, y0, x1, y1 = event.x, event.y, event.x, event.y
        overlapping = self.__canvas.find_overlapping(x0, y0, x1, y1)
        if len(overlapping) == 0:
            shape = self.__canvas.create_oval(x0, y0, x1, y1)
            self.__current_shape = (self.__NEW, x0, y0, shape)
        else:
            self.__current_shape = (self.__EDIT, x0, y0, overlapping[-1])

    def __on_drag(self, event):
        if self.__current_shape is None:
            return
        x_event, y_event = event.x, event.y
        mode, x_origin, y_origin, shape = self.__current_shape
        if mode == self.__NEW:
            x0, y0, x1, y1 = self.__canvas.coords(shape)
            x1, y1 = x_event, y_event
            if x_event < x_origin:
                x0, x1 = x_event, x_origin
            if y_event < y_origin:
                y0, y1 = y_event, y_origin
            self.__canvas.coords(shape, x0, y0, x1, y1)
        else:
            self.__canvas.move(shape, x_event - x_origin, y_event - y_origin)
            self.__current_shape = (self.__EDIT, x_event, y_event, shape)

    def __on_release(self, _):
        self.__current_shape = None


if __name__ == "__main__":
    GraphicsEditor(master=tk.Tk()).mainloop()
