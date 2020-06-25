import json
import os
import sqlite3

def add_unit(item):
	conn = sqlite3.connect("cart_savior.db")
	c = conn.cursor()
	if item['item_name'] != "고등어":
		c.execute(
			"SELECT * FROM items_unit"
		)
		data = c.fetchall()
		result = [{
		'item_name' : item['item_name'],
		'unit' : data[0][1],
		'unit_price' : format(int(data[0][2] * item['item_price']), ",d")
		}]
	else :
		result = {
			'item_name' : item['item_name'],
			'unit' : item['kind_name'],
			'unit_price' : item['item_price']
		}
	return result
