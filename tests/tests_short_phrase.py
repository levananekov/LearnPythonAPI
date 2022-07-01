import requests

def test_homework_headers():
    response = requests.get(url="https://playground.learnqa.ru/api/homework_cookie")
    assert response.headers.get('Set-Cookie'), "Cookie does't matter Homework"