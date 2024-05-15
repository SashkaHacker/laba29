#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import os
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from typing import List

from validation import WorkerValidation


@dataclass
class Worker:
    surname: str
    name: str
    phone: str
    date: List


@dataclass
class Staff:
    workers: List[Worker] = field(default_factory=lambda: [])

    def add_worker(self, surname, name, phone, date):
        self.workers.append(
            Worker(
                surname=surname, name=name, phone=phone, date=date.split(":")
            )
        )

    def phone(self, numbers_phone: int):
        fl = True
        for i in self.workers:
            if i.phone == numbers_phone:
                print(
                    f"Фамилия: {i.surname}\n"
                    f"Имя: {i.name}\n"
                    f"Номер телефона: {i.phone}\n"
                    f"Дата рождения: {':'.join(i.date)}"
                )
                fl = False
                break
        if fl:
            print("Человека с таким номером телефона нет в списке.")

    def save_workers(self, filename: str):
        root = ET.Element("workers")
        for worker in self.workers:
            worker_element = ET.Element("worker")
            name_element = ET.SubElement(worker_element, "name")
            name_element.text = worker.name
            post_element = ET.SubElement(worker_element, "surname")
            post_element.text = worker.surname
            year_element = ET.SubElement(worker_element, "phone")
            year_element.text = str(worker.phone)

            # Сохраняем дату как отдельные элементы
            date_element = ET.SubElement(worker_element, "date")
            for date_part in worker.date:
                part_element = ET.SubElement(date_element, "part")
                part_element.text = date_part

            root.append(worker_element)
        tree = ET.ElementTree(root)
        with open(filename, "wb") as fout:
            tree.write(fout, encoding="utf8", xml_declaration=True)

    def load_workers(self, filename: str):
        with open(filename, "r", encoding="utf8") as fin:
            xml = fin.read()
        parser = ET.XMLParser(encoding="utf8")
        tree = ET.fromstring(xml, parser=parser)
        self.workers = []
        for worker_element in tree:
            name, date, surname, phone = None, [], None, None
            for element in worker_element:
                if element.tag == "name":
                    name = element.text
                elif element.tag == "surname":
                    surname = element.text
                elif element.tag == "phone":
                    phone = element.text
                elif element.tag == "date":
                    for part_element in element:
                        date.append(part_element.text)
                if (
                    name is not None
                    and date
                    and surname is not None
                    and phone is not None
                ):
                    self.workers.append(
                        Worker(
                            surname=surname, name=name, phone=phone, date=date
                        )
                    )
        try:
            for i in self.workers:
                WorkerValidation(
                    surname=i.surname, name=i.name, phone=i.phone, date=i.date
                )
            self.workers.sort(
                key=lambda x: datetime.strptime("-".join(x.date), "%d-%m-%Y")
            )
        except Exception:
            self.workers = []
            print("Invalid JSON")

    def __str__(self):
        """
        Отобразить список работников.
        """
        # Проверить, что список работников не пуст.
        lst = []
        if self.workers:
            # Блок заголовка таблицы
            line = "+-{}-+-{}-+-{}-+-{}-+-{}-+".format(
                "-" * 4, "-" * 30, "-" * 20, "-" * 15, "-" * 15
            )
            lst.append(line)
            lst.append(
                f'| {"№":^4} | {"Фамилия":^30} | {"Имя":^20} | '
                f'{"Номер телефона":^15} | {"Дата рождения":^15} |'
            )

            lst.append(line)

            # Вывести данные о всех сотрудниках.
            for idx, worker in enumerate(self.workers, 1):
                lst.append(
                    f"| {idx:>4} | {worker.surname:<30} | "
                    f"{worker.name:<20}"
                    f" | {worker.phone:>15}"
                    f' | {":".join(worker.date):>15} |'
                )

            lst.append(line)
            return "\n".join(lst)
        return "Список работников пуст."


def main(command_line=None):
    staff = Staff()  # Создать экземпляр класса Staff.

    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename", action="store", help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser(description="workers")
    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления работника.
    add = subparsers.add_parser(
        "add", parents=[file_parser], help="Add a new worker"
    )
    add.add_argument(
        "-n", "--name", action="store", required=True, help="Имя работника"
    )
    add.add_argument(
        "-s", "--surname", action="store", help="Фамилия работника"
    )
    add.add_argument(
        "-p",
        "--phone",
        action="store",
        required=True,
        help="Номер телефона работника",
    )
    add.add_argument(
        "-d",
        "--date",
        action="store",
        required=True,
        help="Дата в формате: (число:месяц:год)",
    )

    # Создать субпарсер для отображения всех работников.
    _ = subparsers.add_parser(
        "display", parents=[file_parser], help="Display all workers"
    )

    # Добавление субпарсера для выбора работника по номеру телефона.
    select_phone = subparsers.add_parser(
        "select", parents=[file_parser], help="Select worker by phone"
    )
    select_phone.add_argument("-p", "--phone", action="store", required=True)

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить всех работников из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        with open(args.filename, "r", encoding="utf8") as fin:
            if len(fin.readlines()) > 0:
                staff.load_workers(args.filename)

    # Добавить работника.
    match args.command:
        case "add":
            staff.add_worker(args.surname, args.name, args.phone, args.date)
            is_dirty = True
        case "display":
            print(staff)
        case "select":
            staff.phone(args.phone)

    # Сохранить данные в файл, если список работников был изменен.
    if is_dirty:
        staff.save_workers(args.filename)


if __name__ == "__main__":
    main()
