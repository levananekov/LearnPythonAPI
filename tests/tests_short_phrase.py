import requests

def test_homework_headers():
    response = requests.get(url="https://playground.learnqa.ru/api/homework_header")
    assert response.headers.get("x-secret-homework-header"), "Cookie does't matter Homework"