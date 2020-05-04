import json
import os

def add_unit(name, price, kind_name):
	path_to_current_file = os.path.realpath(__file__)
	current_directory = os.path.split(path_to_current_file)[0]
	path_to_file = os.path.join(current_directory, "category_code.json")
	with open(path_to_file) as mydata:
		my_json_data = json.load(mydata)
	if name != "고등어":
		result = [{
		'item_name' : item['item_name'],
		'unit' : item['unit'],
		'unit_price' : format(int(item['ratio'] * price), ",d")
		}for item in my_json_data if name == item['item_name']][0]
	else :
		result = [{
			'item_name' : name,
			'unit' : kind_name,
			'unit_price' : price
		}]
	return result
