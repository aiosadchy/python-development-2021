import re
import tkinter as tk
import tkinter.colorchooser
from tkinter.constants import *


object_description = re.compile(
    r"^"                                            r"[\s]*"
    r"(?P<type>oval)"                               r"[\s]*"
    r"<"                                            r"[\s]*"
    r"(?P<x0>[+\-]?(\d+|\d+\.\d+))"                 r"[\s]+"
    r"(?P<y0>[+\-]?(\d+|\d+\.\d+))"                 r"[\s]+"
    r"(?P<x1>[+\-]?(\d+|\d+\.\d+))"                 r"[\s]+"
    r"(?P<y1>[+\-]?(\d+|\d+\.\d+))"                 r"[\s]*"
    r">"                                            r"[\s]*"
    r"(?P<outline_thickness>[+\-]?(\d+|\d+\.\d+))"  r"[\s]+"
    r"(?P<outline_color>#?\w+)"                     r"[\s]+"
    r"(?P<fill_color>#?\w+)"                        r"[\s]*"
    r"$"
)


class GraphicsEditor(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master=master)

        self.__text_frame = tk.LabelFrame(master=self)
        self.__text = tk.Text(master=self.__text_frame, undo=True)
        self.__text.bind("<<Modified>>", self.__update_canvas)

        self.__editor_frame = tk.Frame(master=self)
        self.__control_panel = tk.Frame(master=self.__editor_frame)
        self.__fill_color_button = tk.Button(
            master=self.__control_panel,
            text="Fill color",
            command=self.__pick_fill_color
        )
        self.__outline_color_button = tk.Button(
            master=self.__control_panel,
            text="Outline color",
            command=self.__pick_outline_color
        )
        self.__canvas = tk.Canvas(master=self.__editor_frame, height=512, width=512)
        self.__canvas.bind("<Button-1>", self.__on_click)
        self.__canvas.bind("<ButtonRelease-1>", self.__on_release)
        self.__canvas.bind("<Motion>", self.__on_drag)

        self.pack(expand=True, fill=BOTH)
        self.__text_frame.pack(side=LEFT, expand=True, fill=BOTH)
        self.__text.pack(expand=True, fill=BOTH)
        self.__editor_frame.pack(side=RIGHT, expand=True, fill=BOTH)
        self.__control_panel.pack(side=TOP, expand=True, fill=X)
        self.__fill_color_button.pack(side=LEFT, expand=False)
        self.__outline_color_button.pack(side=LEFT, expand=False)
        self.__canvas.pack(expand=True, fill=BOTH)

        self.__NEW = "new"
        self.__EDIT = "edit"
        self.__current_shape = None

        self.__TAG_INCORRECT = "incorrect"
        self.__text.tag_config(self.__TAG_INCORRECT, background="red")

        self.__fill_color = "white"
        self.__outline_color = "black"

    def __on_click(self, event):
        x0, y0, x1, y1 = event.x, event.y, event.x, event.y
        overlapping = self.__canvas.find_overlapping(x0, y0, x1, y1)
        if len(overlapping) == 0:
            shape = self.__canvas.create_oval(
                x0, y0, x1, y1,
                fill=self.__fill_color,
                outline=self.__outline_color
            )
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
        self.__update_text()

    def __pick_fill_color(self):
        self.__fill_color = tk.colorchooser.askcolor(color=self.__fill_color)[-1]

    def __pick_outline_color(self):
        self.__outline_color = tk.colorchooser.askcolor(color=self.__outline_color)[-1]

    def __update_text(self):
        old_text = self.__text.get("1.0", END).split("\n")
        incorrect_lines = [
            line for line in old_text
            if object_description.match(line) is None and line != ""
        ]
        new_shapes = [self.__serialize(o) for o in self.__canvas.find_all()]
        new_text = "\n".join(new_shapes + incorrect_lines)
        self.__text.delete("1.0", END)
        self.__text.insert("1.0", new_text)
        self.__mark_incorrect_lines()

    def __update_canvas(self, _):
        self.__canvas.delete(ALL)
        text = self.__text.get("1.0", END).split("\n")
        for line in text:
            self.__deserialize(line)
        self.__mark_incorrect_lines()
        self.__text.edit_modified(False)

    def __serialize(self, shape):
        shape_type = self.__canvas.type(shape)
        x0, y0, x1, y1 = self.__canvas.coords(shape)
        outline_thickness = self.__canvas.itemcget(shape, "width")
        outline_color = self.__canvas.itemcget(shape, "outline")
        fill_color = self.__canvas.itemcget(shape, "fill")
        return f"{shape_type} "             \
               f"<{x0} {y0} {x1} {y1}> "    \
               f"{outline_thickness} "      \
               f"{outline_color} "          \
               f"{fill_color}"

    def __deserialize(self, line):
        match = object_description.match(line)
        if match is None:
            return
        attributes = match.groupdict()

        for color in ["fill_color", "outline_color"]:
            try:
                self.winfo_rgb(attributes[color])
            except tk.TclError:
                attributes[color] = "black"

        getattr(self.__canvas, f"create_{attributes['type']}")(
            attributes["x0"], attributes["y0"], attributes["x1"], attributes["y1"],
            width=attributes["outline_thickness"],
            outline=attributes["outline_color"],
            fill=attributes["fill_color"]
        )

    def __mark_incorrect_lines(self):
        self.__text.tag_remove(self.__TAG_INCORRECT, "1.0", END)
        text = enumerate(self.__text.get("1.0", END).split("\n"))
        incorrect_lines = [
            i + 1 for i, line in text
            if object_description.match(line) is None and line != ""
        ]
        for i in incorrect_lines:
            self.__text.tag_add(self.__TAG_INCORRECT, f"{i}.0", f"{i}.end")


if __name__ == "__main__":
    GraphicsEditor(master=tk.Tk()).mainloop()
