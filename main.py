import time
from flask import Flask,render_template,request,redirect,url_for
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--headless')

driver = webdriver.Chrome(options=chrome_options)

searchUrlList = [["https://www.shoppersdrugmart.ca/en/search?query=REPLACE_WITH_OBJECT", "vue-widget-search-listing-products__item"]] 
xpathList = ['//*[@id="module-search-landing"]/div/div/div[1]/article/div/ul/li[1]', '//*[@id="module-search-landing"]/div/div/div[1]/article/div/ul/li[2]', '//*[@id="module-search-landing"]/div/div/div[1]/article/div/ul/li[3]']
resultList = []
items = []

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():
	if request.method == 'POST':
		e = request.form['input']
		print("redirecting...")
		return redirect('/search/' + e + '/')
	return render_template('home_page.html')

@app.route('/search/<string:input>/')
def input(input):
	resultList.clear()
	object = input
	for i in range (len(searchUrlList)):
		search = searchUrlList[i][0]
		print(i)
		search = search.replace("REPLACE_WITH_OBJECT", object)

		driver.get(search)
		time.sleep(1)
		elements = driver.find_elements("xpath", xpathList[3*i])
		items.append(elements[0].get_attribute("innerHTML").split("<a href=\"")[1].split("\" target=\"")[0])
		elements = driver.find_elements("xpath", xpathList[1+(3*i)])
		items.append(elements[0].get_attribute("innerHTML").split("<a href=\"")[1].split("\" target=\"")[0])
		elements = driver.find_elements("xpath", xpathList[2+(3*i)])
		items.append(elements[0].get_attribute("innerHTML").split("<a href=\"")[1].split("\" target=\"")[0])

		print(items)

	i = 0
	
	for item in items:
		driver.get(item)
	#	time.sleep(5)

		nameXPath = ""
		priceXPath = ""
		store = ""

		if i < 3:
			nameXPath = '//*[@id="main-content"]/div[2]/div[1]/div/h1'
			priceXPath = '//*[@id="main-content"]/div[2]/div[2]/p[1]/span'
			store = "Shoppers Drug Mart"
		
		nameElements = driver.find_elements("xpath", nameXPath)
		name = nameElements[0].get_attribute("innerHTML")
	
		priceElements = driver.find_elements("xpath", priceXPath)
		price = priceElements[0].get_attribute("innerHTML")

		priceNum = float(price.split("$")[1])
		
		p = {
			"name": name,
			"price": price,
			"priceNum": priceNum,
			"link": item,
			"store": store
		}
		
		i+=1
		
		resultList.append(p)
		print(p)

	resultList.sort(key=sortFn)
	print(resultList)
	return render_template('search_page.html', data=resultList)

def sortFn(dict):
	return dict['priceNum']
	
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}


app.run(host = '0.0.0.0', port = 81)