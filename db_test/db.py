import sqlite3
import os
import urllib.request 
import json
import pandas as pd
from datetime import datetime, timedelta
import re
import jinja2
import random

conn = sqlite3.connect("cart_savior.db")
c = conn.cursor()

def create_items_table():
	c.execute(
		'CREATE TABLE items('
		'id INTEGER PRIMARY KEY AUTOINCREMENT,'
		'item_name TEXT,'
		'category_code INTEGER,'
		'item_code INTEGER,'
		'unit TEXT,'
		'ratio REAL)'
		)

def create_wiki_table():
	c.execute(
		'CREATE TABLE wiki('
		'item_code INTEGER UNIQUE PRIMARY KEY,'
		'item_name TEXT,'
		'wiki TEXT,'
		'FOREIGN KEY(item_code) REFERENCES items(item_code))'
		)

def input_data_items(item_name, category_code, item_code, unit, ratio):
	c.execute(
		"INSERT OR IGNORE INTO items(item_name, category_code, item_code, unit, ratio) VALUES(?, ?, ?, ?, ?)",
		(item_name, category_code, item_code, unit, ratio)
	)
	conn.commit()

def fill_items():
	path_to_current_file = os.path.realpath(__file__)
	current_directory = os.path.split(path_to_current_file)[0]
	path_to_file = os.path.join(current_directory, "category_code.json")
	with open(path_to_file) as mydata:
		my_json_data = json.load(mydata)
	for item in my_json_data:
		input_data_items(item['item_name'], item['category_code'], item['item_code'], item['unit'], item['ratio'])

def input_data_wiki(item_code, item_name):
	c.execute(
		"INSERT OR IGNORE INTO wiki(item_code, item_name) VALUES(?, ?)",
		(item_code, item_name)
	)
	conn.commit()

def fill_wiki():
	c.execute("SELECT item_code, item_name FROM items")
	data = c.fetchall()
	print("hi")
	for row in data:
		print(row[0])
		input_data_wiki(row[0], row[1])

# 가격 데이터 날짜를 지정해서 받아오기

api_template = jinja2.Template("{{ date.strftime('%Y-%m-%d') }}")

def create_price_table():
	c.execute(
		'CREATE TABLE item_price('
		'date TEXT,'
		'item_name TEXT,'
		'item_code INTEGER,'
		'kind_name TEXT,'
		'rank TEXT,'
		'unit TEXT,'
		'price INTEGER,'
		'FOREIGN KEY(item_code) REFERENCES items(item_code),'
		'UNIQUE(date, item_code, kind_name) ON CONFLICT REPLACE)'
	)

def drop_price_table():
	c.execute(
		'DROP TABLE item_price'
	)

# 넘겨준 날짜에 대한 데이터를 db에 채워넣는 함수
def fill_price_one_day_data(date):
	categories = ['100', '200', '300', '400', '500', '600']
	result = pd.DataFrame()

	for category in categories:
		format_date = api_template.render(date=date)
		url = "http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList" +\
		"&p_cert_key=bceaf385-9d34-4a75-9c6f-0607eb325485&p_cert_id=pje1740&p_returntype=json" +\
		"&p_product_cls_code=01" +\
		"&p_regday=" + format_date +\
		"&p_item_category_code=" + category
		response = urllib.request.urlopen(url) 
		json_str = response.read().decode("utf-8")
		obj = json.loads(json_str)
		try:
			df = pd.DataFrame(obj['data']['item'])
		except TypeError:
			return
		df = df.drop(['kind_code', 'rank_code', 'day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7', 'dpr2', 'dpr3', 'dpr4', 'dpr5', 'dpr6', 'dpr7'], axis=1)
		result = result.append(df)
	
	# df 의 column 순서
	# index, item_name, item_code, kind_name, rank, unit, dpr1
	
	# 하루치 df 완성된 이후 각각의 row를 테이블에 넣기
	
	for row in result.itertuples():
		item_name = row[1]
		item_code = row[2]
		kind_name = row[3]
		rank = row[4]
		unit = row[5]
		if (row[6] == "-"):
			price = 0
		else:
			price = int(row[6].replace(',', ''))
		# print(item_name, item_code, kind_name, rank, unit, price)
		c.execute(
			'INSERT or REPLACE INTO item_price(date, item_name, item_code, kind_name, rank, unit, price) VALUES(?, ?, ?, ?, ?, ?, ?)',
			(format_date, item_name, item_code, kind_name, rank, unit, price)
		)
		conn.commit()
	
def fill_price_data():
	start_date = datetime(2019, 1, 1)
	end_date = datetime.today()
	while ((end_date + timedelta(days=1)).date() != start_date.date()):
		fill_price_one_day_data(start_date)
		print(api_template.render(date=start_date))
		start_date = start_date + timedelta(days=1)


def read():
	c.execute("SELECT price FROM item_price WHERE item_code=111 AND date='2020-06-23'")
	data = c.fetchall()
	for row in data:
		print(row[0])

read()