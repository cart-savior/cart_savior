from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import redirect

import urllib.request 
import json
import pandas as pd
from datetime import datetime
import re
import os
import jinja2

today = str(datetime.now())
today_date = re.search(r'\d{4}-\d{2}-\d{2}', today)[0]
today_date = "2020-04-20"
template = jinja2.Template("{{ date.strftime('%-m월 %d일') }}")
date_now = datetime.now()
formated_date = template.render(date= date_now)
infos = []

app = Flask(__name__)
app.secret_key = "cart_savior"

@app.route('/')
def search_form():
	return render_template("main.html")

def get_info(today_date, item):
	url = "http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList" +\
	"&p_cert_key=bceaf385-9d34-4a75-9c6f-0607eb325485&p_cert_id=pje1740&p_returntype=json" +\
	"&p_product_cls_code=01" +\
	"&p_regday=" + today_date +\
	"&p_country_code=1101" +\
	"&p_item_category_code=" + str(item['category_code'])
	response = urllib.request.urlopen(url) 
	json_str = response.read().decode("utf-8")
	obj = json.loads(json_str)
	# 모든 타입에 대한 (중품, 상품 등) 구분이 있는 가격의 딕셔너리 리스트
	result = []
	# 해당 품목의 df 행 불러오기
	df = pd.DataFrame(obj['data']['item'])
	df = df[df.item_name == item['item_name']]
	for row in df.itertuples():
		one_item = {'item_name': None, 'item_price': None, 'date': None, 'kind_name': None, 'rank': None, 'last_week': None, 'diff': None}
		one_item['item_name'] = row.item_name
		one_item['item_price'] = row.dpr1
		one_item['last_week'] = row.dpr3
		# 차액 계산하기
		this_week = int(row.dpr1.replace(',', ''))
		last_week = int(row.dpr3.replace(',', ''))
		one_item['diff'] = f"{this_week - last_week:,d}"
		one_item['date'] = formated_date
		one_item['kind_name'] = row.kind_name
		one_item['rank'] = row.rank
		result.append(one_item)
	return result
	# today_price = df.dpr1.values[0]
	# kind_name = df.kind_name.values[0]
	# return {'item_name': item['item_name'], 'item_price': today_price, 'date': today_date, 'kind_name': kind_name}

# 검색어를 포함하는 상품명을 모두 받아와 반복문을 돌면서 정보를 뽑는다. 
# item은 해당 상품에 대한 정보를 가지고 있는 딕셔너리.
def append_info(items, today_date):
	list = []
	for item in items:
		list.extend(get_info(today_date, item))
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


@app.route('/search', methods=['GET'])
def search(item_name="오류", item_price=0, date=None):
	# 검색 키워드 받아오기
	search_key =request.args.get("search_text")
	# 해당 키워드가 포함된 모든 item_name 리스트로 받아오기.
	items = get_all_items(search_key)
	# 검색 결과가 없으면
	if len(items) == 0:
		return render_template("search_no_result.html")
	infos = append_info(items, today_date)
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