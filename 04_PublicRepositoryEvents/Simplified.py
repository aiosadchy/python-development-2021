import tkinter as tk
from tkinter.messagebox import showinfo
from functools import partial


class Application(tk.Frame):
    def __init__(self, title):
        super().__init__()
        self.createWidgets()
        self.winfo_toplevel().title(title)

    def __getattr__(self, item):
        return partial(self.__construct, self, item)

    @staticmethod
    def __construct(parent, name, widget_type, geometry, **kwargs):
        constructor = parent.__construct

        class ChildWidget(widget_type):
            def __getattr__(self, item):
                return partial(constructor, self, item)

        print(widget_type, geometry, kwargs)
        result = ChildWidget(parent.master, **kwargs)
        setattr(parent, name, result)
        return result

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
