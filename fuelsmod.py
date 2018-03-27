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

    def check_ru(self, fuelnumber):
        '''
        fuelnumber = 1 for 95 gasoline, 2 for 98 gasoline, 3 for diesel
        '''
        font_elements = []
        soup = self._requesting_page(configuration.url_ru)
        for element in soup.find_all('div', {"class": "min_price"}):
            font_elements.append(element.font.text)
            self.price_list.append(element.sup.text)
        return_str = str(font_elements[fuelnumber])+','+ str(self.price_list[fuelnumber])+'$'
        return return_str

    def dollar_value_by(self):
        soup = self._requesting_page(configuration.url_dollar_by)
        value_str = ''
        for element in soup.find_all('div', {"class": "bank-info-head content_i calc_color"}):
            value_str = element.tbody.text[19:23]
        return str(value_str)

    def check_by(self, fuelnumber):
        '''
        fuelnumber = 0 for 95 gasoline, 2 for diesel, 4 for 98 gasoline
        '''
        soup = self._requesting_page(configuration.url_by)
        for element in soup.find_all('td', {"class": "col2"}):
            self.price_list.append(element.text)
        return float(self.price_list[fuelnumber])/self.dollar_value_by()

    def wrapping_prices(self):
        prices_dict = {}
        prices_dict["Fuels around the world"] = [{"Russia": {"gasoline 95" : self.check_ru(1),
            "gasoline 98" : self.check_ru(2), "diesel": self.check_ru(3)}}, 
            {"Ukraine": {"gasoline 95": self.check_ua_95(), "diesel": self.check_ua_diesel()}}]
        return prices_dict


def main():
    fs = FuelScrap()
    print(fs.wrapping_prices())
    print(fs.check_ua_diesel())
    print(fs.check_ua_95())
    print(fs.check_ru(3))
    print(type(fs.check_ru(2)))
    print(fs.check_ru(2))
    print(fs.check_ru(1))
if __name__ == '__main__':
    main()
