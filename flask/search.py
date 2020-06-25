from flask import Blueprint, render_template
import random
import urllib.request 
import json
import pandas as pd
from datetime import datetime, timedelta
import re
import os
import jinja2
import random

search = Blueprint("search", __name__, static_folder="static", template_folder="templates")

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

@search.route('/')
def index():
	"""메인 페이지 구현 함수"""
	# 랜덤 해시코드 3개를 받아오는 함수
	random_keys = get_random_keywords()
	context = {'random_keys': random_keys}
	return render_template("main.html", **context)
