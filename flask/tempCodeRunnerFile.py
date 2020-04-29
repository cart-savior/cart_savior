	path_to_current_file = os.path.realpath(__file__)
	current_directory = os.path.split(path_to_current_file)[0]
	path_to_file = os.path.join(current_directory, "category_code.json")
	with open(path_to_file) as mydata:
		my_json_data = json.load(mydata)
	for item in my_json_data:
		keys.append(item['item_name'])
	return random.sample(keys, 3)