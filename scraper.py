import requests, json
from bs4 import BeautifulSoup

res = []
URL = "https://www.dunzo.com/"
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

soup_footer = soup.find_all("div", class_="sc-10mkyz7-0 sc-1felxgn-7 fVHOCS")[1]

data = soup_footer.find_all("a", class_="jxbqi7-0 sc-1felxgn-4 fMBqKg")
cities_url = list(map(lambda city: city['href'], data))


for city in cities_url:
	URL = "https://www.dunzo.com/"+city
	page = requests.get(URL)
	
	soup = BeautifulSoup(page.content, 'html.parser')

	data = {}
	data['city'] = soup.find("h1").text
	data['categories'] = []
	# categories = list(map(lambda category: category.get_text(), soup.find_all("p", class_="sc-1gu8y64-0 BbwkM blgsrr-3 bIstaM")))
	categories = soup.find_all("p", class_="sc-1gu8y64-0 BbwkM blgsrr-3 bIstaM")

	for category in categories:
		category_name = category.get_text()
		category_url = category.find_parent('a')['href']
		category_data = {}
		category_data['name'] = category_name
		category_data['stores'] = []

		URL = "https://www.dunzo.com/"+category_url
		page = requests.get(URL)
		soup = BeautifulSoup(page.content, 'html.parser')

		stores = soup.find_all('p', class_='sc-1gu8y64-0 BbwkM sc-1yp76rj-0 iSglrT')
		# category_data['stores'] = list(map(lambda store: store.text, stores))

		for store in stores:
			store_name = store.get_text()
			store_url = store.find_parent('a')['href']
			store_data = {}
			store_data['name'] = store_name
			store_data['products'] = []

			URL = "https://www.dunzo.com/"+store_url
			page = requests.get(URL)
			soup = BeautifulSoup(page.content, 'html.parser')

			products = soup.find_all('p', class_='sc-1gu8y64-0 hFuQhd sc-1twyv6b-0 kArLCp')
			for product in products:
				product_name = product.get_text()
				product_data = {}
				product_data['name'] = product_name

				product_price = product.next_sibling
				if product_price.get_text().startswith('₹'):
					product_price = product_price.get_text()
				elif product_price.next_sibling.get_text().startswith('₹'):
					product_price = product_price.next_sibling.get_text()
				elif product_price.next_sibling.next_sibling.get_text().startswith('₹'):
					product_price = product_price.next_sibling.next_sibling.get_text()

				product_data['price'] = product_price
				print(data['city']+ " =====> " + category_name)
				print(product_name+" =====> "+ product_price)
				store_data['products'].append(product_data)				

			category_data['stores'].append(store_data)

		data['categories'].append(category_data)
	print(data)
	res.append(data)

print(res)
with open('data.json', 'w') as file:
	json.dump(res, file, indent=4)
