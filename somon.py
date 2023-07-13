import cloudscraper, ssl, socket, socks, json, time, urllib
from colorama import Fore
from random import choice
from somon_parser import *

locations = ["all", "511", "512", "683", "624", "625", "627", "626", "513", "676", "629", "630", "631", "632", "633", "635", "636", "648", "637", "638", "634", "639", "651", "640", "623", "641", "643", "644", "645", "646", "647", "650", "649", "515", "628", "642", "665", "652", "684", "653", "654", "655", "656", "657", "658", "659", "660", "661", "662", "663", "664", "667", "666", "668", "669", "670", "671", "672", "673", "674", "514", "675", "681", "677", "678", "679", "680", "682"]





class Error:
    def __init__(self, message, errors):
        print('Info: ' + message)
        print('Error: ' + errors)
        exit()









class SomonParse:



    def __init__(self) -> None:
        pass

    def getContacts(self, city, query, min_price, max_price, exchange, save_path, proxies=""):

        if proxies != '':
            try:
                proxy_ip, proxy_port, proxy_password, proxy_username = proxies.split(':')
            except:
                raise Error('Используйте такой формат: ip:port:password:username', 'Неверный формат прокси')

            socks.set_default_proxy(socks.SOCKS5, proxy_ip, proxy_port, username=proxy_username, password=proxy_password)
            socket.socket = socks.socksocket

        s = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0'},ssl_context=ssl._create_unverified_context())

        try:
            with open('useragents.txt', 'r') as f:
                ua = f.readlines() # User Agents
        except:
            raise Error('Создайте файл с названием useragents.txt и заполните его юзер агентами с каждой строки', 'Нету файла useragents.txt')
        

        url = 'https://somon.tj/search/'

        params = {
            'q=': urllib.parse.quote(query),
            'cities=': locations[city],
            'price_min=': min_price,
            'price_max=': max_price,
            'ad_type=': exchange
        }

        parameters = ''
        i = 1
        for key, val in params.items():
            andy = '&'
            if(i == len(params)):
                andy = ''
            parameters += ''.join(str(key)+str(val)+andy)
            i += 1


        headers = {
            'Host': 'somon.tj',
            'User-Agent': choice(ua).replace('\n', ''),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }


        print('Ищем объявления...')
        
        try:
            r = s.get(f'{url}?{parameters}', headers=headers)
        except:
            raise Error('Используйте валидний прокси', 'Медленный прокси или невалидный')


        if r.status_code == 200:
            data = json.loads(r.text)
            print('Получаем ссылки...')
            r = s.get('https://somon.tj' + data['full_url'])
            links = getLinks(r.text.replace("\\/", "/").encode().decode('UTF-8'))
            if len(links) < 1:
                print('Объявлений не найдено')
            else:
                print(f'Найдено ссылок: {len(links)}')
                print('Парсим каждую ссылку...')
                for link in links:
                    link = link['href']
                    link = "https://somon.tj"+link
                    r = s.get(link)
                    name = getName(r.text.replace("\\/", "/").encode().decode('UTF-8'))
                    headers = {
                        'Host': 'somon.tj',
                        'User-Agent': choice(ua).replace('\n', ''),
                        'Accept': 'application/json, text/javascript, */*; q=0.01',
                        'Accept-Language': 'en-US,en;q=0.5',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Referer': link,
                        'X-Requested-With': 'XMLHttpRequest',
                        'Connection': 'keep-alive',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-origin'
                    }
                    r = s.get(link.replace('adv', 'phone_check'), headers=headers)
                    phone = json.loads(r.text)
                    print(Fore.GREEN + f"{name} - {phone['tel']}")
                    with open(save_path, 'a') as f:
                        f.writelines(f"{name}:{phone['tel']}\n")
                    print('Нажмите CTRL + Z чтобы остановить скрипт')
                    time.sleep(5)
        else:
            with open('error.log', 'w', encoding='UTF-8') as f:
                f.write(r.content)
                f.close()
     
            raise Error('Посматрите файл error.log', 'Статус ответа: ' + r.status_code)