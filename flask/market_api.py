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
		'price': format(product['price'], ",d"),
		'image' : product['thumbnail_image_url'],
		'link' : "https://www.kurly.com/shop/goods/goods_view.php?&goodsno=" + product['no']
		} for product in products][:2]
	return result

def get_ssg(item_name):
	req = requests.get('http://www.ssg.com/search.ssg?target=all&query='+ item_name)
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	name = [name.text for name in soup.select('div > a > em.tx_ko')[:2]]
	price = [price.text for price in soup.select('div > em')[:2]]
	image = [ "http:"+ image.get('src') for image in soup.select('div > a > img.i1')[:2]]
	link = ["http://ssg.com" + link.get('href') for link in soup.select('div.thmb > a')[:2]]
	result = [{
		'site' : "ssg",
		'name' : name[i],
		'price' : price[i],
		'image' : image[i],
		'link' : link[i]
		} for i in range(2)]
	return result

def get_hanaro(item_name):
	req = requests.get('http://www.nonghyupmall.com/BC1F010M/srchTotalList.nh?searchTerm_main=' + item_name + '%40undefined&CHAN_C=1102&chanC=1102')
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	name = [name.text for name in soup.select('div > a > p')][:2]
	price = [price.text[62:-53] for price in soup.select('div > p')][2:4]
	image = ['http://www.nonghyupmall.com/' + image.get('src') for image in soup.select('div.product-thumb > img')][:2]
	link = ['http://www.nonghyupmall.com/BC14010R/viewDetail.nh?wrsC=' + code.get('data-wrs-c') +'&basketCnt=0' for code in soup.select('div.product-info-area > a')][:2]
	result = [{
	    'site' : "hanaro",
	    'name' : name[i],
	    'price' : price[i],
	    'image' : image[i],
	    'link' : link[i]
	    } for i in range(2)]
	return result

def get_coupang(item_name):
	headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36"
	}
	url = "https://www.coupang.com/np/search?component=&q="+ item_name + "&channel=user"
	req = requests.get(url, headers=headers)
	html = req.text
	soup = BeautifulSoup(html, 'html.parser')
	name = [name.text for name in soup.select('div > div.name')][1:3]
	price = [price.text for price in soup.select('div > div.price > em > strong')[1:3]]
	image = ["http:"+ image.get('src') for image in soup.select('dt > img')[1:3]]
	link = ["https://www.coupang.com" + link.get('href') for link in soup.select('form > div > div > ul > li > a')][1:3]
	result = [{
		'site' : "coupang",
		'name' : name[i],
		'price' : price[i],
		'image' : image[i],
		'link' : link[i]
		} for i in range(2)]
	return result

def add_all_market(item_name):
	kurly = get_kurly(item_name)
	ssg = get_ssg(item_name)
	hanaro = get_hanaro(item_name)
	coupang = get_coupang(item_name)
	result = coupang + ssg + hanaro + kurly
	return result
