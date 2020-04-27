# import json
# import os
from flask import Flask
from flask import request
from flask import render_template

import urllib.request 
import json
import pandas as pd
from datetime import datetime, timedelta
import re
import os
import jinja2

# path_to_current_file = os.path.realpath(__file__)
# current_directory = os.path.split(path_to_current_file)[0]
# path_to_file = os.path.join(current_directory, "category_code.json")
# with open(path_to_file) as mydata:
#     my_json_data = json.load(mydata)

# search_key = "밤"
# items = []
# for item in my_json_data:
# 	if search_key in item['item_name']:
# 		items.append(item)

# print(items)


# url = "http://www.kamis.or.kr/service/price/xml.do?action=dailyPriceByCategoryList" +\
# 	"&p_cert_key=bceaf385-9d34-4a75-9c6f-0607eb325485&p_cert_id=pje1740&p_returntype=json" +\
# 	"&p_product_cls_code=01" +\
# 	"&p_regday=" + "2020-04-19" +\
# 	"&p_country_code=1101" +\
# 	"&p_item_category_code=" + "100"

# response = urllib.request.urlopen(url)
# json_str = response.read().decode("utf-8")
# obj = json.loads(json_str)
# print(obj)
# df = pd.DataFrame(obj['data']['item'])

# template = jinja2.Template("{{ date.strftime('%Y년%m월%d일') }}")
# date_now = datetime.now()
# formated_date = template.render(date= date_now)
# print(formated_date)

today = datetime.today()
# print(today - timedelta(days=10))
template = jinja2.Template("{{ date.strftime('%Y-%m-%d') }}")
print(template.render(date= today))