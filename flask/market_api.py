import requests
from bs4 import BeautifulSoup
#item_name = '쌀'

def get_kurly(item_name):
	req = requests.get('https://api.kurly.com/v1/search?keyword="' + item_name + '"&sort_type=-1&page_limit=99&page_no=1&delivery_type=0&ver=1588412210623')
	data = req.json()
	products = data['data']['products']
	result = [{
		'site' : "kurly",
		'name' : product['name'],
		'price': product['price'],
		'image' : product['thumbnail_image_url'],
		'link' : "https://www.kurly.com/shop/goods/goods_view.php?&goodsno=" + product['no']
		} for product in products][:3]
	return result

def get_ssg(item_name):
	req = requests.get('http://www.ssg.com/search.ssg?target=all&query='+ item_name)
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	name = [name.text for name in soup.select('div > a > em.tx_ko')[:3]]
	price = [price.text + "원" for price in soup.select('div > em')[:3]]
	image = [ "http:"+ image.get('src') for image in soup.select('div > a > img.i1')[:3]]
	link = ["ssg.com" + link.get('href') for link in soup.select('div.thmb > a')[:3]]
	result = [{
		'site' : "ssg",
		'name' : name[i],
		'price' : price[i],
		'image' : image[i],
		'link' : link[i]
		} for i in range(3)]
	return result

def add_kurly_ssg(item_name):
	kurly = get_kurly(item_name)
	ssg = get_ssg(item_name)
	return kurly + ssg
