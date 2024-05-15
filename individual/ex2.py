#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk


class RainbowButtons:
    def __init__(self, master):
        self.master = master
        master.title("Цвета радуги")

        self.colors = {
            "Красный": "#ff0000",
            "Оранжевый": "#ff7d00",
            "Желтый": "#ffff00",
            "Зеленый": "#00ff00",
            "Голубой": "#007dff",
            "Синий": "#0000ff",
            "Фиолетовый": "#7d00ff",
        }

        self.label_color = tk.Label(master, text="Цвет:")
        self.entry_code = tk.Entry(master, width=10)
        self.label_name = tk.Label(master, text="")

        row = 1
        for name, code in self.colors.items():
            button = tk.Button(
                master,
                text=name,
                bg=code,
                command=lambda c=code, n=name: self.show_color(c, n),
            )
            button.grid(row=row, column=0)
            row += 1

        self.label_color.grid(row=0, column=0)
        self.entry_code.grid(row=0, column=1)
        self.label_name.grid(row=0, column=2)

    def show_color(self, code, name):
        self.entry_code.delete(0, tk.END)
        self.entry_code.insert(0, code)
        self.label_name.config(text=name)


if __name__ == "__main__":
    root = tk.Tk()
    rainbow_buttons = RainbowButtons(root)
    root.mainloop()
