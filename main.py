import os
import sys
import tkinter as tk
import threading

import keyboard
from pynput import mouse

mouse_button_state = (False, False, False)

class DragWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.overrideredirect(True)
        self.x = 0
        self.y = 0
        self.bind("<Button-1>", self.click)
        self.bind("<B1-Motion>", self.drag)
        self.bind("<ButtonRelease-1>", self.release)
        self.attributes("-transparent", "white")

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
        self.root.attributes('-alpha', 0.3)
        self.root.wm_attributes('-topmost', True)

        self.not_pan = True

        self._image = tk.PhotoImage(file=r'.\images\Exit.png').subsample(10)

        tk.Button(self.root, image=self._image, command=self.exit).place(x=109, y=1)

        self._img = tk.PhotoImage(file=r".\images\Mouse.png")
        self._img = self._img.subsample(6)

        self.mouse = tk.Label(self.root, image=self._img)
        self.mouse.place(x=26, y=15)

        self.keyboard = tk.Label(self.root, text='', font=('Console', 15))
        self.keyboard_text_color = 0
        self.keyboard_text, self.last_keyboard_text = '', ''
        self.keyboard.pack(side='bottom')

        def mouse_listener():
            def on_click(x, y, button, pressed):
                global mouse_button_state
                if button == mouse.Button.left:
                    mouse_button_state = (pressed, mouse_button_state[1], mouse_button_state[2])
                elif button == mouse.Button.middle:
                    mouse_button_state = (mouse_button_state[0], pressed, mouse_button_state[2])
                elif button == mouse.Button.right:
                    mouse_button_state = (mouse_button_state[0], mouse_button_state[1], pressed)

            # 创建鼠标监听器对象
            listener = mouse.Listener(on_click=on_click)
            listener.start()
            listener.join()

        # 启动鼠标监听线程
        mouse_thread = threading.Thread(target=mouse_listener)
        mouse_thread.daemon = True
        mouse_thread.start()

        keyboard.on_press(self.on_key)

    def run(self):
        while True:
            if self.keyboard_text != self.last_keyboard_text:
                self.keyboard.config(text=self.keyboard_text)
                self.last_keyboard_text = self.keyboard_text
            img = ''
            if mouse_button_state == (False, False, False):
                img = 'Mouse'
            elif mouse_button_state == (False, False, True):
                img = 'Right'
            elif mouse_button_state == (False, True, False):
                img = 'Middle'
            elif mouse_button_state == (False, True, True):
                img = 'Right-Middle'
            elif mouse_button_state == (True, False, False):
                img = 'Left'
            elif mouse_button_state == (True, False, True):
                img = 'Left-Right'
            elif mouse_button_state == (True, True, False):
                img = 'Left-Middle'
            elif mouse_button_state == (True, True, True):
                img = 'All'
            try:
                self._img = tk.PhotoImage(file=f".\\images\\{img}.png").subsample(6)
            except RuntimeError:
                os.system('cls')
                sys.exit()
            self.mouse.config(image=self._img)
            if self.keyboard_text_color < 255 and not self.not_pan:
                self.keyboard_text_color += 15
                c = hex(self.keyboard_text_color)[2:]
                if len(c) == 1:
                    c = '0' + c
                self.keyboard.config(fg=f"#{c}{c}{c}")
            if self.keyboard_text_color >= 255:
                self.keyboard.config(text='')
                self.not_pan = True

            self.root.update()

    def exit(self):
        self.root.destroy()
        sys.exit()

    def on_key(self, event):
        name:str = event.name.title()
        if name.upper() in list('ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
            name = 'Key ' + name
        elif name == 'Backspace':
            name = 'BackSpace'
        elif name == 'Left':
            name = '←'
        elif name == 'Right':
            name = '→'
        elif name == 'Up':
            name = '↑'
        elif name == 'Down':
            name = '↓'
        elif name == 'Shift':
            name == 'Left Shift'
        elif name == 'Ctrl':
            name == 'Left Ctrl'

        self.keyboard_text = name
        self.keyboard_text_color = 0
        self.not_pan = False


if __name__ == '__main__':
    app = Main()
    app.run()