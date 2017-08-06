from lxml import html
import requests
from bs4 import BeautifulSoup

netflix_id = 'ct%3DBQAOAAEBEHP92_x7BDSNQvSXhcAY8UuBwB53DwROu4fSFgYOOPdewaqmN4OKZA0ZTKGxKBd3ucJ5Zsk7sr76uzMqcAbrpxhzQHeoToRzJoICatgHLxGZYdIDvCaQ3iWiSB47bfrmN8Mirc8ARtEk5TqlPIDHhToQUossu8TS6NzLMgbtPYYhL9SDu-SozHALt1vU-ZHaKamgSugqhbuSmbMZYc91b1GX52hWVjLMbfUl9kUXJLK9io2MSR1qMvpF-nyt-EzbWr2CJirA52hgoYz0CBFgRK_ibVvvHTTr-NOF78UkPpLxgHwsXZ41ZdOx1HiLtXK3lQSiZs4rC8iZOzD_9g6nXWAItBUfoi8B_2DY0iOrLOPuLVamg4aA7UZE9ngeOahKw2wfFEYFqHSgUynq-ZqgvE-51G4Ei_6AB0oHT_dQB-JkrjlGLOO4He_xp21UEL_H1uMIKobOWDhI-xJYaQbf3FOYFBMTwPUQuKGlOkoXwkwKHAWSd52V3hnZUskN0DAt1zZeUxXi1HrnXOQyUoa7bSPtrNMAvLAnnxEBdPahQhXMbo7z9MpuWrsA0ruoJU0Yj_cJnJHg5NvcRJooeB8Iw1yeog7PAVYPawIu5_U7kFHED6Y.%26bt%3Ddbl%26ch%3DAQEAEAABABTlUPW_OYUq9IbQ2y9go0b3t9GPE4h_m_Y.%26v%3D2%26mac%3DAQEAEAABABRggfpqq4kw7WEKfK5cNNSFc6xOoUQBDSQ.'


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

# Add hulu and other sites later?


print(scrape_netflix("Rogue One: A Star Wars Story"))
#print(scrape_amazon('Fargo'))