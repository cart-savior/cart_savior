from flask import Blueprint, render_template, url_for, redirect

import pandas as pd
import json
import sqlite3
import urllib.request 
from datetime import datetime, timedelta
import re
import jinja2
import random

fill_db = Blueprint("fill_db", __name__, static_folder="static", template_folder="templates")

api_template = jinja2.Template("{{ date.strftime('%Y-%m-%d') }}")

# 넘겨준 날짜에 대한 데이터를 db에 채워넣는 함수
def fill_price_one_day_data(date):
	categories = ['100', '200', '300', '400', '500', '600']
	result = pd.DataFrame()

	conn = sqlite3.connect("cart_savior.db")
	c = conn.cursor()

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

@fill_db.route('/cron/filldb')
def fill_price_data():
	end_date = datetime.today()
	start_date = end_date - timedelta(days=5)
	while ((end_date + timedelta(days=1)).date() != start_date.date()):
		fill_price_one_day_data(start_date)
		print(api_template.render(date=start_date))
		start_date = start_date + timedelta(days=1)
	return redirect(url_for("search_functions.index"))