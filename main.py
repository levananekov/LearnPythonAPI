import requests

res = requests.get("https://playground.learnqa.ru/api/long_redirect")

print(len(res.history))
print(res.url)
