import requests
from lxml import html

response = requests.get("https://en.wikipedia.org/wiki/List_of_the_most_common_passwords")
tree = html.fromstring(response.text)
locator = '//*[contains(text(),"Top 25 most common passwords by year according to SplashData")]//..//td[@align="left"]/text()'
passwords = tree.xpath(locator)

for password in passwords:
    password = str(password).strip()
    res_cookies = requests.post(url="https://playground.learnqa.ru/ajax/api/get_secret_password_homework",
                                data={"login": "super_admin", "password": password}).cookies

    res_text = requests.post("https://playground.learnqa.ru/ajax/api/check_auth_cookie", cookies=res_cookies).text
    print(f"Пароль {password} неверный")
    if res_text != "You are NOT authorized":
        print(f"Верный пароль {password}")
        break
