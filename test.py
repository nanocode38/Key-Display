import tkinter as tk

class DragWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.attributes("-alpha", 0.5)
        self.wm_attributes("-topmost", True)
        self.x = 0
        self.y = 0
        self.bind("<Button-1>", self.click)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<ButtonRelease-1>", self.release)

        self.canvas = tk.Canvas(self, width=125, height=125, highlightthickness=0)
        self.canvas.pack()

    def click(self, event):
        self.x = event.x
        self.y = event.y

    def drag(self, event):
        new_x = self.winfo_x() + event.x - self.x
        new_y = self.winfo_y() + event.y - self.y
        self.geometry(f"+{new_x}+{new_y}")

    def release(self, event):
        pass

class Main(object):
    def __init__(self):
        self.root = DragWindow()
        self.root.geometry("125x125+880+450")

        self._img = tk.PhotoImage(file="images/Mouse.png").subsample(6)
        self.mouse = self.root.canvas.create_image(10, 10, anchor="nw", image=self._img)

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    app = Main()
    app.run()
