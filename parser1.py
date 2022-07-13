
import requests
import json
import time




cookies = {
    '.ASPXANONYMOUS': 'VEm1QSEjlf_9TT_tOCYoqyiflKR2_F8mlumdvCNAslunfN5NZZc1SqVrdMRjuGsKsu5lYAysNKqototcOKIpNt-GsrnPgJb3JWmb9zBFygDUYQYSMMJbd-Ihf_eCytjdmyA-Zg2',
    'CustomerId': 'cbc22e09c59c4c30ac5526c6062b56de',
    'ShouldSetDeliveryOptions': 'True',
    'DontShowCookieNotification': 'true',
    'cookiesession1': '678B286ATUV012358814BDFHJLNP614C',
    '_gcl_au': '1.1.1515858139.1655465834',
    '_ym_d': '1655465834',
    '_ym_uid': '1655465834365278760',
    'tmr_lvid': '8e3f5c2c4703beb2c067908d64b8f4c7',
    'tmr_lvidTS': '1655465834450',
    '_tm_lt_sid': '1655465834468.18276',
    '_ga': 'GA1.2.43497337.1655465835',
    '_tt_enable_cookie': '1',
    '_ttp': '83968147-03de-4088-b26e-6fa9b48882a7',
    'KFP_DID': 'f7ee7d7e-c1ea-069d-80ab-3b3d22a27bdd',
    '_a_d3t6sf': 'duntDv5LADw5q4zELqjC7o_W',
    'flocktory-uuid': 'df385056-9a96-439e-ba0d-cfebaa2da7bd-8',
    'ReviewedSkus': '265072',
    'AddressTooltipInfo': 'Lenta.MainSite.Abstractions.Entities.Ecom.AddressTooltip',
    'oxxfgh': '915dae7d-b735-4a28-a385-7b3b24e07ba0#0#5184000000#5000#1800000#44965',
    'ASP.NET_SessionId': 'xckomoimhqr2wmbp5p5dysa5',
    '_ym_visorc': 'b',
    '_ym_isad': '2',
    '_gid': 'GA1.2.1527031648.1657694395',
    '_dc_gtm_UA-327775-35': '1',
    'tmr_detect': '0%7C1657694436584',
    'tmr_reqNum': '88',
}

headers = {
    'Accept': 'application/json',
    'Accept-Language': 'ru-RU,ru;q=0.9',
    'Connection': 'keep-alive',
    'Origin': 'https://lenta.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
    'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


 #коды всех категорий 
nodeCode = ['g6b6be260dbddd6da54dcc3ca020bf380',  
'gd6dd9b5e854cf23f28aa622863dd6913',
'g301007c55a37d7ff8539f1f169a4b8ae',
'g68552e15008531b8ae99799a1d9391df',
'g7cc5c7251a3e5503dc4122139d606465',
'g1baf1ddaa150137098383967c9a8e732',
'g604e486481b04594c32002c67a2b459a',
'g523853c00788bbb520b022c130d1ae92',
'g1d79df330af0458391dd6307863d333e',
'geee7643ec01603a5db2cf4819de1a033',
'g9290c81c23578165223ca2befe178b47'
]

#функция для отправки запроса 
def get_url(url,json_data):
    response = requests.post(url, cookies=cookies, headers=headers, json=json_data, timeout=30)
    print(response.status_code)
    return response
    
#функция для сохранения данных в Json файл
def save_data(response):
    with open ('data.json', 'a') as f:
        json.dump(response.json(),f, indent=4)

#функция для сбора нужных данных и вывода их в консоль
def collect_data(response,product_list):
    data = response.json()
    products = data['skus']
    for name in products:
        name_product = name['title']
        product_list.append(name_product)
        price_product = name['cardPrice']['value']
        product_list.append(price_product)
        price_WithoutNds_product = name['priceWithoutNds']['value']
        product_list.append(price_WithoutNds_product)
    return product_list




def main():
    f = open('data.json','w') #очистка файла по нужному адресу
    f.close()
    for code in nodeCode: #цикл для прохождения всех категорий 
        json_data = {
        'nodeCode': code,
        'filters': [],
        'typeSearch': 1,
        'sortingType': 'ByPopularity',
        'offset': 0,
        'limit': 100,
        'updateFilters': True,
        }


        url = 'https://lenta.com/api/v1/skus/list'
        response = get_url(url,json_data)
        data = response.json()
        count_product = data['totalCount'] #получаем количество товара в категории
            
        for offset in range(0,count_product+1,50): #цикл для прохода всех товаров в категории
            data = {
                'nodeCode': code,
                'filters': [],
                'typeSearch': 1,
                'sortingType': 'ByPopularity',
                'offset': offset,
                'limit': 100,
                'updateFilters': True,
            }
            response = get_url(url,data)
            print(offset,'/',count_product)
            time.sleep(1.5)
            if (response.status_code == 200): #если код ответа 200 то вызовем функции для сохранения и вывода данных 
                save_data(response)
                product_list = [] #в product_list запишем данных которые хотим вывести в консоль
                product_list = collect_data(response,product_list)
                print(product_list)




if __name__ == '__main__':
    main()
