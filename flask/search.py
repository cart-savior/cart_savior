from flask import Blueprint, render_template

search = Blueprint("second", __name__, static_folder="static", template_folder="templates")

@search.route('/')
def index():
	"""메인 페이지 구현 함수"""
	# 랜덤 해시코드 3개를 받아오는 함수
	random_keys = get_random_keywords()
	context = {'random_keys': random_keys}
	return render_template("main.html", **context)