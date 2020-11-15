# !/usr/bin/python
# -*- coding: utf-8 -*-

# Файл для добычи информации:
# Парсинг сайта investing.com и преобразования ее в конечный продукт - цена за 1 акцию Tesla Inc.

# Так же работа с базой данных в виде csv файла, обновления данных при запуске программы.

# Программа имеет 2 вида работы:
# 1) Если интернет подключен к устройству запуска скрипта, то он берет новейшие данные из сайта.
# 2) Иначе, если подключения не имеется, то берутся данные, заранее записанные в базу данных.

# Данная программа имеет практичное решение в том, что -
# Не имея в определенный момент контакта с интернетом, она будет работать и без него.


import requests
from bs4 import BeautifulSoup
import csv
import subprocess
import os
import datetime

internet = False  # False True

while not internet:
	try:
		subprocess.check_call(["ping", "www.google.ru"])
		internet = True
	except subprocess.CalledProcessError:
		pass
	break


# Если нет интернета, берутся старые данные из базы данных (Старые настолько, насколько давно не запускали программу.
def No_internet_only_database(data_of, price_of):
	with open("Tesla_data.csv", mode="r", encoding='utf-8') as file:
		read = csv.DictReader(file, delimiter=";", lineterminator="\r")  # linet - разделитель между строками таблицы.
		for content in read:
			data_of.append(content['Data'])
			price_of.append(content['Price'])
	return data_of, price_of


# Если устройство подключено к сети Интернет.
def Internet_on(data_of, price_of):
	# Сайт с которого парсим данные.
	url = 'https://ru.investing.com/equities/tesla-motors-historical-data'

	# Имя браузера, что бы сервер думал что это человек
	head = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
						  'Chrome/83.0.4103.116 Safari/537.36'}

	# Начинаем парсить данные с сайта.
	full_page = requests.get(url, headers=head)
	soup = BeautifulSoup(full_page.content, 'html.parser')
	convert_price = soup.findAll('td', {'class': ('redFont', 'greenFont')}, limit=50)
	convert_days = soup.findAll('td', {'class': "first left bold noWrap"})

	# Обрабатываем нужные нам данные.
	convert_price = [x.text for x in convert_price]
	data_of.append([y.text for y in convert_days])

	# Игнорируем ненужные нам данные, добавляя, нужные.
	price_of.append([x for x in convert_price if (x[0] != '+' and x[0] != '-' and x[0] != 1 and x[-1] != '%')])

	return data_of, price_of


# Функция для обработки данных за предыдущий месяц.
# Работает при помощи базы данных, дабы использовать их данные в график.
# Это сделано по причине, что сайт для парсинга, размещает данными ровно за 22 рабочих дня.
# Но данная программа расчитана на вывод новых и более поздних данных.
# Т.к. она настроена на постройку графиков полного предыдущего месяца.
def Gives_data(may, pri_lasts):
	dt = []  # Переменная для записи дат.
	prc = []  # Переменная для записи денег.

	No_internet_only_database(dt, prc)  # Вызов функции для быстрого получения данных.

	for muster in range(len(dt)):
		if int(dt[muster][3:5]) == int(dt[-1][3:5]) - 1:
			may.append(dt[muster][:2])  # Добавляем в переменную предыдущие данные всех месяцев (Даты).
			pri_lasts.append(prc[muster][:3])  # Добавляем в переменную предыдущие данные всех месяцев (Цены).

	return may, pri_lasts


# Функция для округления не целый чисел.
# Скрипт работает только на точных данный, и не принимает остатки.
# И дальше передает их в програму для вывода в график.
def rounding(lists, news):
	for gut in lists:
		if len(gut) >= 3:
			news.append(gut[:3])


# Инициализируем переменные для дальнейшей работы с ними.
data = []  # Список хранящий данные (Даты).
prices = []  # Список хранящий данных (Цены).
price = []

# Проверка на подключение к сети Интернет, т.к. скрипт обладает 2мя разными методами выполнения.
if internet:
	Internet_on(data, prices)
	prices = (prices[0])[::-1]  # Переворачиваем данные, для удобной работы.
	rounding(prices, price)
	data = (data[0])[::-1]  # Переворачиваем данные, для удобной работы.
else:
	No_internet_only_database(data, price)

del prices  # Удаляем ненужные переменные.

helper = data[:]  # Помошник для прохода функции по всем имеющимся данным (Даты).
price_last = []  # Переменная для хранения данных прошлого месяца (Цены).
month = []  # Переменная для хранения данных текущего месяца (Даты).
data = len(data) + 1  # Увеличиваем переменную для шага в дальнейшем цикле (Показывает кол-во дней текущего месяца).
fo = []  # Список для записи количества лишних данных (за 2+ месяца до).
by = []  # Пееременная для записи дат текущего месяца.

# Делим даты по месяцам.
for index in range(len(helper)):
	#  Проверяем текущий месяц с предыдущим, для их разделения.
	if int(helper[index][3:5]) == int(helper[-1][3:5]):
		month.append(helper[index][:2])
		by.append(helper[index])
		data -= 1
		fo.append(index)

# Текущие тренды акции.
price = price[fo[0]:]  # Делаем срез для удаления данных о предыдущем месяце.
Trend_price_line = [price[0], price[len(price) - 1]]  # Создаем линию тренда, и устонавливаем в него данные (Цены).
Trend_month = [month[0][:2], month[len(month) - 1][:2]]  # Создаем линию тренда, и устонавливаем в него данные (Даты).

del data, fo  # Удаляем ненужные нам переменные.

# Отсюда пишем код который берет из базы данных последний месяц.

days = []  # Переменная для хранения данных о предыдущим месяце (Даты).
price_last = []  # Переменная для хранения данных о предыдущим месяце (Цены).

Gives_data(days, price_last)

# Создаем линию тренда, и устонавливаем в него данные.
Trend_price_last = [price_last[0], price_last[len(price_last) - 1]]  # Цены.
Trend_days_last = [days[0][:2], days[len(days) - 1][:2]]  # Даты.

helper = price[:]  # Переменная-помошник, для прохода по всем данным в price.
price = []  # Пересоздаем переменную для записи в ней нужные нам данные.

rounding(helper, price)

Trend_price_lines = Trend_price_line[:]  # Переменная-помошник, для прохода по всем данным в price.
Trend_price_line = []  # Пересоздаем переменную для записи в ней нужные нам данные.

rounding(Trend_price_lines, Trend_price_line)

adds = []  # Переменная для добавления полседних данных в базу данных.

# Функция для проверки наличия последних данных.
# Если данные за текущий день (при условии что он рабочий, и, устройство подключено в интернету) -
# не записаны в файл, то, записываем последние данные из сайта в нашу базу данных.
if internet:
	# Переменная для добавления новых данных в базу данных.
	adds.append(by[-1])
	adds.append(Trend_price_line[-1])

	# bool тип данных, проверка условий.
	# Если останется истенным (True), это означает, что, последние данные не были записаны в базу данных.
	To_day = True

	with open("Tesla_data.csv", mode="r+", encoding='utf-8') as add_new:
		reader = csv.DictReader(add_new, delimiter=";", lineterminator="\r")
		for row in reader:
			if str(row['Data']) == str(by[-1]):
				To_day = False  # Если были записаны, то не вызывает остаток кода.

		# Если To_day остался - True, то проходит запись данных в базу данных.
		if To_day:
			adders = csv.writer(add_new, delimiter=";", lineterminator="\r")
			adders.writerow(adds)

			for row in reader:
				if any(row):
					writer.writerow(row)
