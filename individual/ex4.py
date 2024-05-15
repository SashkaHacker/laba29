#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog


class FileEditor:
    def __init__(self, master):
        self.master = master
        master.title("Редактор файлов")

        self.entry_filename = tk.Entry(master, width=30)
        self.text_editor = tk.Text(master)
        self.button_open = tk.Button(
            master, text="Открыть", command=self.open_file
        )
        self.button_save = tk.Button(
            master, text="Сохранить", command=self.save_file
        )

        self.entry_filename.grid(row=0, column=0)
        self.button_open.grid(row=0, column=1)
        self.button_save.grid(row=0, column=2)
        self.text_editor.grid(row=1, column=0, columnspan=3)

    def open_file(self):
        filename = filedialog.askopenfilename(defaultextension=".txt")
        if filename:
            try:
                with open(filename, "r") as file:
                    text = file.read()
                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert("1.0", text)
                self.entry_filename.delete(0, tk.END)
                self.entry_filename.insert(0, filename)
            except FileNotFoundError:
                tk.messagebox.showerror("Ошибка", f"Файл не найден: {filename}")

    def save_file(self):
        filename = self.entry_filename.get()
        if filename:
            try:
                with open(filename, "w") as file:
                    text = self.text_editor.get("1.0", tk.END)
                    file.write(text)
            except FileNotFoundError:
                tk.messagebox.showerror("Ошибка", f"Файл не найден: {filename}")


if __name__ == "__main__":
    root = tk.Tk()
    file_editor = FileEditor(root)
    root.mainloop()
