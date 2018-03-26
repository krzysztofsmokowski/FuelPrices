import requests
from bs4 import BeautifulSoup
import configuration


class FuelScrap(object):
    def __init__(self):
        self.url_ua = configuration.url_fuel_ua
        self.price_list = []

    def _requesting_page(self, url):
        requested_page = requests.get('{}'.format(url))
        soup = BeautifulSoup(requested_page.text, 'html.parser')
        return soup

    def _average_price(self, list_object):
        return sum(list_object)/len(list_object)

    def check_ua_95(self):
        soup = self._requesting_page(configuration.url_fuel_ua)
        for element in soup.find_all('td', {"class": "a_95"}):
            self.price_list.append(float(element.text))
        return self._average_price(self.price_list)/self.dollar_price_ua()

    def check_ua_diesel(self):
        soup = self._requesting_page(configuration.url_fuel_ua)
        for element in soup.find_all('td', {"class": "dp"}):
            self.price_list.append(float(element.text))
        return self._average_price(self.price_list)/self.dollar_price_ua()

    def dollar_price_ua(self):
        soup = self._requesting_page(configuration.url_dollar_ua)
        for element in soup.find_all('tfoot', {"class": "service_bank_rates_usd"}):
            price = element.find('td', {"class": "sell_rate"})
        return float(price.text)

    def check_ru(self, fuelnum):
        '''
        fuelnum = 1 for 95 gasoline, 2 for 98 gasoline, 3 for diesel
        '''
        font_elements = []
        soup = self._requesting_page(configuration.url_ru)
        for element in soup.find_all('div', {"class": "min_price"}):
            font_elements.append(element.font.text)
            self.price_list.append(element.sup.text)
        return font_elements[fuelnum]+','+ self.price_list[fuelnum]+'$'

    def check_by(self):
        pass

def main():
    fs = FuelScrap()

if __name__ == '__main__':
    main()
