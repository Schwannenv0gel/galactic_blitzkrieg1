img = QtGui.QImage('mendeleev.jpg')
img = img.scaled(141, 131, QtCore.Qt.KeepAspectRatio)
pixmap = QtGui.QPixmap(img)
self.mend_pic.setPixmap(pixmap)
self.mend_pic.setToolTip('Д. И. Менделеев')





        # Проверка корректности введённых значений
        sp_ = all_.split('\n')[:]
        if len(sp_) != 10:
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка!')
            msg.setText('Данные неправильно введены, вводите данные чётко по инструкции.')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            self.modify()
        if not isinstance(sp_[0], int) or not isinstance(sp_[1], str) or \
                not isinstance(sp_[2], str) or not isinstance(sp_[3], str):
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка!')
            msg.setText('Данные неправильно введены, вводите данные чётко по инструкции.')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            self.modify()
        if not isinstance(sp_[4], str) or not isinstance(sp_[5], float):
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка!')
            msg.setText('Данные неправильно введены, вводите данные чётко по инструкции.')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            self.modify()
        if not isinstance(sp_[6], float) or sp_[6] != '-' or not isinstance(sp_[6], int):
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка!')
            msg.setText('Данные неправильно введены, вводите данные чётко по инструкции.')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            self.modify()
        if not isinstance(sp_[7], float) or sp_[7] != '-' or not isinstance(sp_[7], int):
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка!')
            msg.setText('Данные неправильно введены, вводите данные чётко по инструкции.')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            self.modify()
        if not isinstance(sp_[8], int) or sp_[8] != '-':
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка!')
            msg.setText('Данные неправильно введены, вводите данные чётко по инструкции.')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            self.modify()
        if not isinstance(sp_[9], str) or sp_[9] != '-':
            msg = QMessageBox()
            msg.setWindowTitle('Ошибка!')
            msg.setText('Данные неправильно введены, вводите данные чётко по инструкции.')
            msg.setIcon(QMessageBox.Warning)
            msg.exec_()
            self.modify()
        # Конец проверки корректности





        # QMessageBox с информацией
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle('Внимание!')
        msg.setText('Вы находитесь в основном режиме поиска.')
        msg.setInformativeText('Если Вы хотите перейти в режим добавления элементов, нажмите Ctrl+Alt.' +
                               '\n\nНажмите OK, чтобы продолжить.')
        msg.exec_()

# Сообщение об ошибке
msg = QMessageBox()
msg.setWindowTitle('Ошибка!')
msg.setText('Данные неправильно введены, вводите данные чётко по инструкции.')
msg.setIcon(QMessageBox.Warning)
msg.exec_()
self.search()  # <-- Возвращение в начало функции
