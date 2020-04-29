from flask import Flask, request, render_template, session, redirect

import urllib.request 
import json
import pandas as pd
from datetime import datetime, timedelta
import re
import os
import jinja2
import random

# ==================================== global variable ====================================
# =========================================================================================


site_template = jinja2.Template("{{ date.strftime('%-m월 %d일') }}")
api_template = jinja2.Template("{{ date.strftime('%Y-%m-%d') }}")
# formated_date = site_template.render(date=today)

infos = []

application = app = Flask(__name__)
app.secret_key = "cart_savior"

# =========================================================================================
# =========================================================================================

def get_random_keywords():
	keys = []
	path_to_current_file = os.path.realpath(__file__)
	current_directory = os.path.split(path_to_current_file)[0]
	path_to_file = os.path.join(current_directory, "category_code.json")
	with open(path_to_file) as mydata:
		my_json_data = json.load(mydata)
	for item in my_json_data:
		keys.append(item['item_name'])
	return random.sample(keys, 3)


@app.route('/')
def search_form():
	random_keys = get_random_keywords()
	context = {'random_keys': random_keys}
	return render_template("main.html", **context)


# 차액 표시 필터
@app.template_filter()
def diff_format(value):
	if value > 0:
		return f"{value:,d}"
	elif value < 0:
		value = value * -1
		return f"{value:,d}"

	
	value = float(value)
	return "${:,.2f}".format(value)

# 날짜와 아이템을 넣어서 obj 까지 생성하여 반환해주는 함수
def extract_from_url(date, item):
	url = "http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList" +\
	"&p_cert_key=bceaf385-9d34-4a75-9c6f-0607eb325485&p_cert_id=pje1740&p_returntype=json" +\
	"&p_product_cls_code=01" +\
	"&p_regday=" + api_template.render(date=date) +\
	"&p_item_category_code=" + str(item['category_code'])
	response = urllib.request.urlopen(url) 
	json_str = response.read().decode("utf-8")
	obj = json.loads(json_str)
	return obj

def get_dpr1(item, start_date):
	df = None
	while (1):
		obj = extract_from_url(start_date, item)
		try:
			df = pd.DataFrame(obj['data']['item'])
			df = df[df.item_name == item['item_name']]
		except TypeError:
			start_date = start_date - timedelta(days=1)
			continue
		# rank가 일치하는 행 뽑아내기
		row = df[df['rank']==item['rank']].iloc[0]
		if ("-" in row.dpr1):
			start_date = start_date - timedelta(days=1)
			continue
		else:
			break
	return row.dpr1

# 랭크까지 구분된 item의 리스트가 들어온다. 
def get_info(item, date):
	one_item = None
	df = None
	# 여기서부터 값이 없으면 다시 거슬러 올라가야함
	while (1):
		obj = extract_from_url(date, item)
		try:
			df = pd.DataFrame(obj['data']['item'])
			df = df[df.item_name == item['item_name']]
		except TypeError:
			date = date - timedelta(days=1)
			continue
		# rank가 일치하는 행 뽑아내기
		row = df[df['rank']==item['rank']].iloc[0]
		if ("-" in row.dpr1):
			date = date - timedelta(days=1)
			continue
		else:
			break
	one_item = {'item_name': None, 'item_price': None, 'date': None, 'kind_name': None, 'rank': None, 'last_week': None, 'diff': None}
	one_item['item_name'] = row.item_name
	one_item['item_price'] = row.dpr1
	this_week = int(one_item['item_price'].replace(',', ''))	
	if (row.dpr3 == "-"):
		one_item['last_week'] = get_dpr1(item, date + timedelta(days=7))
	else:
		one_item['last_week'] = row.dpr3
	# 차액 계산하기
	last_week = int(one_item['last_week'].replace(',', ''))
	last_week = int(one_item['last_week'].replace(',', ''))
	# one_item['diff'] = f"{this_week - last_week:,d}"
	one_item['diff'] = this_week - last_week
	one_item['date'] = site_template.render(date=date)
	one_item['kind_name'] = row.kind_name
	one_item['rank'] = item['rank']
	return one_item


# 검색어를 포함하는 상품명을 모두 받아와 반복문을 돌면서 정보를 뽑는다. 
# item은 해당 상품에 대한 정보를 가지고 있는 딕셔너리.
# 여기서 rank 까지 구분한 리스트를 한번 정리할 필요가 있어보임. 
def append_info(items):
	list = []
	for item in items:
		list.append(get_info(item, session['today']))
	return list

# 부류번호, 상품명, 상품코드를 포함한 딕셔너리를 items 리스트에 넣어 반환한다. 
def get_all_items(search_key):
	path_to_current_file = os.path.realpath(__file__)
	current_directory = os.path.split(path_to_current_file)[0]
	path_to_file = os.path.join(current_directory, "category_code.json")
	with open(path_to_file) as mydata:
		my_json_data = json.load(mydata)
	items = []
	for item in my_json_data:
		if search_key in item['item_name']:
			items.append(item)
	return items


def get_items_with_rank(items):
	today = datetime.today()
	# 일요일 테스트
	# today = datetime.today() - timedelta(days=1)
	df = None
	result = []
	for item in items:
		# 일요일이면 되돌아가기 위한 반복문
		while (1):
			obj = extract_from_url(today, item)
			# 모든 타입에 대한 (중품, 상품 등) 구분이 있는 가격의 딕셔너리 리스트
			# 해당 품목의 df 행 불러오기
			try:
				df = pd.DataFrame(obj['data']['item'])
				df = df[df.item_name == item['item_name']]
				break
			except TypeError:
				today = today - timedelta(days=1)
		for row in df.itertuples():
			temp = {"category_code": None, "item_name": None, 'rank': None}
			temp['category_code'] = item['category_code']
			temp['item_name'] = item['item_name']
			temp['rank'] = row.rank
			result.append(temp)
	# 오늘 날짜를 저장. 일요일인 경우 하루 전의 날짜를 세션에 저장해둔다. 
	session['today'] = today
	return result

@app.route('/search', methods=['GET'])
def search(item_name="오류", item_price=0, date=None):
	# 검색 키워드 받아오기
	search_key =request.args.get("search_text")
	# 해당 키워드가 포함된 모든 item_name 리스트로 받아오기.
	items = get_all_items(search_key)
	# 검색 결과가 없으면
	if len(items) == 0:
		return render_template("search_no_result.html")
	# rank 정보를 추가한 item 리스트를 새로이 생성
	items = get_items_with_rank(items)
	# 필요 정보를 추출한 infos 리스트 생성
	infos = append_info(items)
	# import pdb; pdb.set_trace()
	# infos 리스트를 세션에 저장한다
	session['list'] = infos
	# 받아온 item 마다 검색하여 get_info를 하고 해당 딕셔너리를 모아 리스트로 만든다. 
	return render_template("search_list.html", list=infos)


@app.route('/search/<search_key>')
def search_hash(item_name="오류", item_price=0, date=None, search_key="오류"):
	items = get_all_items(search_key)
	# 검색 결과가 없으면
	if len(items) == 0:
		return render_template("search_no_result.html")
	# rank 정보를 추가한 item 리스트를 새로이 생성
	items = get_items_with_rank(items)
	# 필요 정보를 추출한 infos 리스트 생성
	infos = append_info(items)
	# import pdb; pdb.set_trace()
	# infos 리스트를 세션에 저장한다
	session['list'] = infos
	# 받아온 item 마다 검색하여 get_info를 하고 해당 딕셔너리를 모아 리스트로 만든다. 
	return render_template("search_list.html", list=infos)


@app.route('/search/<int:index>')
def detail(index):
	if "list" in session:
		context = session['list'][index - 1]
		return render_template("search_detail.html", **context)
	else:
		return redirect(url_for("search"))

if __name__ == '__main__':
	app.run(debug=True, port=8000, host='0.0.0.0')
