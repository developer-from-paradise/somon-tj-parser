

from colorama import init
from colorama import Fore
import platform, os
from threading import Thread
from somon import SomonParse

init(autoreset=True)
# Cleaning console
if platform.system() == 'Windows':
    clear = lambda: os.system('cls')
else:
    clear = lambda: os.system('clear')

clear()

inputStyle = Fore.GREEN + '[#]' + Fore.WHITE + ' '

# Function to get data from user
def getDataFromUser(type, string):
    if type == 'str':
        while True:
            try:
                var = str(input(inputStyle + string))
                return var
            except:
                pass
    elif type == 'int':
        while True:
            try:
                var = int(input(inputStyle + string))
                return var
            except:
                pass


# Function to divine proxy
def func_chunk(alist, wanted_parts):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]


# Function ro get proxy from file
def get_proxies(proxy_file):
    with open(proxy_file, 'r') as f:
        proxies = f.readlines()
    prox = []
    for proxy in proxies:
        prox.append(proxy.replace('\n', ''))
    return prox





def main():
    print(Fore.YELLOW + fr'''
 _____                                   _____    ___   ______
/  ___|                                 |_   _|  |_  |  | ___ \
\ `--.   ___   _ __ ___    ___   _ __     | |      | |  | |_/ /  __ _  _ __  ___   ___  _ __
 `--. \ / _ \ | '_ ` _ \  / _ \ | '_ \    | |      | |  |  __/  / _` || '__|/ __| / _ \| '__|
/\__/ /| (_) || | | | | || (_) || | | |   | |  /\__/ /  | |    | (_| || |   \__ \|  __/| |
\____/  \___/ |_| |_| |_| \___/ |_| |_|   \_/  \____/   \_|     \__,_||_|   |___/ \___||_|
                                    Ismail
                    https://github.com/developer-from-paradise
[0] - Парсинг номеров и имён 
[1] - Парсинг (Заголовок, Описание, Автор, Ссылки на фото, Цена)
''')
    mode = getDataFromUser('int', 'Режим: ')
    proxy_file = getDataFromUser('str', 'Введите путь до файла с прокси: ')
    
    save_path = getDataFromUser('str', 'Введите файл для сохранения: ')

    if mode == 0:
        query = getDataFromUser('str', 'Объявление: ')
        print(Fore.GREEN + '''
    [0] Все города                  [19] Дарваз                         [38] Мехнатобод                 [57] Фархор
    [1] Душанбе                     [20] Деваштич (Ганчи)               [39] Муминабад                  [58] Хамадани
    [2] Худжанд                     [21] Джаббор Расулов                [40] Мургаб                     [59] Ховалинг
    [3] Абдурахмони Джоми           [22] Джайхун (Кумсангир)            [41] Носири Хусрав              [60] Хорог
    [4] Айни                        [23] Джалолиддина Балхи (Руми)      [42] Нурабад                    [61] Хуросон
    [5] Ашт                         [24] Джами                          [43] Нурек                      [62] Шамсиддин Шохин (Шуроабад)
    [6] Бальджуван                  [25] Дусти (Джиликуль)              [44] Пенджикент                 [63] Шахринав
    [7] Бободжон Гафуров            [26] Зафарабад                      [45] Пяндж                      [64] Шахристон
    [8] Бохтар (Курган-Тюбе)        [27] Истаравшан                     [46] Рашт                       [65] Шахритус
    [9] Бустон (Чкаловск)           [28] Истиклол                       [47] Рогун                      [66] Шугнан
    [10] Вандж                      [29] Исфара                         [48] Рошткала                   [67] Яван
    [11] Варзоб                     [30] Ишкашим                        [49] Рудаки 
    [12] Вахдат                     [31] Кабодиён                       [50] Рушан    
    [13] Вахш                       [32] Канибадам                      [51] Сангвор (Тавильдара)       
    [14] Восе                       [33] Куляб                          [52] Спитамен  
    [15] Гиссар                     [34] Кушониён (Бохтар)              [53] Таджикабад             
    [16] Горная Матча               [35] Лахш (Джиргиталь)              [54] Темурмалик
    [17] Гулистон (Кайраккум)       [36] Леваканд (Сарбанд)             [55] Турсунзаде
    [18] Дангара                    [37] Матча                          [56] Файзабад 
    ''')
        city = getDataFromUser('int', 'Город: ')
        exchange = getDataFromUser('str', 'Обмен(Да/Нет): ')
        price_min = getDataFromUser('int', 'Мин. цена: ')
        price_max = getDataFromUser('int','Макс. цена: ')
        proxies = ""
        if price_min > price_max or price_min < 0:
            print(Fore.RED + 'Неверная мин. цена')
            exit()

        if proxy_file != '':
            proxies = get_proxies(proxy_file)[0]


    return mode, city, query, price_min, price_max, exchange, save_path, proxies




if __name__ == '__main__':
    datas = main()
    sm = SomonParse()
    if datas[0] == 0:
        sm.getContacts(datas[1], datas[2], datas[3], datas[4], datas[5], datas[6], datas[7])