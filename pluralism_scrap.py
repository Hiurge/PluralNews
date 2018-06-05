import newspaper
from newspaper import Config, Article, Source

from bs4 import BeautifulSoup 
import urllib.request, urllib.parse, urllib.error 
import re 

pages_dict = {
	"tvn" : ["https://www.tvn24.pl/", "szukaj.html?q=", "+"],
	"tvp" : ["https://www.tvp.info/","szukaj?query=","%20"],
	"kry" : ["http://krytykapolityczna.pl/","szukaj/","+"],
	"jag" : ["http://jagiellonski24.pl/","wyszukiwanie/?pattern=","+"],
	"bus" : ["https://businessinsider.com.pl/","szukaj/?q=","+"],	
}

given_link = None
def link_into_keywords():
	pass

given_keywords = ["morawiecki","davos"] #test
target_news_feed_links = []
def open_target_news_feed(pages_dict, given_keywords):
	
	for key in pages_dict:
		link_tail = pages_dict[key][2].join(given_keywords)
		target_news_feed_link = (pages_dict[key][0] + pages_dict[key][1] + link_tail)
		target_news_feed_links.append(target_news_feed_link)

open_target_news_feed(pages_dict, given_keywords)


######### Linki na feedzie dla TVN
# Zobaczymy czy da sie to przeskalować na inne portale

import requests
from bs4 import BeautifulSoup

url = 'https://www.tvn24.pl/szukaj.html?q=morawiecki+davos'

page = requests.get(url) # target_news_feed_links[0]
soup = BeautifulSoup(page.text, 'html.parser')
tags = soup.find("div", {"class":'searchResult'})
tags = tags.find_all('a')

page_feed_links = []

for each in tags:
	next_link = (re.findall('href="(.*)">', str(each)))[0]
	page_feed_links.append(next_link)

good_feed_links = []
for each in page_feed_links:
	if each.startswith("http") and each.endswith(".html"):
		good_feed_links.append(each)
	
nr = 1
for each in good_feed_links:
	print(nr,". ",each)
	nr += 1


# for each in target_news_feed_links:
# 	my_page = each
# 	html_page = urllib.request.urlopen(my_page).read()
	# tags = BeautifulSoup(html_page, 'html.parser') 
	# tags = tags.find(id=portal_dict["id_results"])
	# tags = tags('article') 
			# else: 
			# 	tags = tags.findAll(portal_dict["tags_mod"][0], {portal_dict["tags_mod"][1] : portal_dict["tags_mod"][2]})
			# if portal_dict["model"] == "reed": REED_get_links_to_all_sub_pages(tags)
			# if portal_dict["model"] == "pracuj": PRACUJ_get_links_to_all_sub_pages(tags)
			# if portal_dict["model"] == "indeed": INDEED_get_links_to_all_sub_pages(tags,location) 
	# for tag in tags:
	# 	offer_desc = tag.findAll("div", { "class" : "metadata" })
	# 	offer_link = tag.findAll("a")
	# 	offer_link = (re.findall('href="(.*)"></a>', str(offer_link)))[0]
	# 	offer_job = re.findall('/jobs/(.*)/[0-9]', str(offer_link))
	# 	offer_job = (" ".join(str(offer_job[0]).split("-")))
	# 	offer_salary = re.findall('salary">(.*)</li>', str(offer_desc))
	# 	if "-" in str(offer_salary):
	# 		offer_salary_min = str(offer_salary).split("-")[0]
	# 		offer_salary_max = str(offer_salary).split("-")[1]
	# 	else:
	# 		offer_salary_min = str(offer_salary)	
	# 		offer_salary_max = str(offer_salary)
	# 	offer_salary = [(re.sub("\D", "", offer_salary_min)), (re.sub("\D", "", offer_salary_max))]
	# 	offer_location = str(re.findall('location">(.*)', str(offer_desc))[0])
	# 	offer_info = [offer_link, offer_job, offer_location, offer_salary]
	# 	offer_info_list.append(offer_info)






