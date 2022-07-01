import requests

def test_homework_cookie():
    response = requests.get(url="https://playground.learnqa.ru/api/homework_cookie")
    assert response.cookies.get('HomeWork'), "Cookie does't matter Homework"