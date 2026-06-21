from curl_cffi.requests import AsyncSession
import pandas as pd
import asyncio


async def get_data(params):
    headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Sec-ch-ua': '"Chromium";v="146", "Google Chrome";v="146", "Not/A)Brand";v="99"',
    'Sec-ch-ua-mobile': '?0',
    'Sec-ch-ua-platform': '"Linux"',
    }
    url = 'https://search.wb.ru/exactmatch/ru/common/v18/search?curr=rub&dest=-1257786&lang=ru&locale=ru&spp=30&resultset=catalog'

    async with AsyncSession(impersonate="chrome146", headers=headers) as session:
        response = await session.get(url=url, params=params)
        print(response.status_code)
        data = response.json()
        return data['products']


def parce_products(products):
    needed = []
    for i in products:
        needed.append({'Имя': i.get('name'),
                       'Артикул': i.get('id'),
                       'Брэнд': i.get('brand'),
                       'Цена со скидкой': i.get('sizes')[0].get('price').get('product') // 100,
                       'Цена без скидок': i.get('sizes')[0].get('price').get('basic') // 100,})
        print(needed[-1])
        print("\n")
    return needed


def save_to_excel(products, filename):
    pass


async def main():
    params = {'query': 'наушники', 'sort': 'popular', 'page': 1}
    data = await get_data(params)  # await застопорит main() пока get_data() не вернёт результат, при этом пока main() стоит могут выполняться дргуие задачи (Tasks)
    parce_products(data)



if __name__ == "__main__":
    asyncio.run(main())  # Запуск цикла событий в одном потоке, с передачей в него корютины, которая становится задачей (Task) и заврещающая цикл при своём завершении
    # Важно понимать, что задачи (Tasks) не делятся на родительские и дочерние, все они просто находятся в цикле событий, в очереди на выполнение