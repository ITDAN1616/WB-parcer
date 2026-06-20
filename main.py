from curl_cffi.requests import AsyncSession
import asyncio

session = AsyncSession(impersonate="chrome146")


async def get_data(params):
    headers = {
    'User-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Sec-ch-ua': '"Chromium";v="146", "Google Chrome";v="146", "Not/A)Brand";v="99"',
    'Sec-ch-ua-mobile': '?0',
    'Sec-ch-ua-platform': '"Linux"',
    'Cookie': 'x_wbaas_token=1.1000.887ab860685b454d83eccc2528ad4c9f.MHw3OC44NS40OS4yN3xNb3ppbGxhLzUuMCAoWDExOyBMaW51eCB4ODZfNjQpIEFwcGxlV2ViS2l0LzUzNy4zNiAoS0hUTUwsIGxpa2UgR2Vja28pIENocm9tZS8xNDguMC4wLjAgU2FmYXJpLzUzNy4zNnwxNzgyMDIxNTkxfHJldXNhYmxlfDJ8ZXlKb1lYTm9Jam9pSW4wPXwwfDN8MTc4MTg5MTk5MXwx.MEUCIQDu3/q7ipdph67QH7QBCsPB53tX3FEq/EdXvWkqXZxx8wIgSZE+PTn2+hhqBKPfFM+V76fiwisWZQNCEtU5wcaO1qI=; _wbauid=2455341001781762398; _cp=1'
    }
    url = 'https://www.wildberries.ru/__internal/u-search/exactmatch/ru/common/v18/search?curr=rub&dest=-1257786&lang=ru&locale=ru&spp=30&resultset=catalog'

    response = await session.get(url=url, headers=headers, params=params)
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


async def main():
    params = {'query': 'наушники', 'sort': 'popular', 'page': 1}
    data = await get_data(params)
    parce_products(data)



if __name__ == "__main__":
    asyncio.run(main())