# !/usr/bin/python
# -*- coding: utf-8 -*-

# Создание приложения для отображения цены на 1 акцию Tesla Inc с датами, а так же котировок.
# Приложение создано для получения цены акции Tesla Inc в настоящем времени и проверка истории за текущий месяц.
# Так же можно отслеживать линию тренда Tesla Inc за текущий и предыдущий месяц -
# С условием наличия более 2х дней после начала месяца.

from PyQt5.Qt import *
import pyqtgraph as pg
import datetime
from data import price, price_last, month, days, Trend_price_last, Trend_days_last, Trend_price_lines, Trend_month


# Наследуемся от QWidget.
class Window(QWidget):
	def __init__(self):
		super().__init__()  # Вызываем метод супер класса.
		self.Geometry()  # Вызывает метод с необходимыми геометрическими установками.
		layout_v = QVBoxLayout(self)  # Создаем вертикальный макет.
		layout_h = QHBoxLayout(self)  # Создаем горизонтальный макет.
		self.view = view = pg.PlotWidget()  # Создаем графическое пространство.
		self.view_2 = pg.PlotWidget()  # Создаем графическое пространство.
		self.view.setLabels(left="Цена за 1 акцию ( В долларах )", bottom="Дата ( В днях )")  # Надпись над осями.
		self.curve = view.plot(name="Tesla Inc price")  # Создаем линию для цен Tesla Inc.
		self.curve2 = view.plot(name="Tesla Inc trend line")  # Создаем линию для линии тренда.

		# Создаем кнопку и присваеваем ей название.
		# Для цен.
		self.price_current_month = QPushButton("Вывести текущий месяц Tesla Inc. Вывести / Убрать линию тренда.")
		self.price_previous_month = QPushButton("Вывести предыдущий месяц Tesla Inc. Вывести / Убрать линию тренда.")

		# Надпись над графиком с выводом номера месяца.
		layout_v.addWidget(QLabel("Потоковый график TSLA.\t\t\t\t\t\tЗа: " + str(
			int(datetime.date.today().strftime('%m')) - 1) + ' - ' + str(
			int(datetime.date.today().strftime('%m'))) + '  Месяца.'))

		# Соединения кнопки и перенапровеления его в функцию.
		self.price_current_month.clicked.connect(lambda: self.Graph())
		self.price_previous_month.clicked.connect(lambda: self.Previous_month())

		layout_v.addWidget(self.view)  # Добавляем графическое пространство в графическое приложение.

		# Добавляем кнопку для вывода графика текущего - цен и линии тренда.
		layout_h.addWidget(self.price_current_month)
		layout_h.addWidget(self.price_previous_month)

		# Установка расположения кнопок.
		layout_v.addLayout(layout_h)
		self.setLayout(layout_v)

		# Подсказки к кнопкам, при наведении.
		self.price_current_month.setToolTip('Кнопка для вывода данных.')
		self.price_previous_month.setToolTip('Кнопка для вывода данных.\nЕсли она подчеркнута серым - не работает.')

	def Graph(self):
		# Проверка на наличие данных текущего месяца.
		if self.price_current_month.clicked.connect(lambda: self.Trend_line()) and len(price) < 3:
			# Если данных в проверке, оказалось меньше 3х, то на кнопке выводится сообщения для пользователя.
			# И кнопка блокируется.
			self.price_current_month.setText("Мало данных за месяц для вывода тренда.")
			self.price_current_month.setEnabled(False)

		# Убираем ненужное с наших данных.
		y_main = [float(i.replace(' ', '').replace(',', '.')) for i in price]
		x_main = [float(i.replace('', '').replace(',', '.')) for i in month]

		# Вставляем наши данные для создания граффика, и создаем ей специальные инициалы, шрифты, цвет.
		self.curve.setData(x=x_main, y=y_main, pen=pg.mkPen('#74a9f7', width=5), symbol='o', symbolPen='r')
		self.curve2.setData(pen=pg.mkPen('#w', width=-1), symbol='o')  # Устанавливаем для линии тренда ее специальный маневр:

		# При нажатии на эту функцию, линия тренда исчезает, при нажатии на вывод линии тренда она пояявляется.
		self.view.setXRange(x_main[0], x_main[len(x_main) - 1])  # Автоустановка маштаба по базе данным (Ось Х).
		self.view.setYRange(y_main[0], y_main[len(x_main) - 1])  # Автоустановка маштаба по базе данным (Ось Y).

		self.price_current_month.clicked.connect(lambda: self.Trend_line())  # При нажатии на кнопку, выводится линия тренда.

	def Trend_line(self):
		# Убираем ненужное с наших данных.
		y_line = [float(i.replace(' ', '').replace(',', '.')) for i in Trend_price_lines]
		x_line = [float(i.replace('', '').replace(',', '.')) for i in Trend_month]

		# Вставляем наши данные для создания граффика, и создаем ей специальные инициалы, шрифты, цвет.
		self.curve2.setData(x=x_line, y=y_line, pen=pg.mkPen('#r', width=3), symbol='x', symbolPen='g')

		# При нажатии на кнопку линия тренда удаляется.
		self.price_current_month.clicked.connect(lambda: self.Graph())

	def Previous_month(self):
		# Предыдущий месяц.
		self.price_current_month.setEnabled(True)

		# Убираем ненужное с наших данных.
		y_main = [float(i.replace(' ', '').replace(',', '.')) for i in price_last]
		x_main = [float(i.replace('', '').replace(',', '.')) for i in days]

		# Вставляем наши данные для создания граффика, и создаем ей специальные инициалы, шрифты, цвет.
		self.curve.setData(x=x_main, y=y_main, pen=pg.mkPen('#74a9f7', width=5), symbol='o', symbolPen='r')

		# Устанавливаем для линии тренда ее специальный маневр:
		self.curve2.setData(pen=pg.mkPen('#w', width=-1), symbol='o')

		# При нажатии на эту функцию, линия тренда исчезает, при нажатии на вывод линии тренда она пояявляется.
		self.view.setXRange(x_main[0], x_main[len(x_main) - 1])  # Автоустановка маштаба по базе данным (Ось Х).
		self.view.setYRange(y_main[0], y_main[len(x_main) - 1])  # Автоустановка маштаба по базе данным (Ось Y).

		# При нажатии на кнопку, выводится линия тренда.
		self.price_previous_month.clicked.connect(lambda: self.Trend_previous())

	def Trend_previous(self):
		# Предыдущий месяц линия тренда.
		# Убираем ненужное с наших данных.
		y_line = [float(i.replace(' ', '').replace(',', '.')) for i in Trend_price_last]
		x_line = [float(i.replace('', '').replace(',', '.')) for i in Trend_days_last]

		# Вставляем наши данные для создания граффика, и создаем ей специальные инициалы, шрифты, цвет.
		self.curve2.setData(x=x_line, y=y_line, pen=pg.mkPen('#r', width=3), symbol='x', symbolPen='g')

		# При нажатии на кнопку линия тренда удаляется.
		self.price_previous_month.clicked.connect(lambda: self.Previous_month())

	# Настройки окна, названия приложения, иконки, шрифта, и тд.
	def Geometry(self):
		self.setWindowTitle('Tesla Inc (TSLA)')  # Название приложения.
		self.setWindowIcon(QIcon('tesla_logo.png'))  # Испортируемая фотография.
		pg.setConfigOption('background', 'w')  # Установка цвета фона
		pg.setConfigOption('foreground', 'k')  # Установка шрифта текста.
		self.setFixedSize(800, 500)  # Функция блокировка изменения размера окна.
		self.move(1100, 125)  # Размещаем наше приложение по X и Y координате.


if __name__ == "__main__":
	# Создаем объект приложения в виде класса. Sys.argv - это список аргументов из командной строки.
	# Скрипты Python могут быть запущены из программной оболочки.
	# Это один из способов, как мы можем контролировать запуск наших скриптов.
	app = QApplication([])

	w = Window()  # Экрземпляр класса.
	w.show()  # отображает виджет на экране. Виджет сначала создаётся в памяти и позже показывается на экране.
	app.exec()  # Запуск цикла обработки событий.
