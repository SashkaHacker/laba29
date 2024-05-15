#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk


class Calculator:
    def __init__(self, master):
        self.master = master
        master.title("Калькулятор")

        self.entry1 = tk.Entry(master, width=10)
        self.entry2 = tk.Entry(master, width=10)
        self.label = tk.Label(master, text="Результат:")

        self.button_add = tk.Button(master, text="+", command=self.add)
        self.button_sub = tk.Button(master, text="-", command=self.sub)
        self.button_mul = tk.Button(master, text="*", command=self.mul)
        self.button_div = tk.Button(master, text="/", command=self.div)

        self.entry1.grid(row=0, column=0)
        self.entry2.grid(row=0, column=1)
        self.label.grid(row=1, column=0, columnspan=2)
        self.button_add.grid(row=2, column=0)
        self.button_sub.grid(row=2, column=1)
        self.button_mul.grid(row=3, column=0)
        self.button_div.grid(row=3, column=1)

    def add(self):
        self.calculate("+")

    def sub(self):
        self.calculate("-")

    def mul(self):
        self.calculate("*")

    def div(self):
        self.calculate("/")

    def calculate(self, operation):
        try:
            num1 = float(self.entry1.get())
            num2 = float(self.entry2.get())
            match operation:
                case "+":
                    result = num1 + num2
                case "-":
                    result = num1 - num2
                case "*":
                    result = num1 * num2
                case "/":
                    if num2 == 0:
                        result = "Ошибка: деление на ноль"
                    else:
                        result = num1 / num2
            self.label.config(text=f"Результат: {result}")

        except ValueError:
            self.label.config(text="Ошибка: неверный ввод")


if __name__ == "__main__":
    root = tk.Tk()
    calculator = Calculator(root)
    root.mainloop()
