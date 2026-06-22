from curl_cffi.requests import AsyncSession
import pandas as pd
import random
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
        # print(needed[-1])
        # print("\n")
    return needed


def save_to_excel(products, filename):
    tabl = pd.DataFrame(data=products)
    print(tabl)
    tabl.to_excel(f"{filename}.xlsx", index=False)


async def main():
    while True:
        pages = input("Сколько страниц с товаром нужно? ")
        try:
            int(pages)
        except:
            print("Введи ЧИСЛО")
            continue
        if (int(pages) > 10):
            print("Извините, но этот парсер рассчитан максимум на 10 страниц")
            continue
        break

    for i in range(1, pages + 1):
        params = {'query': 'шампунь', 'sort': 'popular', 'page': i}
        await asyncio.sleep(random.uniform(2.1, 4.8))
        data = await get_data(params)  # await застопорит main() пока get_data() не вернёт результат, при этом пока main() стоит могут выполняться дргуие задачи (Tasks)
        products = parce_products(data)
        save_to_excel(products=products, filename='TABL')



if __name__ == "__main__":
    asyncio.run(main())  # Запуск цикла событий в одном потоке, с передачей в него корютины, которая становится задачей (Task) и заверщающая цикл при своём завершении
    # Важно понимать, что задачи (Tasks) не делятся на родительские и дочерние, все они просто находятся в цикле событий, в очереди на выполнение