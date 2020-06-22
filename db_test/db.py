import sqlite3

conn = sqlite3.connect("cart_savior.db")
c = conn.cursor()

def create_items_table():
	c.execute(
		'CREATE TABLE items('
		'id INTEGER PRIMARY KEY AUTOINCREMENT,'
		'item_name TEXT,'
		'category_code INTEGER,'
		'item_code INTEGER,'
		'unit TEXT,'
		'ratio REAL)'
		)

def input_data_items(item_name, category_code, item_code, unit, ratio):
	c.execute(
		"INSERT INTO items(item_name, category_code, item_code, unit, ratio) VALUES(?, ?, ?, ?, ?)",
		(item_name, category_code, item_code, unit, ratio)
	)
	conn.commit()

# def input_data_items():
# 	c.execute(
# 		'INSERT INTO items(item_name, category_code, item_code, unit, ratio) '
# 		'VALUES(\'쌀\', 100, 111, \'1kg\', 0.05)'
# 	)
# 	conn.commit()
# 	c.close()

# create_items_table()
input_data_items('찹쌀', 100, 112, '100g', 0.1)
# input_data_items()
