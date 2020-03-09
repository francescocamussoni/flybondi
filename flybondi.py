import requests
from bs4 import BeautifulSoup
import smtplib
import time
import re
import unicodedata

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'}

def strip_accents(text):
    try:
        text = unicode(text, 'utf-8')
    except NameError:
        pass

    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode("utf-8")

    return str(text)

def check_price(URL):
    for url in URL:
        try:
            page = requests.get(url, headers=headers)

            soup1 = BeautifulSoup(page.content, "html.parser")
            soup = BeautifulSoup(soup1.prettify(), "html.parser")

            price=[float(x.get_text().strip().strip('$').replace('.', '').replace(',', '.')) for x in soup.findAll(class_=re.compile("db material-transition absolute translate-"))]
            price = [x for x in price if x]

            club_fb=[x.get_text().strip() for x in soup.findAll(class_="b f7 ff--lato grey-100 pb1")]
            if 'Club Flybondi' in club_fb:
                price=price[1::2]

            n=int(len(price)/2)
            total_price=float('%.2f'%(min(price[:n])+min(price[n:])))

            places = " ".join(soup.find(class_="flex-grow-1 flex-grow-0-ns ml2 ml0-ns").get_text().replace('\n', '').replace('\t', '').split()).split(' a ')
            places[0], places[1] = places[1], places[0]

            dates = [x.get_text().strip().replace('.', '').replace(',', '.') for x in soup.findAll(class_="b ff--poppins mv3")]

            time = [x.get_text().strip().replace('.', '').replace(',', '.') for x in soup.findAll(class_="jsx-2654605770 b f2l")]
            time_selected = [time[2*price.index(min(price[:n]))], time[2*price.index(min(price[n:]))]]

            print(total_price)
            if total_price < 3500:
                send_mail(total_price, places, dates, time_selected)
        except:
            print('no anduvo perro')

def send_mail(price, place, date, time):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('camussonif@gmail.com', 'zsfxbuufrvhvaukp')

    place=[strip_accents(x) for x in place]

    subject = 'Vuelo a $'+str(price)+' del '+date[0]+' al '+date[1]
    body = 'Hay un vuelo a $'+str(price)+' del '+date[0]+' al '+date[1]+'. El vuelo sale de '+place[0]+' a las '+time[0]+' y la vuelta es desde '+place[1]+' a las '+time[1]+'. Link: https://flybondi.com/ar/search/results?adults=1&children=0&currency=ARS&departureDate=2020-02-21&fromCityCode=BUE&infants=0&returnDate=2020-02-25&toCityCode=BRC'

    msg = f"Subject: {subject}\n\n{body}"

    server.sendmail('camussonif@gmail.com', 'camussonif@gmail.com', msg)
    server.quit()

while(True):
    url=['https://flibondi.com/ar/search/results?adults=1&children=0&currency=ARS&departureDate=2020-03-19&fromCityCode=BRC&infants=0&returnDate=2020-03-24&toCityCode=COR']#feriado puente brc cordoba
    url.append('https://flybondi.com/ar/search/results?adults=1&children=0&currency=ARS&departureDate=2020-02-20&fromCityCode=BRC&infants=0&returnDate=2020-02-25&toCityCode=COR')#carnaval brc cordoba
    url.append('https://flybondi.com/ar/search/results?adults=1&children=0&currency=ARS&departureDate=2020-04-04&fromCityCode=BRC&infants=0&returnDate=2020-04-14&toCityCode=COR')#semanita brc cordoba
    url.append('https://flybondi.com/ar/search/results?adults=1&children=0&currency=ARS&departureDate=2020-02-20&fromCityCode=BRC&infants=0&returnDate=2020-02-25&toCityCode=BUE')#carnaval brc bsas
    url.append('https://flybondi.com/ar/search/results?adults=1&children=0&currency=ARS&departureDate=2020-04-04&fromCityCode=BRC&infants=0&returnDate=2020-04-14&toCityCode=BUE')#semanita brc bsas
    url.append('https://flybondi.com/ar/search/results?adults=1&children=0&currency=ARS&departureDate=2020-03-19&fromCityCode=BRC&infants=0&returnDate=2020-03-24&toCityCode=COR')#feriado puente brc bsas
    check_price(url)
    time.sleep(60*60)

