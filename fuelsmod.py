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

    def check_ua(self, fuelnumber):
        '''
        if you want to receive average price of gasoline fuel type 1
        in order to receive average price of diesel fuel type 2
        '''
        soup = self._requesting_page(configuration.url_fuel_ua)
        price = ''
        for element in soup.find_all('tfoot'):
            for price in element.find_all('span', {"class":'value'})[-3:]:
                self.price_list.append(price.text)
        return float(self.price_list[fuelnumber])/self.dollar_price_ua()
        
    def dollar_price_ua(self):
        soup = self._requesting_page(configuration.url_dollar_ua)
        for element in soup.find_all('tfoot', {"class": "service_bank_rates_usd"}):
            price = element.find('td', {"class": "sell_rate"})
        return float(price.text)

    def check_ru(self, fuelnumber):
        '''
        fuelnumber = 1 for 95 gasoline, 2 for 98 gasoline, 3 for diesel
        '''
        font_elements = []
        soup = self._requesting_page(configuration.url_ru)
        for element in soup.find_all('div', {"class": "min_price"}):
            font_elements.append(element.font.text)
            self.price_list.append(element.sup.text)
        return_str = str(font_elements[fuelnumber])+','+ str(self.price_list[fuelnumber])
        return str(return_str)

    def dollar_value_by(self):
        soup = self._requesting_page(configuration.url_dollar_by)
        value_str = ''
        for element in soup.find_all('div', {"class": "bank-info-head content_i calc_color"}):
            value_str = element.tbody.text[19:23]
        return float(value_str)

    def check_by(self, fuelnumber):
        '''
        fuelnumber = 0 for 95 gasoline, 2 for diesel, 4 for 98 gasoline
        '''
        soup = self._requesting_page(configuration.url_by)
        for element in soup.find_all('td', {"class": "col2"}):
            self.price_list.append(element.text)
        to_return = float(self.price_list[fuelnumber])/self.dollar_value_by()
        return str(to_return)

    def wrapping_prices(self):
        prices_dict = {}
        prices_dict["Fuels around the world"] = [{"Russia": {"gasoline 95" : self.check_ru(1),
            "gasoline 98" : self.check_ru(2), "diesel": self.check_ru(3)}},
            {"Ukraine": {"gasoline 95": self.check_ua(1), "diesel" : self.check_ua(2)}},
            {"Belarus": {"gasoline 95": self.check_by(0), "diesel": self.check_by(2)}}]
        return prices_dict


def main():
    fs = FuelScrap()
    print(fs.wrapping_prices())

if __name__ == '__main__':
    main()
