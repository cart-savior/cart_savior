from flask import Flask, request, render_template, session, redirect, url_for
from apscheduler.schedulers.background import BackgroundScheduler

from search_functions import search_functions
import fill_db

import pandas as pd
import json
import sqlite3
import urllib.request 
from datetime import datetime, timedelta
import re
import jinja2
import random

# ==================================== global variable ====================================
# =========================================================================================


application = app = Flask(__name__)
app.secret_key = "cart_savior"
app.register_blueprint(search_functions, url_prefix="")


# =========================================================================================
# =========================================================================================


cron = BackgroundScheduler()
cron.add_job(fill_db.fill_price_data, trigger="cron", hour='14', minute='00')
cron.start()

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