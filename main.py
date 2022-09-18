import sys
from decimal import *
from design import Ui_MainWindow
from PyQt5.QtWidgets import (QMainWindow, QApplication)
from operator import add, sub, mul, truediv


operations = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv
}


big_input_font = 40
memory_font = 18
buttons_font_size = 26


class Calc(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.setWindowTitle('Калькулятор')
        self.ui.setupUi(self)
        self.max_input_length = self.ui.big_input.maxLength()
        self.initUI()

    def initUI(self):
        self.ui.num_1.clicked.connect(lambda: self.add_num(1))
        self.ui.num_2.clicked.connect(lambda: self.add_num(2))
        self.ui.num_3.clicked.connect(lambda: self.add_num(3))
        self.ui.num_4.clicked.connect(lambda: self.add_num(4))
        self.ui.num_5.clicked.connect(lambda: self.add_num(5))
        self.ui.num_6.clicked.connect(lambda: self.add_num(6))
        self.ui.num_7.clicked.connect(lambda: self.add_num(7))
        self.ui.num_8.clicked.connect(lambda: self.add_num(8))
        self.ui.num_9.clicked.connect(lambda: self.add_num(9))
        self.ui.num_0.clicked.connect(lambda: self.add_num(0))
        self.ui.num_10.clicked.connect(self.set_negative)

        self.ui.c_button.clicked.connect(self.clean_all)
        self.ui.ce_button.clicked.connect(self.clean_input)

        self.ui.point.clicked.connect(self.add_point)

        self.ui.plus.clicked.connect(lambda: self.do_operation('+'))
        self.ui.minus.clicked.connect(lambda: self.do_operation('-'))
        self.ui.mult.clicked.connect(lambda: self.do_operation('*'))
        self.ui.div.clicked.connect(lambda: self.do_operation('/'))
        self.ui.equal.clicked.connect(self.calculate)

        self.ui.backspace.clicked.connect(self.backspace)

    def set_negative(self):
        self.clear_memory_if_eq()
        num = self.ui.big_input.text()
        if self.ui.big_input.maxLength() + 1 == len(num) and '-' in num:
            self.ui.big_input.setMaxLength(self.ui.big_input.maxLength() + 1)
        if '-' not in num:
            if num != '0':
                num = '-' + num
        else:
            num = num[1:]
        if self.max_input_length + 1 == len(num) and '-' in num:
            self.ui.big_input.setMaxLength(self.max_input_length + 1)
        else:
            self.ui.big_input.setMaxLength(self.max_input_length)
        self.ui.big_input.setText(num)
        self.adjust_big_input_font_size()

    def clear_memory_if_eq(self):
        if self.get_sign_from_memory() == '=':
            self.ui.label.setText('')
            self.adjust_memory_font_size()

    def add_num(self, value):
        self.clear_memory_if_eq()
        if self.ui.big_input.text() == '0':
            self.ui.big_input.setText(str(value))
            self.adjust_big_input_font_size()
            return
        self.ui.big_input.setText(self.ui.big_input.text() + str(value))
        self.adjust_big_input_font_size()

    def clean_all(self):
        self.clear_memory_if_eq()
        self.ui.big_input.setText('0')
        self.adjust_big_input_font_size()
        self.ui.label.clear()

    def clean_input(self):
        self.ui.big_input.setText('0')
        self.adjust_big_input_font_size()

    def add_point(self):
        self.clear_memory_if_eq()
        if '.' not in self.ui.big_input.text():
            self.ui.big_input.setText(self.ui.big_input.text() + '.')
            self.adjust_big_input_font_size()

    def add_memory(self, to_do):
        if not self.ui.label.text() or self.get_sign_from_memory() == '=':
            self.ui.label.setText(self.remove_zeros(self.ui.big_input.text()) + f" {to_do}")
            self.ui.big_input.setText('0')
            self.adjust_big_input_font_size()
            self.adjust_memory_font_size()

    @staticmethod
    def remove_zeros(num):
        num = str(float(num))
        if num[-2::] == '.0':
            return num[0:-2]
        return num

    def get_num_from_input(self):
        num = self.ui.big_input.text().strip('.')
        if '.' in num:
            return float(num)
        return int(num)

    def get_num_from_memory(self):
        if self.ui.label.text():
            num = self.ui.label.text().strip('.').split()[0]
            if '.' in num:
                return float(num)
            return int(num)

    def get_sign_from_memory(self):
        if self.ui.label.text():
            return self.ui.label.text().strip('.').split()[-1]

    def calculate(self):
        memory = self.ui.label.text()
        new_num = self.ui.big_input.text()

        if memory:
            try:
                result = self.remove_zeros(

                    str(operations[self.get_sign_from_memory()](Decimal(self.get_num_from_memory()),
                                                                Decimal(self.get_num_from_input())))
                )
                self.ui.label.setText(memory + " " + self.remove_zeros(new_num) + ' =')
                self.adjust_memory_font_size()
                self.ui.big_input.setText(result)
                self.adjust_big_input_font_size()
                return result
            except Exception:
                pass

    def do_operation(self, sign):
        memory = self.ui.label.text()
        try:
            if not memory:
                self.add_memory(sign)
            else:
                memory_sign = self.get_sign_from_memory()
                if memory_sign != sign:
                    if memory_sign == '=':
                        self.add_memory(sign)
                    else:
                        self.ui.label.setText(memory[0:-1] + sign)
                else:
                    self.ui.label.setText(self.calculate() + ' ' + sign)
        except Exception:
            pass
        self.adjust_memory_font_size()

    def backspace(self):
        self.clear_memory_if_eq()
        current_num = self.ui.big_input.text()

        if len(current_num) == 1:
            self.ui.big_input.setText('0')
        elif len(current_num) == 2 and current_num[0] == '-':
            self.ui.big_input.setText('0')
        else:
            self.ui.big_input.setText(current_num[0:-1])
        self.adjust_big_input_font_size()

    def get_big_input_width(self):
        return self.ui.big_input.fontMetrics().boundingRect(self.ui.big_input.text()).width()

    def get_memory_width(self):
        return self.ui.label.fontMetrics().boundingRect(self.ui.label.text()).width()

    def adjust_big_input_font_size(self):
        size = big_input_font
        while self.get_big_input_width() > self.ui.big_input.width() - 15:
            size -= 1
            self.ui.big_input.setStyleSheet("color: rgb(236, 236, 236); font-size: {}pt;".format(size))

        size = 1
        while self.get_big_input_width() < self.ui.big_input.width() - 60:
            size += 1
            if size > 40:
                break
            self.ui.big_input.setStyleSheet("color: rgb(236, 236, 236); font-size: {}pt;".format(size))

    def adjust_memory_font_size(self):
        size = memory_font
        while self.get_memory_width() > self.ui.label.width() - 15:
            size -= 1
            self.ui.label.setStyleSheet("color: #888; font-size: {}pt;".format(size))

        size = 1
        while self.get_memory_width() < self.ui.label.width() - 60:
            size += 1
            if size > 18:
                break
            self.ui.label.setStyleSheet("color: #888; font-size: {}pt;".format(size))

    def resizeEvent(self, event) -> None:
        self.adjust_big_input_font_size()
        self.adjust_memory_font_size()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = Calc()
    calc.show()
    sys.exit(app.exec())
