import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QInputDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyMendUI import Ui_MainWindow
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


class InterTableMend(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Назначение кнопок
        self.search_button.clicked.connect(self.do_search)
        self.spravka_button.clicked.connect(self.spravka)

        # vvv Подключение к БД vvv
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName('MenTab.sqlite3')
        self.db.open()

        self.search()

    def keyPressEvent(self, event):
        if int(event.modifiers()) == (Qt.ControlModifier + Qt.AltModifier):
            self.modify()

        if int(event.modifiers()) == (Qt.ControlModifier + Qt.ShiftModifier):
            if event.key() == Qt.Key_B:
                self.search()

    def closeEvent(self, event):
        self.db.close()

    def showEvent(self, event):
        # print('show')
        pass

    # /|-----------[1]------------|\
    #  vvvv Функция добавления vvvv
    def modify(self):
        # Очистим текстовые поля, чтоб не отвлекали
        self.search_str.setText('')
        self.text_output.setPlainText('')

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Внимание!')
        msg.setText('Вы перешли в режим добавления элементов')
        msg.setInformativeText('Программа спросит у вас свойства одного элемента.' +
                               '\nЕсли хотите снова добавить элемент, то снова нажмите Ctrl+Alt.')
        msg.exec_()

        self.label.setText('Добавление')

        all_, ok = QInputDialog.getMultiLineText(self, 'Свойства нового элемента',
                                                 'Введите свойства по порядку:\n  порядковый номер\n  название' +
                                                 '\n  химический символ\n  латинское название\n  период, группа' +
                                                 '\n  атомная масса\n  температура плавления' +
                                                 '\n  температура кипения' +
                                                 '\n  год открытия\n  первооткрыватель' +
                                                 '\n\nЕсли свойства с 7 по 10 неизвестны, пишите "-".' +
                                                 '\n\nПишите без единиц измерения.')
        if not ok:
            self.modify()

        self.mod_sp = []

        try:
            self.mod_sp.append(int(all_.split('\n')[0]))
            self.mod_sp.append(all_.split('\n')[1])
            self.mod_sp.append(all_.split('\n')[2])
            self.mod_sp.append(all_.split('\n')[3])
            self.mod_sp.append(all_.split('\n')[4])
            self.mod_sp.append(float(all_.split('\n')[5]))

            if all_.split('\n')[6] == '-':
                self.mod_sp.append('-')
            else:
                self.mod_sp.append(float(all_.split('\n')[6]))

            if all_.split('\n')[7] == '-':
                self.mod_sp.append('-')
            else:
                self.mod_sp.append(float(all_.split('\n')[7]))

            if all_.split('\n')[8] == '-':
                self.mod_sp.append('-')
            else:
                self.mod_sp.append(int(all_.split('\n')[8]))

            self.mod_sp.append(all_.split('\n')[9])

        except Exception:
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка!')
            msg.setText('Данные неправильно введены, вводите данные чётко по инструкции.')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            self.modify()  # <-- Возвращение к началу функции добавления при какой-либо ошибке

        if len(self.mod_sp) != 10:
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка!')
            msg.setText('Данные неправильно введены, вводите данные чётко по инструкции.')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            self.modify()

        self.do_mod()

    def do_mod(self):
        # Сборка значений в список для отправки в БД
        sp = []
        for x in self.mod_sp:
            if x == '-':
                sp.append('NULL')
            elif isinstance(x, float) or isinstance(x, int):
                sp.append(str(x))
            elif isinstance(x, str):
                sp.append(f'"{x}"')

        # Добавление SQL-запросом
        query = QSqlQuery()
        query.exec(f'''INSERT INTO elements
        VALUES ({sp[0]}, {sp[1]}, {sp[2]}, {sp[3]}, {sp[4]}, {sp[5]}, {sp[6]}, {sp[7]}, {sp[8]}, {sp[9]})''')
        query.finish()

        self.db.commit()

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Элемент добавлен')
        msg.setText('Если хотите выйти из режима добавления, нажмите Ctrl+Shift+B.\nЕсли нет,— нажмите Ctrl+Alt.')
        msg.exec_()

    # /|---------[2]----------|\
    #  vvvv Функция поиска vvvv
    def search(self):
        # QMessageBox с информацией
        # msg = QMessageBox()
        # msg.setIcon(QMessageBox.Information)
        # msg.setWindowTitle('Внимание!')
        # msg.setText('Вы находитесь в основном режиме поиска.')
        # msg.setInformativeText('Если Вы хотите перейти в режим добавления элементов, нажмите Ctrl+Alt.' +
        #                        '\n\nНажмите OK, чтобы продолжить.')
        # msg.exec_()

        self.label.setText('Поиск:')  # <-- Чтобы при переходе из особого режима всё менялось обратно
        self.text_output.setPlainText('')

    def do_search(self):
        self.text_output.setPlainText('')
        self.label.setText('Поиск:')

        # Список параметров поиска
        params = ['Порядковый номер', 'Название элемента', 'Химический символ', 'Относительная атомная масса']

        # Узнаём, по какому параметру будет поиск
        parameter, ok_pressed = QInputDialog.getItem(
            self, 'Параметр поиска', 'Выберите параметр поиска', (params[0], params[1], params[2], params[3]), 0, False)

        # Возвращение к началу функции
        if not ok_pressed:
            self.search()

        search_ask = self.search_str.text()  # <-- Снимаем значение с нашего QLineEdit

        if search_ask == '':
            self.label.setText('Введите запрос')
        else:
            # Создание экземпляра QSqlQuery
            query = QSqlQuery()

            # vvv Выполнение SQL-запроса vvv
            if parameter == params[0]:
                query.exec(f'''SELECT * FROM elements
                WHERE id = {search_ask}''')

            elif parameter == params[1]:
                query.exec(f'''SELECT * FROM elements
                WHERE name = "{search_ask}"''')

            elif parameter == params[2]:
                query.exec(f'''SELECT * FROM elements
                WHERE symbol = "{search_ask}"''')

            elif parameter == params[3]:
                query.exec(f'''SELECT * FROM elements
                WHERE atom_mass = {search_ask}''')


        # Достаём значение из SQL-запроса
        query.first()
        ls = [query.value(i) for i in range(10)]  # <-- Список полученных значений

        # Обработка значений перед выводом
        lst_val = []
        for x in ls:
            if x == '':
                lst_val.append('неизвестно')
            else:
                lst_val.append(x)

        # vvv Выведение полученных данных на текстовое поле vvv
        txt = f'Порядковый номер:  {lst_val[0]}\n\nНазвание:  {lst_val[1]}' + \
              f'\n\nХимический символ:  {lst_val[2]}\n\nЛатинское название:  {lst_val[3]}' + \
              f'\n\nПериод и группа:  {lst_val[4]}\n\nОтносительная атомная масса:  {lst_val[5]} а. е. м.' + \
              f'\n\nТемпература плавления:  {lst_val[6]}\u00B0C\n\nТемпература кипения:  {lst_val[7]}\u00B0C' + \
              f'\n\nГод открытия:  {lst_val[8]}\n\nКто открыл:  {lst_val[9]}'
        self.text_output.setPlainText(txt)

    # /|----------[3]----------|\
    #  vvvv Функция справки vvvv
    def spravka(self):
        txt_main = 'В программе есть два режима: поиск химических элементов и их добавление.'

        txt_inf = '\nПри запуске программы сначала стоит режим поиска.' + \
                  '\n\nЧтобы найти элемент, введите запрос в верхнее текстовое поле,' + \
                  '\nзатем, нажав на кнопку поиска, выберите его тип.' + \
                  '\n\nЧтобы перейти в режим добавления, нажмите Ctrl+Alt.' + \
                  '\n\nЧтобы выйти из него нажмите Ctrl+Shift+B.' + \
                  '\n\nЕсли хотите выйти из программы, но не получается,' + \
                  '\nвоспользуйтесь диспетчером задач.' + \
                  '\n\nЕсли программа выводит None, значит данные введены неверно.' + \
                  '\n\nНажмите OK, чтобы продолжить.'

        txt_det = 'Автор: Пашков И. А.' + \
                  '\nДата выхода релизной версии: *это типа дата*' + \
                  '\nСсылка на исходники: *тут типа ссылка*' + \
                  '\n\nНе судите строго, это мой первый проект на Python))'

        # QMessageBox с информацией о программе
        msg = QMessageBox()
        msg.setWindowTitle('Справка')
        msg.setIcon(QMessageBox.Information)
        msg.setTextFormat(Qt.RichText)
        msg.setText(f'<b>{txt_main}</b>')
        msg.setInformativeText(txt_inf)
        msg.setDetailedText(txt_det)
        msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    itm = InterTableMend()
    itm.show()
    sys.exit(app.exec())
