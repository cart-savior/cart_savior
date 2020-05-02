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


api_template = jinja2.Template("{{ date.strftime('%Y-%m-%d') }}")

application = app = Flask(__name__)
app.secret_key = "cart_savior"

# =========================================================================================
# =========================================================================================

def get_random_keywords():
	"""빈 데이터가 없는 상품들 중 3가지를 랜덤으로 뽑아서 리스트로 반환하는 함수"""
	keys = ['쌀', '찹쌀', '콩', '팥', '녹두', '고구마', '감자', '배추', '양배추', '시금치', '상추',
       '얼갈이배추', '수박', '참외', '오이', '호박', '토마토', '딸기', '무', '당근', '열무',
       '건고추', '풋고추', '붉은고추', '양파', '파', '생강', '고춧가루', '미나리', '깻잎', '피망',
       '파프리카', '멜론', '깐마늘', '방울토마토', '참깨', '땅콩', '느타리버섯', '팽이버섯',
       '새송이버섯', '호두', '아몬드', '사과', '배', '포도', '바나나', '참다래', '파인애플', '오렌지',
       '레몬', '건포도', '건블루베리', '망고', '쇠고기', '돼지고기', '닭고기', '계란', '우유',
       '고등어', '꽁치', '갈치', '명태', '물오징어', '건멸치', '건오징어', '김', '건미역', '수입조기',
       '새우젓', '멸치액젓', '굵은소금', '전복', '새우']
	return random.sample(keys, 3)


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
	return search_key


@app.route('/')
def index():
	"""메인 페이지 구현 함수"""
	random_keys = get_random_keywords()
	context = {'random_keys': random_keys}
	return render_template("main.html", **context)


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

# 날짜와 아이템을 넣어서 obj 까지 생성하여 반환해주는 함수
def extract_from_url(date, item):
	"""날짜와 아이템을 api url에넣어서 딕셔너리로 반환해주는 함수"""
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
	"""전달 받은 날짜를 기점으로 dpr1이 있는 날짜의 dpr1을 반환하는 함수"""
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
		try: 
			row = df[df['rank']==item['rank']].iloc[0]
		except IndexError:
			session['temp_date'] = start_date
			return 0
		if ("-" in row.dpr1):
			start_date = start_date - timedelta(days=1)
			continue
		else:
			break
	session['temp_date'] = start_date
	return row.dpr1

def get_info(item, date):
	"""rank, kind_name으로 구분된 상품에 대하여 상품명, 금일 가격, kind_name, rank, 
	일주일 전 가격, 한 달 전 가격, 일년 전 가격, 차액을 구하여 딕셔너리로 반환하는 함수"""
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
		if df.empty:
			date = date - timedelta(days=1)
			continue
		df = df[df['rank']==item['rank']]
		# kind_name도 있는 날, 없는 날이 달라서 오류가 발생함. 찾을 수 없을 경우 -1 에러코드 반환
		try:
			row = df[df['kind_name']==item['kind_name']].iloc[0]
		except IndexError:
			return -1
		if ("-" in row.dpr1):
			date = date - timedelta(days=1)
			continue
		else:
			break
	one_item = {'item_name': None, 'category_code': None, 'item_code': None, 'item_price': None, 'date': None, \
		'kind_name': None, 'rank': None, 'last_week': None, 'diff': None}
	one_item['item_name'] = row.item_name
	one_item['category_code'] = item['category_code']
	one_item['item_code'] = item['item_code']
	one_item['item_price'] = int(row.dpr1.replace(',', ''))
	if (row.dpr3 == "-"):
		one_item['last_week'] = get_dpr1(item, date - timedelta(days=7))
		one_item['last_week_date'] = session['last_week_date']
	else:
		one_item['last_week'] = int(row.dpr3.replace(',', ''))
		one_item['last_week_date'] = date - timedelta(days=7)
	one_item['diff'] = one_item['item_price'] - one_item['last_week']
	one_item['date'] = date
	one_item['kind_name'] = row.kind_name
	one_item['rank'] = item['rank']
	one_item['last_month'] = row.dpr5
	one_item['last_month_date'] = date - timedelta(days=30)
	one_item['last_year'] = row.dpr6
	one_item['last_year_date'] = date - timedelta(days=365)
	return one_item


def append_info(items):
	"""검색어를 포함하는 상품을 rank, kind_name으로 모두 나누어 각각에 대한 데이터를 딕셔너리로 정리하고,
	생성된 딕셔너리를 리스트에 추가하여 반환하는 함수"""
	list = []
	for item in items:
		temp = get_info(item, session['today'])
		if temp != -1:
			list.append(temp)
	return list

def get_all_items(search_key):
	"""검색어를 기반으로 category_code.json의 정보를 딕셔너리로 가져와 리스트에 축적하여 반환하는 함수"""
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
	"""키워드로 받아온 상품을 rank, kind_name을 구분하여 리스트에 축적하는 함수"""
	today = datetime.today()
	# 일요일로 테스트를 진행하려면 오늘로부터 일요일이 되기 위한 일수를 빼고 진행하면 된다. 
	# today = datetime.today() - timedelta(days=3)
	df = None
	result = []
	for item in items:
		# 일요일이면 되돌아가기 위한 반복문
		while (1):
			obj = extract_from_url(today, item)
			try:
				df = pd.DataFrame(obj['data']['item'])
				df = df[df.item_name == item['item_name']]
				break
			except TypeError:
				today = today - timedelta(days=1)
		for row in df.itertuples():
			temp = {"category_code": None, "item_code": None, "item_name": None, 'rank': None, 'kind_name': None}
			temp['category_code'] = item['category_code']
			temp['item_code'] = item['item_code']
			temp['item_name'] = item['item_name']
			temp['rank'] = row.rank
			temp['kind_name'] = row.kind_name
			result.append(temp)
	# 오늘 날짜를 저장. 일요일인 경우 하루 전의 날짜를 세션에 저장해둔다. 
	session['today'] = today
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
		# 작년, 저번 달 데이터 가공
		if (context['last_month'] == "-"):
			context['last_month'] = get_dpr1(context, context['date'] - timedelta(days=30))
			context['last_month_date'] = session['temp_date']
		else:
			context['last_month'] = int(context['last_month'].replace(',', ''))
		if (context['last_year'] == "-"):
			context['last_year'] = get_dpr1(context, context['date'] - timedelta(days=365))
			context['last_year_date'] = session['temp_date']
		else:
			context['last_year'] = int(context['last_year'].replace(',', ''))
		# import pdb; pdb.set_trace()
		test_list = ["jilim", "sohpark", "dachung"]
		return render_template("search_detail.html", item=context, test=test_list)
	else:
		return redirect(url_for("search"))

if __name__ == '__main__':
	app.run(debug=True, port=8000, host='0.0.0.0')
