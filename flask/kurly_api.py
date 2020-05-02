import requests
item_name = '쌀'

def get_kurly(item_name):
	req = requests.get('https://api.kurly.com/v1/search?keyword="' + item_name + '"&sort_type=-1&page_limit=99&page_no=1&delivery_type=0&ver=1588412210623')
	data = req.json()
	products = data['data']['products']
	result = [{
		'name' : product['name'],
		'price': product['price'],
		'image' : product['thumbnail_image_url'],
		'link' : "https://www.kurly.com/shop/goods/goods_view.php?&goodsno=" + product['no']
		} for product in products][:3]
	return result

print(get_kurly(item_name))
