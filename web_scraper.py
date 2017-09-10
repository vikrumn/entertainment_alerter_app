from lxml import html
import requests
from bs4 import BeautifulSoup
import time

netflix_id = 'ct%3DBQAOAAEBEATp0bYq7WpJobwE2PxFi1GB0OFGe9fyVUGgEmMKudOmST2ospxDejcLabZb-a3zFhSIPmLL-LubOlcp18DC1Yp9IQXlyR-y6mOSGwjo5snK8SeWZT_z-w71QLKFhyjD8DxGi-IpD0DSTNQefMjFyNNV67Y-sXKb8o-J4bQjokQ-xBESCmMrVuJxaALTgveeeqd_jRGsQOoSIluQyKzsdqELELCbD_GTy3IyatEK9nUrINjfOXOvNg-PsTpF3Xou10c2iI0Ej1siUbvAvpBmoQFkBrGL5PisSMHdK6tNn01yNu6LCClx6UTzqothGEmyCJVydaX1JpwSSOPCN42-0YcDsBwOLkSJLW8FqF4Ips_qouQPjxmCDJ_e4Zwo2cO0o8NHbmo98vncxn1cz6SY0IAKXHppjRygwjEEucUN1SgLoBec1qIT-PZcrtXxukU38VEgLObxMD7Dafz7UV_Ix0bZrNN75eD1W4bKq5fXgpIyvCdRJA7kWquTvf1aTemdIyBzkZgjo9_rHIw_iR7vjkQJSnA6h8xZchCLU_i-79CRtSWmlkxfrrRxvZiDtB-_VrUp8TvS-0C7FJGWRX0fuGBVFd8evPKo8KHpz0HJ2lhNJ7p54rMuh0jkmUXxcdsS1buS%26bt%3Ddbl%26ch%3DAQEAEAABABQAaWFmKVnfQE_QTXzpHQwZOGaGPlFZ0k8.%26v%3D2%26mac%3DAQEAEAABABQmXZcAB1cgpvmlTl2g6utsyl_XbKPPxv0.'

def scrape_netflix(title):
	cookies = {'NetflixId' : netflix_id,
            'profilesNewSession' : '0',
            'profilesNewUser' : '0'
            }
	with requests.Session() as s:
	    response = s.get("https://www.netflix.com/search?q=" + title, cookies = cookies)
	search_results_page = BeautifulSoup(response.content, 'lxml')
	search_results_list = search_results_page.find_all('div', 'title-card-container')
	for result in search_results_list:
		if list(result.descendants)[0]['aria-label'].lower() == title.lower():
			return True
	return False

def scrape_amazon(title):
	response = requests.get('https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Dinstant-video&field-keywords=' + title)
	search_results_page = BeautifulSoup(response.content, 'lxml')
	search_results_list = list(search_results_page.find_all(text = title))
	if len(search_results_list) > 0:
		return True
	return False

def search_imdb(search_string):
	results_list = []
	search_string.replace(" ", "+") 
	with requests.Session() as s:
		response = s.get("http://www.imdb.com/find?ref_=nv_sr_fn&q=" + search_string + "&s=all")
	page = BeautifulSoup(response.content, 'lxml')
	x = page.find("div", { "class" : "findSection" })
	for elem in page.find("div", { "class" : "findSection" }).find_all('td', {"class" : 'result_text'}):
		results_list.append(elem.text)
	return results_list


# Add hulu and other sites later
if __name__ == '__main__':
	print(scrape_netflix("Rogue One: A Star Wars story"))