from flask import Flask, request, render_template, session, redirect

from search_functions import search_functions
from fill_db import fill_db

# ==================================== global variable ====================================
# =========================================================================================


# api_template = jinja2.Template("{{ date.strftime('%Y-%m-%d') }}")

application = app = Flask(__name__)
app.secret_key = "cart_savior"
app.register_blueprint(search_functions, url_prefix="")
app.register_blueprint(fill_db, url_prefix="")


# =========================================================================================
# =========================================================================================


# 차액 쉼표 표시 필터
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


if __name__ == '__main__':
	# app.run(debug=True, port=8000, host='0.0.0.0')
	application.debug = True
	application.run()