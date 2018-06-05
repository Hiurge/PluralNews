from bs4 import BeautifulSoup
import requests
import time
import re
from random import randint

keywords = None # User input / from link
keywords = "AI polska" # Test
keywords = "+".join(keywords.split(" "))

def scrape_news_from_google(s):
	time.sleep(randint(0, 2))
	r = requests.get("http://www.google.pl/search?q="+s+"&tbm=nws")
	print("Searching for: ", s)
	print("Status code: ", r.status_code)
	content = r.text 
	print(content)
	news_link = []
	soup = BeautifulSoup(content, "html.parser")
	href_divs = soup.findAll("h3", {"class": "r"})
	print(href_divs)
	for href_div in href_divs:
		print(href_div)
		href_div = (re.findall('q=(.*)">', str(href_div)))[0]
		print(href_div) 
		# href_div = href_div.split("&amp")  # 503 wyjebalo i nie moge tego przetestowac xD raczej dziala
		# href_div = href_div[0]
		news_link.append(href_div)

	news_summaries = []
	soup = BeautifulSoup(content, "html.parser")
	st_divs = soup.findAll("div", {"class": "st"})
	for st_div in st_divs: 
		st_div = st_div.text.rstrip('...')
		news_summaries.append(st_div)

	news_source = []
	news_date = []
	soup = BeautifulSoup(content, "html.parser")
	slp_divs = soup.findAll("div", {"class": "slp"})
	for slp_div in slp_divs: 
		slp_div_source = re.findall('f">([^\s]+)', str(slp_div))[0]
		news_source.append(slp_div_source)
		slp_div_date = re.findall(' - (.*)</s', str(slp_div))[0]
		news_date.append(slp_div_date)

	news_title = []
	soup = BeautifulSoup(content, "html.parser")
	r_divs = soup.findAll("h3", {"class": "r"})
	for r_div in r_divs:
		r_div = r_div.text.rstrip('...')
		news_title.append(r_div)

	search_info = []
	news_number = 10 # expand it
	for num in range(0,(news_number)):
		search_info.append([news_title[num], news_source[num], news_date[num], news_summaries[num], news_link[num]])
	
	return search_info

# We store search_info for each search type here. n = news nr
	# TITLE    =  tvn_search[n][0]
	# SOURCE   =  tvn_search[n][1] 
	# DATE     =  tvn_search[n][2]
	# SUMMARY  =  tvn_search[n][3] 
	# LINK  =     tvn_search[n][4]

#all_search = scrape_news_from_google(keywords) 
tvn_search = scrape_news_from_google((keywords+"+tvn24.pl"))
#tvp_search = scrape_news_from_google((keywords+"+tvp.info"))
#kry_search = scrape_news_from_google((keywords+"+krytykapolityczna.pl"))
#jag_search = scrape_news_from_google((keywords+"+jagiellonski24.pl"))
#bus_search = scrape_news_from_google((keywords+"+businessinsider.com.pl"))
# add more, yes

# Extract text, if possible, extract specificly headline and first paragraph and or text: 
def extract_text_from_one_news(news_link):
	
	time.sleep(randint(0, 2))
	r = requests.get(news_link) 
	print("Status code: ", r.status_code)
	content = r.text 

	news_soup = BeautifulSoup(content, 'html.parser')
	for script in news_soup(["script", "style"]):
		script.extract()

	news_soup = BeautifulSoup(content, 'html.parser')
	for script in news_soup(["script", "style"]):
		script.extract()

	text = news_soup.get_text()
	lines = (line.strip() for line in text.splitlines())
	
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
	def chunk_space(chunk):
		chunk_out = chunk + ' '
		return chunk_out
	
	text = ''.join(chunk_space(chunk) for chunk in chunks if chunk).encode('utf-8') # Get rid of all blank lines and ends of line
	text = text.decode('utf-8')
	print(text)
	text = re.sub("[^A-Za-zżźćńółęąśŻŹĆĄŚĘŁÓŃ.+3]"," ", text)
	
	clean_news_text = text
	#clean_news_text = text.lower().split()    # Trzeba pomyslec jaki tekst chcemy dostać

	return clean_news_text

#Testy:
news_link = "https://www.tvn24.pl/rex-tillersona-i-jacek-czaputowicz-o-relacjach-polski-i-usa,809936,s.html"
words_from_one_news = extract_text_from_one_news(news_link)
print(words_from_one_news)








#######################################################################################################
#
# 	EXAMPLE OUTPUT
#
#	Delete this later.
#
#
#
# nr = 1
# for n in all_search:
# 	print(str(nr)+". \n","Title:",n[0], "\n","Source:",n[1], "\n","Date:",n[2],"\n","Summary:",n[3], "\n","Link:", n[4], "\n")
# 	nr += 1

# nr = 1
# for n in tvn_search:
# 	print(str(nr)+". \n","Title:",n[0], "\n","Source:",n[1], "\n","Date:",n[2],"\n","Summary:",n[3], "\n","Link:", n[4], "\n")
# 	nr += 1

# nr = 1
# for n in tvp_search:
# 	print(str(nr)+". \n","Title:",n[0], "\n","Source:",n[1], "\n","Date:",n[2],"\n","Summary:",n[3], "\n","Link:", n[4], "\n")
# 	nr += 1

# nr = 1
# for n in kry_search:
# 	print(str(nr)+". \n","Title:",n[0], "\n","Source:",n[1], "\n","Date:",n[2],"\n","Summary:",n[3], "\n","Link:", n[4], "\n")
# 	nr += 1

# nr = 1
# for n in jag_search:
# 	print(str(nr)+". \n","Title:",n[0], "\n","Source:",n[1], "\n","Date:",n[2],"\n","Summary:",n[3], "\n","Link:", n[4], "\n")
# 	nr += 1

# nr = 1
# for n in bus_search:
# 	print(str(nr)+". \n","Title:",n[0], "\n","Source:",n[1], "\n","Date:",n[2],"\n","Summary:",n[3], "\n","Link:", n[4], "\n")
# 	nr += 1

# # Zwraca:

# 1. 
#  Title: Polska szuka sojuszników w Davos. Premier chce powstania  
#  Source: BusinessInsider 
#  Date: 2 dni temu 
#  Summary: Głównym celem wizyty premiera Mateusza Morawieckiego na Forum Ekonomicznym w Davos jest szukanie sojuszników przy sprawach związanych chociażby z bezpieczeństwem - w tym także gazowym. Zdaniem premiera, świat potrzebuje też nowego ładu dla setek milionów ludzi na całym świecie 
#  Link: https://businessinsider.com.pl/wiadomosci/morawiecki-w-davos-bezpieczenstwo-gaz-nowy-lad/5mpc5f7&amp;sa=U&amp;ved=0ahUKEwi6mO20nPnYAhXLMywKHfczAeYQqQIIFCgAMAA&amp;usg=AOvVaw3NAdjhAFqPhpvvtaQ6DPfG 

# 2. 
#  Title: Premier Morawiecki właśnie określił, kiedy wejdziemy do strefy euro  
#  Source: BusinessInsider 
#  Date: 3 dni temu 
#  Summary: Wszystko jasne. Premier Morawiecki w wywiadzie dla Bloomberg TV w Davos powiedział, że Polska wejdzie do strefy euro, kiedy osiągnie dochód rozporządzalny na poziomie 80-90 proc. najbogatszych krajów UE. Pytani przez nas ekonomiści odczytują tę wypowiedź jasno. - Czyli raczej nigdy - mówi z  
#  Link: https://businessinsider.com.pl/finanse/davos-kiedy-polska-wejdzie-do-strefy-euro-mowi-mmorawiecki/n6t14jw&amp;sa=U&amp;ved=0ahUKEwi6mO20nPnYAhXLMywKHfczAeYQqQIIHSgAMAE&amp;usg=AOvVaw1n531rCrHN4G7PZR22n188 

# 3. 
#  Title: W Davos Duda i Morawiecki „promują” Polskę pod swoimi rządami 
#  Source: Polityka.pl 
#  Date: 1 dzień temu 
#  Summary: W Davos Duda i Morawiecki „promują” Polskę pod swoimi rządami. Dobrze, że prezydent i premier szukają w Davos sojuszników, tylko czemu wcześniej żyrowali działania, które utrudniają ich znalezienie? Andrzej Duda i Mateusz ... Panowie Duda i Morawiecki wykonali zadanie. „Promowali” Polskę pod  
#  Link: https://www.polityka.pl/tygodnikpolityka/swiat/1735692,1,w-davos-duda-i-morawiecki-promuja-polske-pod-swoimi-rzadami.read&amp;sa=U&amp;ved=0ahUKEwi6mO20nPnYAhXLMywKHfczAeYQqQIIIygAMAI&amp;usg=AOvVaw2CO8g35tXro4h8pcm4ngMI 

# 4. 
#  Title: Kompromitacja w Davos? Morawiecki musiał się zdziwić, gdy  
#  Source: naTemat 
#  Date: 4 dni temu 
#  Summary: Polskimi przedstawicielami na tegorocznym spotkaniu w szwajcarskim Davos są m.in. Mateusz Morawiecki i prezydent Andrzej Duda. Jednak spotkania i konferencje, dyskusje jeszcze się na dobre nie rozpoczęły, a wyjazd w Alpy już nie będzie udany. A to za sprawą pierwszej strony rozdawanej każdemu  
#  Link: http://natemat.pl/228061,kompromitacja-w-davos-morawiecki-zobaczyl-okladke-prestizowego-pisma&amp;sa=U&amp;ved=0ahUKEwi6mO20nPnYAhXLMywKHfczAeYQqQIIJigAMAM&amp;usg=AOvVaw1fViCj-up6AA-BeL4BIbDi 

# 5. 
#  Title: Davos zmaga się z kryptowalutami. Niebezpieczeństwo dostrzega  
#  Source: Gazeta 
#  Date: 2 dni temu 
#  Summary: Z kolei premier Mateusz Morawiecki ujawnił w rozmowie z RMF FM, że powołał zespół złożony z przedstawicieli odpowiednich ministerstw, Urzędu Ochrony Konkurencji i Konsumentów czy Komisji Nadzoru Finansowego, który w ciągu miesiąca ma opracować rekomendacje konkretnych działań mających  
#  Link: http://wyborcza.pl/7,155287,22943984,davos-zmaga-sie-z-kryptowalutami-niebezpieczenstwo-dostrzega.html&amp;sa=U&amp;ved=0ahUKEwi6mO20nPnYAhXLMywKHfczAeYQqQIILygAMAQ&amp;usg=AOvVaw3pNA3ofi47PjICtWX9mGcU 

# 6. 
#  Title: Morawiecki powołał zespół ds. niebezpiecznych instrumentów  
#  Source: Wprost.pl 
#  Date: 2 dni temu 
#  Summary: Ten zespół za miesiąc dokładnie ma przestawić listę swoich rekomendacji, jak ograniczać ryzyko związane z tego typu różnymi schematami – wyjaśnił Morawiecki. Premier skomentował również swoją obecność na Światowym Forum Ekonomicznym w Davos. Jego zdaniem chodzi tutaj o promocję kraju 
#  Link: https://www.wprost.pl/kraj/10100134/morawiecki-powolal-zespol-ds-niebezpiecznych-instrumentow-finansowych.html&amp;sa=U&amp;ved=0ahUKEwi6mO20nPnYAhXLMywKHfczAeYQqQIINygAMAU&amp;usg=AOvVaw2DK2WNt9whBJkhtR2HKNMp 

# 7. 
#  Title: Morawiecki w Davos: Spotkania m.in. z Perrym i Rasmussenem 
#  Source: Interia 
#  Date: 4 dni temu 
#  Summary: Światowe Forum Ekonomiczne (WEF), które po raz 48. odbywa się w szwajcarskim Davos, ponownie przyciągnęło liderów współczesnego świata, szeroką reprezentację polityków, przedstawicieli organizacji pozarządowych i biznesu, którzy wspólnie będą szukać odpowiedzi na ważne w ostatnich latach  
#  Link: http://fakty.interia.pl/news-morawiecki-w-davos-spotkania-m-in-z-perrym-i-rasmussenem,nId,2511892&amp;sa=U&amp;ved=0ahUKEwi6mO20nPnYAhXLMywKHfczAeYQqQIIOigAMAY&amp;usg=AOvVaw0-4E8RcqCh4jVbr3_SvQsb 

# 8. 
#  Title: Mateusz Morawiecki i sekretarz energii USA Rickiem Perrym  
#  Source: WNP.PL 
#  Date: 3 dni temu 
#  Summary: Premier Mateusz Morawiecki spotkał się w trakcie Światowego Forum Ekonomicznego w Davos z sekretarzem energii USA Rickiem Perrym. ... Jak poinformowała Kancelaria Prezesa Rady Ministrów, Mateusz Morawiecki omówił z przedstawicielem administracji Donalda Trumpa polskie oczekiwania  
#  Link: http://gazownictwo.wnp.pl/mateusz-morawiecki-i-sekretarz-energii-usa-rickiem-perrym-rozmawiali-w-davos,315980_1_0_0.html&amp;sa=U&amp;ved=0ahUKEwi6mO20nPnYAhXLMywKHfczAeYQqQIIPSgAMAc&amp;usg=AOvVaw1_1-xGZRKRS7Xwtdk_N31B 

# 9. 
#  Title: Morawiecki w Davos o działaniach ws. luki w VAT: niech Unia bierze  
#  Source: Niezalezna.pl 
#  Date: 3 dni temu 
#  Summary: "Ale brakuje jeszcze tej masy krytycznej do zrozumienia, także przez przedstawicieli rajów podatkowych, którzy przyjeżdżają do Davos, że jest to niezdrowe podejście, niezdrowe eksploatowanie innych" - powiedział Morawiecki. Premier powiedział też, że z ostatnich danych wynika, że wpływy VAT w 2017  
#  Link: https://niezalezna.pl/215076-morawiecki-w-davos-o-dzialaniach-ws-luki-w-vat-niech-unia-bierze-przyklad-z-polski&amp;sa=U&amp;ved=0ahUKEwi6mO20nPnYAhXLMywKHfczAeYQqQIIQigAMAg&amp;usg=AOvVaw0WIOg0xEjQqgPI8xT4mQ1l 

# 10. 
#  Title: FAZ: Mateusz Morawiecki – „Anty-Macron z Polski” 
#  Source: Rzeczpospolita 
#  Date: 5 godz. temu 
#  Summary: Nawiązując do wystąpienia polskiego premiera w Davos, Astheimer pisze, że Morawiecki „przystąpił do kontrataku” mówiąc o krajach stosujących praktyki protekcjonistyczne. Celem Polski jest realizacja swobody usług, co przyczyni się do wzrostu konkurencyjności całej Unii i jest dobre dla wszystkich  
#  Link: http://www.rp.pl/Polityka/180129374-FAZ-Mateusz-Morawiecki--Anty-Macron-z-Polski.html&amp;sa=U&amp;ved=0ahUKEwi6mO20nPnYAhXLMywKHfczAeYQqQIISSgAMAk&amp;usg=AOvVaw3RSC1rQmoVHGJvI223ZKdJ 

# 1. 
#  Title: Premier o sporze z Unią. "Musimy zmienić sądownictwo dużo  
#  Source: TVN24 
#  Date: 3 dni temu 
#  Summary: Na drodze dialogu przedstawiciele polskich władz tłumaczą europejskim partnerom znaczenie reform w Polsce - przekonywał premier Mateusz Morawiecki w rozmowie z agencją Bloomberga. Szef rządu, podobnie jak prezydent Andrzej Duda, bierze udział w Forum Ekonomicznym w Davos. - W dialogu  
#  Link: https://www.tvn24.pl/wiadomosci-ze-swiata,2/premier-morawiecki-komentuje-w-davos-spor-z-komisja-europejska,809022.html&amp;sa=U&amp;ved=0ahUKEwjDvIm1nPnYAhVGFywKHeHfDJ4QqQIIFCgAMAA&amp;usg=AOvVaw16fgXx_J4Y-SutqKcu8NE6 

# 2. 
#  Title: Morawiecki odpytany o migrantów. "To nie tak, że nie pomagamy. To  
#  Source: TVN24 
#  Date: 1 dzień temu 
#  Summary: To tylko kwestia perspektywy - w ten sposób Mateusz Morawiecki bronił w wywiadzie dla CNN braku zgody Polski na przyjmowanie imigrantów z Bliskiego Wschodu. Zapewniał, że "zwiększamy wysiłki, by zajmować się problemami tam, gdzie występują". Przebywający na szczycie w Davos polski premier  
#  Link: https://www.tvn24.pl/wiadomosci-z-kraju,3/premier-o-migrantach-z-bliskiego-wschodu-w-wywiadzie-dla-cnn,809597.html&amp;sa=U&amp;ved=0ahUKEwjDvIm1nPnYAhVGFywKHeHfDJ4QqQIIFygAMAE&amp;usg=AOvVaw1DWxAcV0GCZ_0Bn-vN72WA 

# 3. 
#  Title: Morawiecki chciałby, aby Wielka Brytania była częścią Unii  
#  Source: TVN24 
#  Date: 2 dni temu 
#  Summary: Wciąż mam niewielką nadzieję, że jest jakiś sposób, który pozwoliłby Wielkiej Brytanii być częścią Unii Europejskiej – powiedział premier Mateusz Morawiecki w wywiadzie, jakiego udzielił w środę BBC w kuluarach Światowego Forum Ekonomicznego w Davos. Morawiecki zaznaczył w swej wypowiedzi,  
#  Link: http://tvn24bis.pl/ze-swiata,75/premier-mateusz-morawiecki-o-brexicie-w-davos,809268.html&amp;sa=U&amp;ved=0ahUKEwjDvIm1nPnYAhVGFywKHeHfDJ4QqQIIGigAMAI&amp;usg=AOvVaw2CzkvrUU8d0M6Uh4k244fw 

# 4. 
#  Title: Ruszył szczyt w Davos. Napięty grafik Dudy i Morawieckiego 
#  Source: TVN24 
#  Date: 4 dni temu 
#  Summary: Prezydent Andrzej Duda jest w Szwajcarii, gdzie bierze udział w Światowym Forum Ekonomicznym w Davos. Będzie uczestniczył w debatach na temat Europy Środkowej oraz Bliskiego Wschodu; spotka się m.in. z prezesem Google'a i królem Jordanii. W szczycie uczestniczy też premier Mateusz  
#  Link: http://tvn24bis.pl/ze-swiata,75/prezydent-duda-przylecial-do-szwajcarii-wezmie-udzial-w-forum-w-davos,808798.html&amp;sa=U&amp;ved=0ahUKEwjDvIm1nPnYAhVGFywKHeHfDJ4QqQIIHSgAMAM&amp;usg=AOvVaw36louXSlr5uZV5NPanNUd9 

# 5. 
#  Title: Budapeszt, Davos i Bruksela. Styczniowy kalendarz dyplomatyczny  
#  Source: TVN24 
#  Date: 29 Gru 2017 
#  Summary: Poza Budapesztem i Brukselą, premier Mateusz Morawiecki odwiedzi w styczniu również Davos - mówił w piątek w radiowej Jedynce wicemarszałek Senatu Adam Bielan, pytany o plany polskiej dyplomacji na najbliższy czas. W czwartek minister spraw zagranicznych Witold Waszczykowski poinformował,  
#  Link: https://www.tvn24.pl/wiadomosci-z-kraju,3/bielan-morawiecki-odwiedzi-budapeszt-davos-i-bruksele,802196.html&amp;sa=U&amp;ved=0ahUKEwjDvIm1nPnYAhVGFywKHeHfDJ4QqQIIICgAMAQ&amp;usg=AOvVaw0aGtpKPhHP6PB_QZsH0MI1 

# 6. 
#  Title: Duda spotkał się z Trumpem. "Potwierdzili swoją wzajemną osobistą  
#  Source: TVN24 
#  Date: 1 dzień temu 
#  Summary: Prezydent Andrzej Duda spotkał się z prezydentem USA Donaldem Trumpem podczas Światowego Forum Ekonomicznego w Davos - poinformował szef ... koncernów, szefów organizacji pozarządowych i znanych osobistości, wśród nich są prezydent Andrzej Duda i premier Mateusz Morawiecki, a także  
#  Link: https://www.tvn24.pl/wiadomosci-ze-swiata,2/spotkanie-dudy-i-trumpa-w-davos-prezydenci-rozmawiali-na-szczycie,809656.html&amp;sa=U&amp;ved=0ahUKEwjDvIm1nPnYAhVGFywKHeHfDJ4QqQIIIygAMAU&amp;usg=AOvVaw04r6E2bVedgpKgQCh7DDQ_ 

# 7. 
#  Title: Morawiecki w wywiadzie dla "Die Welt": nie ustąpimy w sporze z  
#  Source: TVN24 
#  Date: 2 dni temu 
#  Summary: Wyboru Sędziów (Richterwahlausschuss) - pisze jednak "Die Welt". "Zasiadają w niej wyłącznie politycy. Niemcy nie stosują się (tym samym) do zaleceń Komisji Weneckiej Rady Europy" - cytuje Morawieckiego w rozmowie przeprowadzonej w kuluarach Światowego Forum Ekonomicznego (WEF) w Davos  
#  Link: https://www.tvn24.pl/wiadomosci-ze-swiata,2/morawiecki-w-die-welt-nie-ustapimy-w-sporze-z-bruksela,809318.html&amp;sa=U&amp;ved=0ahUKEwjDvIm1nPnYAhVGFywKHeHfDJ4QqQIIJigAMAY&amp;usg=AOvVaw0DxE2NJ_bIMpFoJN0F-uA1 

# 8. 
#  Title: Morawiecki w rozmowie z Merkel "nie będzie unikać" kwestii reparacji 
#  Source: TVN24 
#  Date: 2 dni temu 
#  Summary: Jak dodał, kwestię odszkodowań trzeba "bardzo dobrze policzyć". Morawiecki, który uczestniczy w Światowym Forum Ekonomicznym w Davos, w środę otrzymał zaproszenie na spotkanie z kanclerz Niemiec Angelą Merkel. Jak poinformowało Centrum Informacyjne Rządu, rozmowa odbędzie się 15 lutego  
#  Link: https://www.tvn24.pl/wiadomosci-z-kraju,3/morawiecki-nie-wyklucza-rozmowy-z-merkel-o-reparacjach-wojennych,809305.html&amp;sa=U&amp;ved=0ahUKEwjDvIm1nPnYAhVGFywKHeHfDJ4QqQIIKSgAMAc&amp;usg=AOvVaw371ytWzWCqxuAAo8hZ-h9K 

# 9. 
#  Title: "Zagrożenie dla bezpieczeństwa w regionie". Premier po spotkaniu  
#  Source: TVN24 
#  Date: 3 dni temu 
#  Summary: Zgadzamy się, że gazociąg Nord Stream 2 jest zagrożeniem dla bezpieczeństwa w regionie - powiedział w środę premier Mateusz Morawiecki po spotkaniu w Davos z sekretarzem energii USA Rickiem Perry. - Rozmawialiśmy o tym, by Polska stawała się coraz bardziej bezpiecznym węzłem dystrybucji  
#  Link: http://tvn24bis.pl/surowce,78/premier-morawiecki-o-nord-stream-2,809180.html&amp;sa=U&amp;ved=0ahUKEwjDvIm1nPnYAhVGFywKHeHfDJ4QqQIILCgAMAg&amp;usg=AOvVaw0j3p-akoDMM-_GmdrH010I 

# 10. 
#  Title: "Paleta tematów była bardzo szeroka". Godzinna rozmowa Dudy i  
#  Source: TVN24 
#  Date: 1 dzień temu 
#  Summary: Tillerson opuścił Belweder około godziny 21.30. Szef amerykańskiej dyplomacji przyleciał do Warszawy wprost ze Światowego Forum Ekonomicznego w Davos, na którym obecny był także polski prezydent. W sobotę rano z sekretarzem stanu USA będą rozmawiali premier Mateusz Morawiecki i minister  
#  Link: https://www.tvn24.pl/wiadomosci-z-kraju,3/sekretarz-stanu-usa-rex-tillerson-w-polsce,809573.html&amp;sa=U&amp;ved=0ahUKEwjDvIm1nPnYAhVGFywKHeHfDJ4QqQIILygAMAk&amp;usg=AOvVaw06ONq_Mm88PMc-26nein0X 

# 1. 
#  Title: Premier i prezydent w Davos. „Chcę pokazać, że nasz model  
#  Source: TVP 
#  Date: 4 dni temu 
#  Summary: Podczas Światowego Forum Ekonomicznego w Davos premier Mateusz Morawiecki spotka się m.in. z sekretarzem USA do spraw energii, premierami: Norwegii, Danii i Holandii oraz szefami takich firm jak Google czy ArcelorMittal - podało we wtorek Centrum Informacyjne Rządu 
#  Link: https://www.tvp.info/35721497/premier-i-prezydent-w-davos-chce-pokazac-ze-nasz-model-gospodarczy-dziala&amp;sa=U&amp;ved=0ahUKEwj7p-C1nPnYAhWxh6YKHboTAJ8QqQIIFCgAMAA&amp;usg=AOvVaw1iUl0z3FUOKakC8j2U6PcE 

# 2. 
#  Title: Premier: W Davos dostrzeżono fakt zmniejszania się nierówności w  
#  Source: TVP 
#  Date: 3 dni temu 
#  Summary: Mówimy o walce z rajami podatkowymi, o naszych sukcesach w związku z uszczelnieniem systemu podatkowego, jako przykład działania dla dobra społeczeństwa wsi, miasteczek czy miast powiatowych – tak premier Mateusz Morawiecki przedstawiał w „Gościu Wiadomości” efekty swojej wizyty na forum 
#  Link: http://www.tvp.info/35737215/premier-w-davos-dostrzezono-fakt-zmniejszania-sie-nierownosci-w-polsce&amp;sa=U&amp;ved=0ahUKEwj7p-C1nPnYAhWxh6YKHboTAJ8QqQIIHSgAMAE&amp;usg=AOvVaw0G9eKa9xRCj9LDxQPF_ulX 

# 3. 
#  Title: Premier: Zagrożenie ze strony Rosji traktuję jako największe  
#  Source: TVP 
#  Date: 6 godz. temu 
#  Summary: Traktuję w taki sposób zagrożenie ze strony Rosji – tak premier Mateusz Morawiecki wywiadzie dla „Politico” odpowiedział na pytanie o największe dziś, według niego, zagrożenie dla Polski. Skrytykował też plan budowy ... Szef rządu udzielił wywiadu podczas forum w Davos. Był pytany m.in. o największe  
#  Link: https://www.tvp.info/35781335/premier-zagrozenie-ze-strony-rosji-traktuje-jako-najwieksze-zagrozenie-dla-polski&amp;sa=U&amp;ved=0ahUKEwj7p-C1nPnYAhWxh6YKHboTAJ8QqQIIJigAMAI&amp;usg=AOvVaw2BwxLv2YkHkqvMaPgkv3F- 

# 4. 
#  Title: Premier Morawiecki: Wierzę, że jest sposób, by Wielka Brytania  
#  Source: TVP 
#  Date: 2 dni temu 
#  Summary: Premier Mateusz Morawiecki spotkał się m.in. z amerykańskim sekretarzem ds. energii Rickiem Perrym (fot. ... Na zakończenie pierwszego dnia Światowego Forum Ekonomicznego w Davos premier Mateusz Morawiecki uczestniczył w kolacji z inwestorami i przedstawicielami rządów USA i Wielkiej Brytanii  
#  Link: https://www.tvp.info/35738454/premier-morawiecki-wierze-ze-jest-sposob-by-wielka-brytania-zachowala-wiezi-z-ue&amp;sa=U&amp;ved=0ahUKEwj7p-C1nPnYAhWxh6YKHboTAJ8QqQIIKSgAMAM&amp;usg=AOvVaw1Hnr2d1RQ_FrpBVk02eARg 

# 5. 
#  Title: Morawiecki w „Die Welt”: polskie sądownictwo bardziej niezawisłe  
#  Source: TVP 
#  Date: 2 dni temu 
#  Summary: Premier Mateusz Morawiecki twierdzi, że Polska nie zamierza ustępować w sporze z UE ws. reformy sądownictwa (fot. ... samym) do zaleceń Komisji Weneckiej Rady Europy – powiedział szef polskiego rządu w rozmowie przeprowadzonej w kuluarach Światowego Forum Ekonomicznego (WEF) w Davos 
#  Link: https://www.tvp.info/35749086/morawiecki-w-die-welt-polskie-sadownictwo-bardziej-niezawisle-niz-niemieckie&amp;sa=U&amp;ved=0ahUKEwj7p-C1nPnYAhWxh6YKHboTAJ8QqQIILCgAMAQ&amp;usg=AOvVaw3pt3b3FtWZEpszmWXwXcwh 

# 6. 
#  Title: Premier o „kontroli nad sądownictwem”: Tyle w tym prawdy, ile lodu  
#  Source: TVP 
#  Date: 2 dni temu 
#  Summary: Premier Mateusz Morawiecki, który uczestniczy w Światowym Forum Ekonomicznym w Davos, mówił w wywiadzie dla CNN o podejściu Polski do kwestii uchodźców; akcentował przy tym zaangażowanie naszego kraju w pomoc na miejscu. Szef polskiego rządu wyjaśnił też, o co chodzi w polskiej reformie  
#  Link: https://www.tvp.info/35754625/premier-o-kontroli-nad-sadownictwem-tyle-w-tym-prawdy-ile-lodu-na-saharze&amp;sa=U&amp;ved=0ahUKEwj7p-C1nPnYAhWxh6YKHboTAJ8QqQIILygAMAU&amp;usg=AOvVaw2jCzyNrGlGpyo-vgd1c-1S 

# 7. 
#  Title: W cieniu złowrogiej swastyki [OPINIA] 
#  Source: TVP 
#  Date: 14 godz. temu 
#  Summary: Nowy rząd próbuje na spokojnie kolejny raz przetłumaczyć polskie racje politykom Unii Europejskiej. Mateusz Morawiecki na forum ekonomicznym w Davos robi to samo na płaszczyźnie ekonomicznej i, jak się zdaje, wychodzi mu to nie najgorzej. Gdy więc mamy do czynienia z nowym otwarciem w  
#  Link: https://www.tvp.info/35772286/w-cieniu-zlowrogiej-swastyki-opinia&amp;sa=U&amp;ved=0ahUKEwj7p-C1nPnYAhWxh6YKHboTAJ8QqQIIMigAMAY&amp;usg=AOvVaw2KQZ1BuE_VWOMbtsVW6XEW 

# 8. 
#  Title: Burza fleszy. Rex Tillerson w Warszawie 
#  Source: TVP 
#  Date: 1 dzień temu 
#  Summary: Prezydent Andrzej Duda spotkał się w piątek wieczorem w Belwederze z sekretarzem stanu USA. Spotkanie trwało około godziny. – Politycy uzgodnili polsko-amerykańską mapę działań, dotyczącą relacji gospodarczych i politycznych, w tym w zakresie bezpieczeństwa międzynarodowego – poinformował  
#  Link: https://www.tvp.info/35771398/burza-fleszy-rex-tillerson-w-warszawie&amp;sa=U&amp;ved=0ahUKEwj7p-C1nPnYAhWxh6YKHboTAJ8QqQIINSgAMAc&amp;usg=AOvVaw3MlJ2sJaWc8FxG3zJby8bo 

# 9. 
#  Title: Premier: w Davos widoczne coraz większe zrozumienie dla reformy  
#  Source: Polskie 
#  Date: 3 dni temu 
#  Summary: W rozmowach z przywódcami politycznymi w Davos widać coraz większe zrozumienie również dla tych aspektów, które czasami wydawały się niektórym ... Morawiecki powiedział w środę w TVP Info, że prowadzone przez niego w Davos rozmowy z przywódcami politycznymi służą budowie "odpowiedniej  
#  Link: http://www.polskieradio.pl/5/3/Artykul/2003256,Premier-w-Davos-widoczne-coraz-wieksze-zrozumienie-dla-reformy-wymiaru-sprawiedliwosci&amp;sa=U&amp;ved=0ahUKEwj7p-C1nPnYAhWxh6YKHboTAJ8QqQIIOigAMAg&amp;usg=AOvVaw1iOXwHLOdjNkOp2Vb1LZzg 

# 10. 
#  Title: Premier Mateusz Morawiecki w Davos będzie promował polski  
#  Source: Niezalezna.pl 
#  Date: 4 dni temu 
#  Summary: O komentarz w tej skandalicznej sprawie portal Niezależna.pl poprosił Tadeusza Płużańskiego, historyka, szefa publicystyki TVP Info. W jego ocenie "to jakieś nieporozumienie i skandal, żeby z okazji tak tragicznego i tak podniosłego dnia podnosić takie hasła restauracyjne, łącząc to jeszcze z kolczastymi drutami  
#  Link: http://niezalezna.pl/214942-premier-w-davos-bedzie-promowal-polski-model-gospodarczy&amp;sa=U&amp;ved=0ahUKEwj7p-C1nPnYAhWxh6YKHboTAJ8QqQIIPSgAMAk&amp;usg=AOvVaw0_0THT5eCDgaPEEnKz3WPK 

# 1. 
#  Title: STAN GRY: Petru: Morawiecki trudny dla opozycji, Syska: Opozycja  
#  Source: 300polityka.pl 
#  Date: 27 Gru 2017 
#  Summary: Za kilka miesięcy, w trakcie których Morawiecki i Szczerski będą peregrynować od Tallina po Sofię (czyli po obszarze tzw. Trójmorza) w poszukiwaniu sojuszników, .... One czytają umowy przed podpisaniem”. http://krytykapolityczna.pl/kraj/sroczynski-sutowski-wywiad/. — OJCIEC RYDZYK STOI ZA KARĄ  
#  Link: http://300polityka.pl/stan-gry/2017/12/27/petru-morawiecki-trudny-dla-opozycji-syska-opozycja-zmarnowala-rok-pompowanie-budki-i-gasiuk-niepowazne-sroczynski-chwali-komisje-jakiego/&amp;sa=U&amp;ved=0ahUKEwiZyPy1nPnYAhXL1SwKHfE2DJgQqQIIFCgAMAA&amp;usg=AOvVaw32xtBx2MCwG5BBB9MNMCoh 

# 2. 
#  Title: O uchodźcach Polaków rozmowy… 
#  Source: Krytyka 
#  Date: 16 Lip 2017 
#  Summary: Kochaj uchodźcę swego nie bardziej niż siebie samego, czyli modyfikacja klasycznego przykazania skierowana do polityków, dziennikarzy i medialnej publiczności. Tekst pochodzi z Krytyki Politycznej nr 3: Nasz dom publiczny. W tym roku mija 15 lat od wydania pierwszego numeru Krytyki Politycznej 
#  Link: http://krytykapolityczna.pl/kraj/o-uchodzcach-polakow-rozmowy/&amp;sa=U&amp;ved=0ahUKEwiZyPy1nPnYAhXL1SwKHfE2DJgQqQIIFygAMAE&amp;usg=AOvVaw0XinKtU0SmrK1x6sax6Jj1 

# 3. 
#  Title: Książki poczciwe i niepoczciwe 
#  Source: Krytyka 
#  Date: 6 Kwi 2017 
#  Summary: Wallace pokazuje, że na granicy naszego pola widzenia może dziać się coś, czego zwykle nie dostrzegamy. Kinga Dunin czyta „Niepamięć” Davida Fostera Wallace'a, „Sonatę Gustava” Rose Tremain, „Pedanta w kuchni” Juliana Barnesa oraz „Za zamkniętymi drzwiami” B.A. Paris. David Foster Wallace  
#  Link: http://krytykapolityczna.pl/kultura/czytaj-dalej/kinga-dunin-czyta/ksiazki-poczciwe-i-niepoczciwe/&amp;sa=U&amp;ved=0ahUKEwiZyPy1nPnYAhXL1SwKHfE2DJgQqQIIGigAMAI&amp;usg=AOvVaw0i7aqzQ7HiljKaurc8Fuwm 

# 4. 
#  Title: Lewicę można utopić w wannie 
#  Source: Krytyka 
#  Date: 15 Kwi 2017 
#  Summary: Bo ten wizerunek – elity biurokratyczno-kosmopolitycznej pośrednio uderza w nas. Na zasadzie: panowie z „Sowy i Przyjaciół” są oderwani od problemów zwykłego człowieka, latają samolotami, śpią w drogich hotelach i ustalają na jakichś konferencjach w Brukseli czy Davos coś, czego nie rozumiemy 
#  Link: http://krytykapolityczna.pl/kraj/sutowski-dunin-lewica/&amp;sa=U&amp;ved=0ahUKEwiZyPy1nPnYAhXL1SwKHfE2DJgQqQIIHSgAMAM&amp;usg=AOvVaw1D_plVyc-0bCvADbxxEWEn 

# 5. 
#  Title: STAN GRY: GPC mocno o Marszu: Kompromitacja, może jeszcze  
#  Source: 300polityka.pl 
#  Date: 14 Lis 2017 
#  Summary: Estetyka Czarnego Bloku i hasła „faszyści burżuje, wasz koniec się szykuje” od lat przekonują bowiem tylko już przekonanych”. http://krytykapolityczna.pl/kraj/majmurek-jak-oswoilismy-faszyzm-marsz-niepodleglosci/. — PIOTR ZAREMBA O ROZGRYWCE O MACIEREWICZA W TLE DYSKUSJI O ZMIANIE  
#  Link: http://300polityka.pl/stan-gry/2017/11/15/stan-gry-gpc-mocno-o-marszu-kompromitacja-moze-jeszcze-tradycja-nkwd-zaremba-i-fijolek-o-scenariuszu-bez-macierewicza-wronski-chwali-pad/&amp;sa=U&amp;ved=0ahUKEwiZyPy1nPnYAhXL1SwKHfE2DJgQqQIIICgAMAQ&amp;usg=AOvVaw2c1hha4mWce2BhCeq65LHU 

# 6. 
#  Title: STAN GRY: Rabin Schudrich chwali Kaczyńskiego, Sroczyński  
#  Source: 300polityka.pl 
#  Date: 21 Lis 2017 
#  Summary: Polityka unijna to jednak jedyna sfera, na którą PiS wyraźnie nie ma pomysłu – i na niej tylko potrafi tracić, o czym świadczy jedyne ostre wahnięcie sondaży od 2015 roku, jakie nastąpiło po niesławnym 27:1 w Brukseli”. http://krytykapolityczna.pl/kraj/sutowski-tweet-tuska-to-wielkie-ogarnijcie-sie-kur/ 
#  Link: http://300polityka.pl/stan-gry/2017/11/21/sta-gry-rabin-schudrich-chwali-kaczynskiego-sroczynski-tusk-skroci-kadencje-i-wroci-kkz-kaczynski-premierem-na-rok/&amp;sa=U&amp;ved=0ahUKEwiZyPy1nPnYAhXL1SwKHfE2DJgQqQIIIygAMAU&amp;usg=AOvVaw3P0F2HVXIF8j7Ue0dDqaJ5 

# 7. 
#  Title: STAN GRY: GW: Jaki jak Kapitan Bomba, Krytyka: Jaki jak Ikonowicz  
#  Source: 300polityka.pl 
#  Date: 14 Paź 2017 
#  Summary: ... — GOWIN: WIĘCEJ BŁĘDÓW PO NASZEJ STRONIE – mówił Krzysztofowi Ziemcowi w RMF: “Moim zdaniem, więcej błędów było po naszej stronie, a teraz wspólnie musimy wypracować rozwiązania, które zyskają akceptację pana prezydenta (…). Liczymy, że ze strony ośrodka prezydenckiego będzie  
#  Link: http://300polityka.pl/stan-gry/2017/10/14/stan-gry-gw-jaki-jak-kapitan-bomba-krytyka-jaki-jak-ikonowicz-danielewski-zandberg-jakby-chcial-cie-wyslac-na-korepetycje-ze-wszystkiego/&amp;sa=U&amp;ved=0ahUKEwiZyPy1nPnYAhXL1SwKHfE2DJgQqQIIJigAMAY&amp;usg=AOvVaw0WSwtHHjJI9NRvNN_u0kO4 

# 8. 
#  Title: STAN GRY: GPC na jedynce atakuje Axel Springer, RZ: Morawiecki  
#  Source: 300polityka.pl 
#  Date: 19 Wrz 2017 
#  Summary: POSŁOWIE CHCĄ OGRANICZYĆ REKLAMĘ PIWA, POPIERA TO MORAWIECKI – jak pisze w RZ Wiktor Farfecki: “W Sejmie pojawiają się głosy, by całkowicie ich zakazać. Takie rozwiązanie przedstawił poseł PiS Przemysław Czarnecki. Lobbuje w tej sprawie Małgorzata Zwiercan z koła Wolni i Solidarni,  
#  Link: http://300polityka.pl/stan-gry/2017/09/19/stan-gry-gpc-na-jedynce-atakuje-axel-springer-rz-morawiecki-popiera-ograniczenie-reklamy-piwa-gw-o-kopiuj-wklej-kampanii-billboardowej/&amp;sa=U&amp;ved=0ahUKEwiZyPy1nPnYAhXL1SwKHfE2DJgQqQIIKSgAMAc&amp;usg=AOvVaw0qQIU5cOCUgu16s0Jna-gl 

# 9. 
#  Title: STAN GRY: Godusławski: Strach broni przed budżetowym  
#  Source: 300polityka.pl 
#  Date: 9 Lis 2017 
#  Summary: ... — KRZYSZTOF WOŁODŹKO W GPC O BEZDUSZNYM STOSUNKU KRAKOWSKICH URZĘDNIKÓW WOBEC BIEDNEJ KOBIETY: “Małgorzata Tyrpa nie prosi o jałmużnę, nie chce z łaski kąta u obcych ludzi. Borykając się z własnymi życiowymi problemami, spłaciła długi, które powstały w wyniku  
#  Link: http://300polityka.pl/stan-gry/2017/11/09/stan-gry-goduslawski-strach-broni-przed-budzetowym-szalenstwem-mucha-o-decyzji-pis-ws-ochrony-zwierzat-ikonowicz-warszawa-to-nie-prywatna-firma-po/&amp;sa=U&amp;ved=0ahUKEwiZyPy1nPnYAhXL1SwKHfE2DJgQqQIILCgAMAg&amp;usg=AOvVaw1cs6RDcjvvFMmyNJIhTRRE 

# 10. 
#  Title: Amerykańscy liberałowie odkrywają, że „byli głupi” 
#  Source: Krytyka 
#  Date: 18 Lut 2017 
#  Summary: Jednym z niewielu pocieszających aspektów wygranej Donalda Trumpa w jesiennych wyborach prezydenckich jest impuls do (auto)diagnozy amerykańskiego liberalizmu, a konkretniej jego politycznej inkarnacji – Partii Demokratycznej i jej zaplecza. Mała to, rzecz jasna, ulga: pośród niewielu  
#  Link: http://krytykapolityczna.pl/swiat/usa-frank-bylismy-glupi/&amp;sa=U&amp;ved=0ahUKEwiZyPy1nPnYAhXL1SwKHfE2DJgQqQIILygAMAk&amp;usg=AOvVaw08BVE2MbDeOPW4s6j9uC3D 

# 1. 
#  Title: Niebywałe! Morawiecki naprawdę to powiedział. Wicepremier  
#  Source: Najwyższy 
#  Date: 31 Paź 2017 
#  Summary: Mateusz Morawiecki, minister rozwoju i finansów był gościem „Faktów po faktach” na antenie TVN24. Wicepremier mówił między innymi o deficycie, wydatkach społecznych i sytuacji gospodarczej Polski. Ten wywiad może przejść do historii, bo świetnie obrazuje prawdziwe podejście do gospodarki Morawieckiego 
#  Link: http://nczas.com/wiadomosci/polska/niebywale-morawiecki-naprawde-to-powiedzial-wicepremier-wreszcie-pokazal-prawdziwa-twarz/&amp;sa=U&amp;ved=0ahUKEwjjoI23nPnYAhUGiCwKHTpeBLsQqQIIFCgAMAA&amp;usg=AOvVaw1DGIr1lhnYHISHGVfxvZS4 

# 2. 
#  Title: STAN GRY: Zaremba: Możliwe, że prezes widzi Morawieckiego jako  
#  Source: 300polityka.pl 
#  Date: 6 Gru 2017 
#  Summary: Jeśli Morawiecki ma być czymś więcej niż dekoracją, przebudowie ulec powinno wiele: model administrowania, polityki kadrowej i mentalność partyjnych działaczy. Możliwe, że prezes o tym myśli, ba widzi Morawieckiego jako swego następcę. Ale czy ogólnej intencji towarzyszą konkretne pomysły na  
#  Link: http://300polityka.pl/stan-gry/2017/12/06/stan-gry-zaremba-mozliwe-ze-prezes-widzi-morawieckiego-jako-nastepce-dabrowska-kaczynski-lubi-byc-politycznie-uwiedziony-nowym-pomyslem-wronski-mm-to-faza-gierkowska/&amp;sa=U&amp;ved=0ahUKEwjjoI23nPnYAhUGiCwKHTpeBLsQqQIIFygAMAE&amp;usg=AOvVaw2vK7EGbgdTLdiYzKmeQAUe 

# 3. 
#  Title: STAN GRY: Matyja: Polacy wcale nie porywają się z szablą  
#  Source: 300polityka.pl 
#  Date: 15 Gru 2017 
#  Summary: Nie mamy zatem do czynienia jedynie z podmianą wizerunkowych zderzaków. Odpowiedź, czy zaliczając kolejne testy Morawiecki zda egzamin z przywództwa dopiero przed nami”. http://jagiellonski24.pl/2017/12/14/wasz-premier-nasz-sejm/. — ANTONI DUDEK UWAŻA, ŻE MORAWIECKI BĘDZIE  
#  Link: http://300polityka.pl/stan-gry/2017/12/15/stan-gry-matyja-polacy-wcale-nie-porywaja-sie-z-szabla-trudnowski-i-mazur-determinacja-pmm-majmurek-o-zawieszonej-deadrianizacji-rz-pis-odzyskuje-zachodnia-polske/&amp;sa=U&amp;ved=0ahUKEwjjoI23nPnYAhUGiCwKHTpeBLsQqQIIGigAMAI&amp;usg=AOvVaw32oktF_179yjLiHAK7G7Ti 

# 4. 
#  Title: Andrzej Friszke: Naród według Jarosława Kaczyńskiego 
#  Source: Gazeta 
#  Date: 29 Paź 2017 
#  Summary: Obawiam się, że nawet gdy PiS się skończy, to pozostanie ogromna wrogość między Polakami, nieufność, odmowa budowania wspólnoty. Na pewno będzie nam ciężko. Zniszczono to, co było wielkim kapitałem Polski w latach, gdy wychodziliśmy z komunizmu - mówi historyk Andrzej Friszke. W wywiadzie  
#  Link: http://wyborcza.pl/7,75398,22579192,andrzej-friszke-narod-wedlug-jaroslawa-kaczynskiego.html&amp;sa=U&amp;ved=0ahUKEwjjoI23nPnYAhUGiCwKHTpeBLsQqQIIHSgAMAM&amp;usg=AOvVaw3aIrYbDUIBYvqm1BuIL_XG 

# 5. 
#  Title: STAN GRY: GW: Kaczyński na 75%, Trudnowski: Sezon polityczny  
#  Source: 300polityka.pl 
#  Date: 26 Paź 2017 
#  Summary: Z całą odpowiedzialnością, władzą i ograniczeniami za tym idącymi”. http://jagiellonski24.pl/2017/10/25/szeregowy-premier-z-nowogrodzkiej/. — CZY NOWY SEZON POLITYCZNY BĘDĄ SPONSOROWAĆ LITERKI C, B I A – Piotr Trudnowski na Jagielloński24: “Ostatnie tygodnie pokazują, że ekipa  
#  Link: http://300polityka.pl/stan-gry/2017/10/26/stan-gry-gw-kaczynski-na-75-trudnowski-sezon-polityczny-sponsoruja-literki-c-b-i-a-fakt-krytykuje-karczewskiego/&amp;sa=U&amp;ved=0ahUKEwjjoI23nPnYAhUGiCwKHTpeBLsQqQIIICgAMAQ&amp;usg=AOvVaw2dcqPllLa_tRjOJgdYyqcl 

# 6. 
#  Title: Solaris idzie na rekord. Polska firma wyprodukuje najwięcej  
#  Source: Forsal.pl 
#  Date: 6 Paź 2017 
#  Summary: Rok 2017 będzie rekordowy dla Solaris Bus & Coach pod względem wyprodukowanych autobusów – będzie ich łącznie ponad 1,4 tys. sztuk - poinformowała w piątek spółka. We wrześniu, tylko na rynku polskim, wielkopolski producent podpisał umowy na dostarczenie 107 autobusów 
#  Link: http://forsal.pl/artykuly/1076209,solaris-idzie-na-rekord-polska-firma-wyprodukuje-najwiecej-autobusow-w-swojej-historii.html&amp;sa=U&amp;ved=0ahUKEwjjoI23nPnYAhUGiCwKHTpeBLsQqQIIIygAMAU&amp;usg=AOvVaw0bFlh6inV8m-ecBPzXTMO6 

# 7. 
#  Title: STAN GRY: Flis: PiS konsumuje Kukiza i konserwatywną PO  
#  Source: 300polityka.pl 
#  Date: 15 Paź 2017 
#  Summary: ... — EPISKOPAT PROSI O OTWARTOŚĆ WOBEC UKRAIŃCÓW: “Dziękując za dotychczasową życzliwość okazaną osobom przybywającym z Ukrainy do Polski, Episkopat prosi o dalszą otwartość i gościnność wobec nich. Zwraca się również z prośbą o organizację punktów duszpasterskich dla  
#  Link: http://300polityka.pl/stan-gry/2017/10/16/stan-gry-flis-pis-konsumuje-kukiza-i-konserwatywna-po-karnowski-o-nowej-opozycji-zaremba-o-szczuciu-trudnowski-kawior-stanie-wam-w-gardle/&amp;sa=U&amp;ved=0ahUKEwjjoI23nPnYAhUGiCwKHTpeBLsQqQIIJigAMAY&amp;usg=AOvVaw0g8IuA6L4KDo7Fy7gFT-0D 

# 8. 
#  Title: STAN GRY: Zandberg: Wspólna lista i Giertych to prezent dla PiS  
#  Source: 300polityka.pl 
#  Date: 5 Sie 2017 
#  Summary: Fransa Timmermansa”. http://jagiellonski24.pl/2017/08/04/zaprosmy-timmermansa-do-krynicy/. — NAJPOWAŻNIEJSZY DOTĄD KONFLIKT PREZYDENT – MON – jak pisze Paweł Wroński w GW: “To kolejny – i chyba najpoważniejszy w ostatnim czasie – kryzys w relacji ministra obrony z prezydentem,  
#  Link: http://300polityka.pl/stan-gry/2017/08/05/stan-gry-zandberg-wspolna-lista-i-giertycha-to-prezent-dla-pis-niesiolowski-nie-przeszkadza-mi-miller-na-liscie-bielecki-timmermans-otwiera-rany/&amp;sa=U&amp;ved=0ahUKEwjjoI23nPnYAhUGiCwKHTpeBLsQqQIIKSgAMAc&amp;usg=AOvVaw03_XaWnPOxo9pUHnUSDqxy 

# 9. 
#  Title: Narodowcy chcą mieć swoją telewizję. Zaczynają zrzutkę na kanał  
#  Source: Gazeta 
#  Date: 12 Lut 2017 
#  Summary: Kita powołuje się tu na raport portalu Jagiellonski24.pl z września 2015 r., zgodnie z którym kapitał zagraniczny to 76 proc. rynku prasowego, 48 proc. rynku radiowego i 36 proc. telewizyjnego. Dlatego stowarzyszenie chce budować własny portal informacyjny i telewizję internetową. Rzecznik kończy tekst  
#  Link: http://wyborcza.pl/7,75398,21359903,telewizja-narodowa-z-marszu.html&amp;sa=U&amp;ved=0ahUKEwjjoI23nPnYAhUGiCwKHTpeBLsQqQIILCgAMAg&amp;usg=AOvVaw2aFsNAflUzrak5AO8gZ5tH 

# 10. 
#  Title: STAN GRY: Sienkiewicz: To już rozgrywka młodych, nie pokolenia  
#  Source: 300polityka.pl 
#  Date: 8 Sie 2017 
#  Summary: ... — POLSKA ZDANIEM WASZCZYKOWSKIEGO NIE POTRZEBUJE WIĘKSZEJ OBECNOŚCI NATO: “Z kolei w rozmowie z dziennikiem „Kommiersant”, Waszczykowski zapewnił Rosjan, że Polska w tej chwili nie potrzebuje dodatkowych sił NATO na swoim terytorium. Zbył też pytanie o to, czy rząd byłby  
#  Link: http://300polityka.pl/stan-gry/2017/08/08/stan-gry-sienkiewicz-to-juz-rozgrywka-mlodych-nie-pokolenia-frasyniuka-wojcik-potrzebujemy-nowej-opozycji-szuldrzynski-nowy-poczatek-pad/&amp;sa=U&amp;ved=0ahUKEwjjoI23nPnYAhUGiCwKHTpeBLsQqQIILygAMAk&amp;usg=AOvVaw0RqZQJn-QfZGEsKlcJAMGk 

# 1. 
#  Title: Premier Morawiecki właśnie określił, kiedy wejdziemy do strefy euro  
#  Source: BusinessInsider 
#  Date: 3 dni temu 
#  Summary: Wszystko jasne. Premier Morawiecki w wywiadzie dla Bloomberg TV w Davos powiedział, że Polska wejdzie do strefy euro, kiedy osiągnie dochód rozporządzalny na poziomie 80-90 proc. najbogatszych krajów UE. Pytani przez nas ekonomiści odczytują tę wypowiedź jasno. - Czyli raczej nigdy - mówi z  
#  Link: https://businessinsider.com.pl/finanse/davos-kiedy-polska-wejdzie-do-strefy-euro-mowi-mmorawiecki/n6t14jw&amp;sa=U&amp;ved=0ahUKEwjVwqa3nPnYAhUBCywKHawzBQsQqQIIFCgAMAA&amp;usg=AOvVaw3ue4wsVAFBEiaMtDeESTfC 

# 2. 
#  Title: Polska szuka sojuszników w Davos. Premier chce powstania  
#  Source: BusinessInsider 
#  Date: 2 dni temu 
#  Summary: Głównym celem wizyty premiera Mateusza Morawieckiego na Forum Ekonomicznym w Davos jest szukanie sojuszników przy sprawach związanych chociażby z bezpieczeństwem - w tym także gazowym. Zdaniem premiera, świat potrzebuje też nowego ładu dla setek milionów ludzi na całym świecie 
#  Link: https://businessinsider.com.pl/wiadomosci/morawiecki-w-davos-bezpieczenstwo-gaz-nowy-lad/5mpc5f7&amp;sa=U&amp;ved=0ahUKEwjVwqa3nPnYAhUBCywKHawzBQsQqQIIFygAMAE&amp;usg=AOvVaw0mcWdzPoIev9R_Ie2Axjzu 

# 3. 
#  Title: Z kim w Davos spotka się premier Morawiecki 
#  Source: BusinessInsider 
#  Date: 4 dni temu 
#  Summary: Poprzez solidarność międzypokoleniową, solidarność społeczną, nasze programy społeczne, chcę pokazać, że nasz model gospodarczy działa – powiedział premier we wtorek przed wylotem do Davos. Premier Morawiecki zamierza poruszać temat polityki prorodzinnej i zwracać uwagę innych państw na  
#  Link: https://businessinsider.com.pl/wiadomosci/davos-z-kim-spotka-sie-premier-morawiecki/gl6ftpw&amp;sa=U&amp;ved=0ahUKEwjVwqa3nPnYAhUBCywKHawzBQsQqQIIGigAMAI&amp;usg=AOvVaw3NZNXKtGD-HiZyR807GIwN 

# 4. 
#  Title: Polska ofensywa promocyjna w Davos 
#  Source: BusinessInsider 
#  Date: 3 dni temu 
#  Summary: Foto: Flickr.com / Kancelaria Premiera / Public domain Do Davos przyjechał m.in. premier Mateusz Morawiecki, który spotkał się z Sekretarzem USA ds. ... to świetne miejsce do inwestycji - taka jest najkrótsza konkluzja wypowiedzi gości panelu dyskusyjnego organizowanego przez Pekao S.A. w Davos 
#  Link: https://businessinsider.com.pl/finanse/polska-w-davos-i-promocja-gospodarki/x11jyzw&amp;sa=U&amp;ved=0ahUKEwjVwqa3nPnYAhUBCywKHawzBQsQqQIIHSgAMAM&amp;usg=AOvVaw0OG8NOXBt3in1HagRjKxaz 

# 5. 
#  Title: Donald Trump i Andrzej Duda spotkali się w Davos 
#  Source: BusinessInsider 
#  Date: 1 dzień temu 
#  Summary: Polska szuka sojuszników w Davos. Premier chce powstania nowego ładu na świecie. Coraz bliżej ukończenia S7. Podpisano ważną umowę. Raper 50 Cent zarobił miliony na sprzedaży albumu za... bitcoiny. Premier Morawiecki właśnie określił, kiedy wejdziemy do strefy euro. Jest jednak pewien haczyk 
#  Link: https://businessinsider.com.pl/wiadomosci/davos-2018-rozmowa-andrzeja-dudy-i-donalda-trumpa/xztn27b&amp;sa=U&amp;ved=0ahUKEwjVwqa3nPnYAhUBCywKHawzBQsQqQIIICgAMAQ&amp;usg=AOvVaw0t3JNrzLnpfpEezz1xQtXd 

# 6. 
#  Title: Premier: przychody z VAT wzrosły o blisko jedną czwartą w ciągu roku 
#  Source: BusinessInsider 
#  Date: 4 dni temu 
#  Summary: To oznacza wzrost o 23 proc. rdr Takie informacje przekazał premier Mateusz Morawiecki przed wylotem na Światowe Forum Ekonomiczne w Davos. ... się niezwykle pozytywnym bilansem w porównaniu do poprzednich 10 lat" - powiedział Morawiecki podczas konferencji prasowej po posiedzeniu rządu 
#  Link: https://businessinsider.com.pl/firmy/podatki/przychody-podatkowe-z-vat-w-polsce-w-2017-roku/rtp8de3&amp;sa=U&amp;ved=0ahUKEwjVwqa3nPnYAhUBCywKHawzBQsQqQIIIygAMAU&amp;usg=AOvVaw3cHL_q0IsQKKkJKnfStOAW 

# 7. 
#  Title: Bruksela szykuje bombę, która może poważnie zaszkodzić Polsce  
#  Source: BusinessInsider 
#  Date: 2 dni temu 
#  Summary: Piotr Bielski, główny ekonomista BZ WBK (któremu przez lata szefował Mateusz Morawiecki), jako jeden z nielicznych przestrzegał przed podobnymi pomysłami. Dlaczego są aż tak dla nas niebezpieczne? ... Premier Morawiecki w Davos mówił, że IV kw. 2017 r. zamknęliśmy 5 proc. wzrostem PKB 
#  Link: https://businessinsider.com.pl/finanse/makroekonomia/polska-zostanie-bez-srodkow-ue-piotr-bielski-bz-wbk/g5dsvpy&amp;sa=U&amp;ved=0ahUKEwjVwqa3nPnYAhUBCywKHawzBQsQqQIIJigAMAY&amp;usg=AOvVaw0GJKEXA2jnDHn06ydACxH3 

# 8. 
#  Title: Prezydent wejście do strefy euro uzależnia od zarobków Polaków 
#  Source: BusinessInsider 
#  Date: 2 dni temu 
#  Summary: W środowej rozmowie z agencją Bloomberga do kwestii przystąpienia do unii walutowej odnosił się premier Mateusz Morawiecki. Stwierdził on m.in. ... W Światowym Forum Ekonomicznym w Davos, które odbywa się w dniach 23-26 stycznia, uczestniczą liderzy światowej polityki, szefowie najważniejszych  
#  Link: https://businessinsider.com.pl/finanse/waluty/kiedy-polska-wejdzie-do-strefy-euro-stanowisko-prezydenta/1k6jhtf&amp;sa=U&amp;ved=0ahUKEwjVwqa3nPnYAhUBCywKHawzBQsQqQIIKSgAMAc&amp;usg=AOvVaw3ggvA5bztaukpeyXvveXlE 

# 9. 
#  Title: Andrzej Konieczny został nowym szefem Lasów Państwowych 
#  Source: BusinessInsider 
#  Date: 19 Sty 2018 
#  Summary: Premier Morawiecki: cieszę się, że tworzymy państwo opiekuńcze · Światowe Forum Ekonomiczne odbywa się w Davos - najwyżej położonym mieście w Europie. Zmaga się  
#  Link: https://businessinsider.com.pl/polityka/andrzej-konieczny-dyrektorem-lasow-panstwowych/zcb9wmh&amp;sa=U&amp;ved=0ahUKEwjVwqa3nPnYAhUBCywKHawzBQsQqQIILCgAMAg&amp;usg=AOvVaw0Os6VFSACMajIVOQBryn5Q 

# 10. 
#  Title: Oto majątek Mateusza Morawieckiego 
#  Source: BusinessInsider 
#  Date: 8 Gru 2017 
#  Summary: Mateusz Morawiecki ostatnie oświadczenie majątkowe złożył wiosną br. Opisuje ono jego majątek na koniec 2016 roku. Z dokumentu wynika, że Mateusz Morawiecki jest właścicielem dwóch domów - o powierzchni około 150 mkw. wraz z działką zajmującą 0,46 ha i drugiego o powierzchni 100 mkw 
#  Link: https://businessinsider.com.pl/polityka/mateusz-morawiecki-oswiadczenie-majatkowe/vbyk1n4&amp;sa=U&amp;ved=0ahUKEwjVwqa3nPnYAhUBCywKHawzBQsQqQIILygAMAk&amp;usg=AOvVaw1KNS8vv9QrXU4shJw71Vlw 
