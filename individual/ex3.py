#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk


class ColorPicker:
    def __init__(self, master):
        self.master = master
        master.title("Выбор цвета")

        self.red_var = tk.IntVar(value=0)
        self.green_var = tk.IntVar(value=0)
        self.blue_var = tk.IntVar(value=0)

        self.label_color = tk.Label(master, text="Цвет:", width=10)
        self.label_show = tk.Label(master, bg="#000000", width=10)

        self.create_radio_group("Красный", self.red_var, 0, 1)
        self.create_radio_group("Зеленый", self.green_var, 2, 3)
        self.create_radio_group("Синий", self.blue_var, 4, 5)

        self.label_color.grid(row=0, column=0)
        self.label_show.grid(row=0, column=1)

    def create_radio_group(self, color_name, var, row1, row2):
        tk.Radiobutton(
            self.master,
            text="0",
            variable=var,
            value=0,
            command=self.update_color,
        ).grid(row=row1, column=0)
        tk.Radiobutton(
            self.master,
            text="255",
            variable=var,
            value=255,
            command=self.update_color,
        ).grid(row=row2, column=0)
        tk.Label(self.master, text=color_name).grid(
            row=row1, column=1, rowspan=2
        )

    def update_color(self):
        red = self.red_var.get()
        green = self.green_var.get()
        blue = self.blue_var.get()
        color_code = f"#{red:02x}{green:02x}{blue:02x}"
        self.label_show.config(bg=color_code)


if __name__ == "__main__":
    root = tk.Tk()
    color_picker = ColorPicker(root)
    root.mainloop()
