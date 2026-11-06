import requests

url = "http://127.0.0.1:5000/notes"

print("--- ТЕСТ 1: СОЗДАНИЕ ---")
r = requests.post(url, json={"author": "Анна", "text": "Привет"})
print("Создание 1:", r.status_code, r.json())

r = requests.post(url, json={"author": "Иван", "text": "Как дела?"})
print("Создание 2:", r.status_code, r.json())

r = requests.post(url, json={"author": "Анна", "text": "Хорошо"})
print("Создание 3:", r.status_code, r.json())

print("\n--- ТЕСТ 2: ЛАЙКИ ---")
r = requests.post(f"{url}/1/like")
print("Лайк заметки 1:", r.status_code, r.json())

r = requests.post(f"{url}/1/like")
print("Еще лайк заметки 1:", r.status_code, r.json())

r = requests.post(f"{url}/2/like")
print("Лайк заметки 2:", r.status_code, r.json())

r = requests.post(f"{url}/999/like")
print("Лайк несуществующей (404):", r.status_code, r.json())

print("\n--- ТЕСТ 3: СОРТИРОВКА ---")
r = requests.get(f"{url}?sort=likes&order=desc")
print("Сортировка по лайкам (убывание):", r.status_code, r.json())

r = requests.get(f"{url}?sort=abc")
print("Неизвестный sort (400):", r.status_code, r.json())

r = requests.get(f"{url}?order=random")
print("Неизвестный order (400):", r.status_code, r.json())

print("\n--- ТЕСТ 4: СТАТИСТИКА ПО АВТОРАМ ---")
r = requests.get("http://127.0.0.1:5000/authors")
print("Статистика:", r.status_code, r.json())

print("\n--- ТЕСТ 5: МАССОВОЕ УДАЛЕНИЕ ---")
r = requests.delete(f"{url}?author=Иван")
print("Удаление всех заметок Ивана:", r.status_code, r.json())

r = requests.delete(f"{url}?author=Иван")
print("Повторное удаление Ивана:", r.status_code, r.json())

r = requests.delete(f"{url}")
print("Удаление без автора (400):", r.status_code, r.json())