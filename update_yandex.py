import sqlite3
import requests
import os

API_TOKEN = "YOUR_YANDEX_API_TOKEN"
CLID = "YOUR_CLID"

def update_yandex_prices():
    url = "https://yandex.ru"

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json"
    }

    model_numbers = [14, 15, 16, 17]
    memory_options = ["128GB", "256GB"]

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "database", "prices.db")

    for model in model_numbers:
        for memory in memory_options:
            params = {
                "query": f"iPhone {model} {memory}",
                "clid": CLID,
                "count": 1
            }

            try:
                print(f"🔄 Запрашиваю Яндекс для iPhone {model} {memory}...")
                response = requests.get(url=url, headers=headers, params=params, timeout=10)

                if response.status_code == 200:
                    data = response.json()

                    if data.get("results"):
                        product = data["results"][0]
                        name = product["name"]
                        price = product["price"]["value"]
                        ref_link = product["link"]

                        conn = sqlite3.connect(db_path)
                        cursor = conn.cursor()

                        cursor.execute("""
                        INSERT OR REPLACE INTO yandex_prices (model_number, memory, model_name, price, partner_link)
                        VALUES (?, ?, ?, ?, ?)
                        """, (model, memory, name, int(price), ref_link))

                        conn.commit()
                        conn.close()
                        print(f"✅ База обновлена: {name} -> {price} руб.")
                else:
                    print(f"❌ Ошибка Яндекса: {response.status_code}")

            except Exception as e:
                print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    update_yandex_prices()

