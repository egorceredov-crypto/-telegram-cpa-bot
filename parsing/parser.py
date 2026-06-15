import time
import requests
from bs4 import BeautifulSoup


def parse_by_model(model_number: int):
    # Используем точную ссылку на общий каталог, где лежат все телефоны
    url = "https://msk.stores-apple.com/catalog/iphones/"

    print(f"\n---- Анализирую код страницы для iPhone {model_number} ----")
    print(f"🔗 Ссылка отправки запроса: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        res = requests.get(url=url, headers=headers, timeout=10)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, "html.parser")

        frame_elements = soup.find_all("div", class_="item-parent")
        parsed_data = []
        seen_models = set()

        for font in frame_elements:
            try:
                link_element = font.find("a", class_="dark_link")
                if link_element and link_element.has_attr("href"):
                    name = link_element.text.strip()

                    # СТРОГИЙ ФИЛЬТР: Если мы ищем, например, 13-й айфон, а в названии товара нет строки "13" — пропускаем!
                    # Это уберет 15 и 16 модели из выдачи для iPhone 13.
                    if f" {model_number}" not in name and f" {model_number}e" not in name:
                        continue

                    # ПРАВИЛЬНАЯ СБОРКА ССЫЛКИ (Убирает баг 404 со скриншота)
                    href = link_element["href"]
                    if href.startswith("http"):
                        link = href
                    else:
                        # Если ссылка начинается со слэша, склеиваем аккуратно
                        if href.startswith("/"):
                            link = "https://msk.stores-apple.com" + href
                        else:
                            link = "https://msk.stores-apple.com/" + href
                else:
                    continue

                if name in seen_models:
                    continue
                seen_models.add(name)

                price_element_discount = font.find("div", class_="price_value_sale")
                if price_element_discount:
                    price_raw = price_element_discount.text.strip()
                else:
                    price_element_basic = font.find("span", class_="price_value")
                    price_raw = price_element_basic.text.strip() if price_element_basic else "0"

                clean_price = "".join(filter(str.isdigit, price_raw))
                price_num = int(clean_price) if clean_price else 0

                if price_num > 0:
                    parsed_data.append({
                        "name": name,
                        "price": price_num,
                        "link": link
                    })

            except Exception as e:
                print(f"Ошибка в цикле парсера: {e}")

        # Сортируем от самых дешевых к дорогим
        parsed_data.sort(key=lambda x: x['price'])
        print(f"Успешно! Найдено строго моделей iPhone {model_number}: {len(parsed_data)}")
        return parsed_data

    except Exception as e:
        print(f"Ошибка сети при парсинге: {e}")
        return []

#Временная заглушка
def parse_yandex_market(model_number: int):
    return {
        "price": 70000,
        "link": "https://yandex.ru"
    }
