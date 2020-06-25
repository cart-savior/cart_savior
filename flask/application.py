from flask import Flask, request, render_template, session, redirect

import sqlite3
import urllib.request 
import json
import pandas as pd
from datetime import datetime, timedelta
import re
import os
import jinja2
import random

import market_api
import add_unit
from search import search

# ==================================== global variable ====================================
# =========================================================================================


api_template = jinja2.Template("{{ date.strftime('%Y-%m-%d') }}")

application = app = Flask(__name__)
app.secret_key = "cart_savior"
app.register_blueprint(search, url_prefix="")


# =========================================================================================
# =========================================================================================

# def get_random_keywords():
# 	"""빈 데이터가 없는 상품들 중 3가지를 랜덤으로 뽑아서 리스트로 반환하는 함수"""
# 	keys = ['쌀', '찹쌀', '콩', '팥', '녹두', '고구마', '감자', '배추', '양배추', '시금치', '상추',
#        '얼갈이배추', '수박', '참외', '오이', '호박', '토마토', '딸기', '무', '당근', '열무',
#        '건고추', '풋고추', '붉은고추', '양파', '파', '생강', '고춧가루', '미나리', '깻잎', '피망',
#        '파프리카', '멜론', '깐마늘', '방울토마토', '참깨', '땅콩', '느타리버섯', '팽이버섯',
#        '새송이버섯', '호두', '아몬드', '사과', '배', '포도', '바나나', '참다래', '파인애플', '오렌지',
#        '레몬', '건포도', '건블루베리', '망고', '쇠고기', '돼지고기', '닭고기', '계란', '우유',
#        '고등어', '꽁치', '갈치', '명태', '물오징어', '건멸치', '건오징어', '김', '건미역', '수입조기',
#        '새우젓', '멸치액젓', '굵은소금', '전복', '새우']
# 	return random.sample(keys, 3)


def key_replace(search_key):
	"""입력된 검색어를 가지고 있는 데이터와 일치하게 변경해주는 함수"""
	path_to_current_file = os.path.realpath(__file__)
	current_directory = os.path.split(path_to_current_file)[0]
	path_to_file = os.path.join(current_directory, "search_replace.json")
	with open(path_to_file) as mydata:
		my_json_data = json.load(mydata)
	for item in my_json_data:
		if search_key == item['input']:
			return item['output']
	return [search_key]


def market_search_replace(search_key):
	"""입력된 검색어를 가지고 있는 데이터와 일치하게 변경해주는 함수"""
	path_to_current_file = os.path.realpath(__file__)
	current_directory = os.path.split(path_to_current_file)[0]
	path_to_file = os.path.join(current_directory, "market_replace.json")
	with open(path_to_file) as mydata:
		my_json_data = json.load(mydata)
	for item in my_json_data:
		if search_key == item['input']:
			return item['output']
	return search_key


# 차액 표시 필터
@app.template_filter()
def num_format(value):
	"""숫자를 int로 받으면 쉼표를 포함하여 표기해주는 함수"""
	if value > 0:
		return f"{value:,d}"
	elif value < 0:
		value = value * -1
		return f"{value:,d}"

	value = float(value)
	return "${:,.2f}".format(value)

# 지난주, 지난달, 지난해 데이터는 따로 get_price_with_rank를 만들어서 하는 게 빠를듯
def get_price_with_rank(item, start_date):
	"""item_code, kind_name, rank 까지로 제한된 상품에 대해 날짜를 되돌아가며 가격을 찾는 함수"""
	conn = sqlite3.connect("cart_savior.db")
	c = conn.cursor()
	day_traceback = 0
	result = {}
	# TODO 랭크도 포함인데, 이건 items 테이블에 없어서 여기서 리스트로 넘겨야할듯
	while (day_traceback < 5):
		date_text = api_template.render(date=start_date)
		c.execute(
			"SELECT * FROM item_price WHERE date='" + date_text + "'"
			"AND item_code=" + str(item['item_code']) +
			" AND kind_name LIKE '%" + item['kind_name'] + "%'"
			" AND rank='" + item['rank'] + "'"
		)
		data = c.fetchall()
		# 아예 자료가 없거나 0인 경우
		if len(data) == 0:
			start_date -= timedelta(days=1)
			day_traceback += 1
		elif data[0][6] == 0:
			start_date -= timedelta(days=1)
			day_traceback += 1
		else:
			# 딕셔너리 형으로 다시 정리
			one_item = {}
			one_item['date'] = data[0][0]
			one_item['price'] = data[0][6]
			return one_item

def get_price(item, start_date):
	"""전달 받은 날짜를 기점으로 dpr1이 있는 날짜의 dpr1을 반환하는 함수"""
	conn = sqlite3.connect("cart_savior.db")
	c = conn.cursor()
	day_traceback = 0
	result = []
	# TODO 랭크도 포함인데, 이건 items 테이블에 없어서 여기서 리스트로 넘겨야할듯
	while (day_traceback < 10):
		date_text = api_template.render(date=start_date)
		c.execute(
			"SELECT * FROM item_price WHERE date='" + date_text + "'"
			"AND item_code=" + str(item['item_code']) +
			" AND kind_name LIKE '%" + item['kind_name'] + "%'"
		)
		data = c.fetchall()
		# 아예 자료가 없거나 0인 경우
		if len(data) == 0:
			start_date -= timedelta(days=1)
			day_traceback += 1
		elif data[0][6] == 0:
			start_date -= timedelta(days=1)
			day_traceback += 1
		else:
			for row in data:
				# 딕셔너리 형으로 다시 정리
				one_item = {}
				one_item['date'] = row[0]
				one_item['item_name'] = row[1]
				one_item['item_code'] = row[2]
				one_item['kind_name'] = row[3]
				one_item['rank'] = row[4]
				one_item['price'] = row[6]
				result.append(one_item)
			return result


def get_info(items):
	"""최신일자로 조회한 모든 행이 담긴 item_codes를 받아와서 출력에 필요한 형태로 정리하는 함수"""
	result = []
	for item in items:
		one_item = {}
		one_item['date'] = datetime.strptime(item['date'], '%Y-%m-%d')
		one_item['item_name'] = item['item_name']
		one_item['item_code'] = item['item_code']
		one_item['item_price'] = item['price']
		one_item['kind_name'] = item['kind_name']
		one_item['rank'] = item['rank']
		
		# 문자열 date를 다시 datetime 오브젝트로 변환.
		date_obj = datetime.strptime(item['date'], '%Y-%m-%d')
		
		# get_price 함수를 이용해서 지난주, 지난달, 1년전 데이터 가져오기.
		last_week = get_price_with_rank(item, date_obj - timedelta(days=7))
		if last_week is None:
			one_item['last_week'] = 0
			one_item['last_week_date'] = date_obj - timedelta(days=7)
		else:
			one_item['last_week'] = last_week['price']
			one_item['last_week_date'] = datetime.strptime(last_week['date'], '%Y-%m-%d')
		
		# TODO 지난주 자료가 없을 땐, 자료 없음으로 띄울 수 있도록 해보면?
		one_item['diff'] = one_item['item_price'] - one_item['last_week']

		last_month = get_price_with_rank(item, date_obj - timedelta(days=30))
		if last_month is None:
			one_item['last_month'] = 0
			one_item['last_week_date'] = date_obj - timedelta(days=30)
		else:
			one_item['last_month'] = last_month['price']
			one_item['last_month_date'] = datetime.strptime(last_month['date'], '%Y-%m-%d')
		
		last_year = get_price_with_rank(item, date_obj - timedelta(days=365))
		if last_year is None:
			one_item['last_year'] = 0
			one_item['last_year_date'] = date_obj - timedelta(days=365)
		else:
			one_item['last_year'] = last_year['price']
			one_item['last_year_date'] = datetime.strptime(last_year['date'], '%Y-%m-%d')

		result.append(one_item)

	return result


def get_all_items(search_key):
	"""상품명이 검색어를 포함하면 해당 행을 items에서 가져온다"""
	conn = sqlite3.connect("cart_savior.db")
	c = conn.cursor()
	c.execute("SELECT * FROM items WHERE item_name LIKE '%" + search_key + "%'")
	data = c.fetchall()
	# 찾는 모든 행을 딕셔너리로 바꿔서 전달
	result = []
	for item in data:
		one_item = {}
		one_item['item_name'] = item[1]
		one_item['item_code'] = item[2]
		one_item['kind_name'] = item[3]
		result.append(one_item)
	return result


def get_items_from_price_table(items_searched):
	"""모든 아이템 코드에 대한 최신일자 행을 반환해주는 함수"""
	# index, item_name, item_code, kind_name이 저장된 딕셔너리 리스트를 받아온다.
	# 오늘 날짜
	# today = datetime.today() - timedelta(days=4)
	today = datetime.today()
	result = []
	conn = sqlite3.connect("cart_savior.db")
	c = conn.cursor()

	for item in items_searched:
		data = get_price(item, today)
		if data is not None:
			result.extend(data)
	return result


# ==========================================

# 검색 로직
# 검색 키워드 받아오기 -> category_code.json에서 해당 키워드를 포함하는 상품명 모두 받아와 리스트에 저장하기(get_all_items)
# -> rank 정보를 추가한 리스트 생성(get_items_with_rank) 
# -> 해당 리스트로 나머지 필요한 정보를 모두 추출하여 새로운 리스트 생성 (append_info)
# -> 해당 리스트(infos) 세션에 저장 -> search_list.html에 정보 뿌리기

# ==========================================

@app.route('/search', methods=['GET'])
def search(item_name="오류", item_price=0, date=None):
	"""입력된 키워드를 기반으로 상품 리스트를 만들고 정보를 모아 리스트로 만드는 함수.
	이 함수는 검색창을 통해 키워드가 들어올 경우 실행된다."""
	search_key =request.args.get("search_text")
	search_key = key_replace(search_key)
	# search_key는 리스트 형태로 바뀐다. 검색어 전환 때문에.
	items_searched = []
	for key in search_key:
		items_searched.extend(get_all_items(key))
	# 검색 결과가 없으면
	if len(items_searched) == 0:
		random_keys = search.get_random_keywords()
		context = {'random_keys': random_keys}
		return render_template("search_no_result.html", **context)
	# item_price 테이블에서 items_searched 코드가 있는 최근일자 행을 조회
	items = get_items_from_price_table(items_searched)
	infos = get_info(items)
	session['list'] = infos
	# 금일자 dataframe에 해당 상품이 없으면
	if len(session['list']) == 0:
		random_keys = search.get_random_keywords()
		context = {'random_keys': random_keys}
		return render_template("search_no_result.html", **context)
	return render_template("search_list.html", list=infos)


@app.route('/search/<search_key>')
def search_hash(item_name="오류", item_price=0, date=None, search_key="오류"):
	"""입력된 키워드를 기반으로 상품 리스트를 만들고 정보를 모아 리스트로 만드는 함수.
	이 함수는 해시태그 클릭을 통해 키워드가 들어올 경우 실행된다."""
	items = get_all_items(search_key)
	# 검색 결과가 없으면
	if len(items) == 0:
		random_keys = get_random_keywords()
		context = {'random_keys': random_keys}
		return render_template("search_no_result.html", **context)
	items = get_items_with_rank(items)
	infos = append_info(items)
	session['list'] = infos
	# 금일자 dataframe에 해당 상품이 없으면
	if len(session['list']) == 0:
		random_keys = get_random_keywords()
		context = {'random_keys': random_keys}
		return render_template("search_no_result.html", **context)
	return render_template("search_list.html", list=infos)


@app.route('/search/<int:index>')
def detail(index):
	"""search_list에서 클릭한 상품을 기반으로 search_detail.html로 정보를 뿌리는 함수.
	index는 몇번째 상품을 클릭했는지 알려주는 변수"""
	if "list" in session:
		context = session['list'][index - 1]
		market_key = market_search_replace(context['item_name'])
		market = market_api.add_all_market(market_key)
		# unit 관련 데이터 쿼리로 뽑아야함
		unit_info = add_unit.add_unit(context)
		return render_template("search_detail.html", item=context, market=market, unit_info=unit_info)
	else:
		return redirect(url_for("search"))

if __name__ == '__main__':
	# app.run(debug=True, port=8000, host='0.0.0.0')
	application.debug = True
	application.run()