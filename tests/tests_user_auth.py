import pytest
import requests
from lib import BaseCase


class TestsUserAuth(BaseCase):
    params = ["no_cookies", "no_headers"]

    def setup(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response = requests.post(url="https://playground.learnqa.ru/api/user/login", data=data)

        self.auth_sid = self.get_cookie(response, "auth_sid")
        self.token = self.get_header(response, "x-csrf-token")
        self.user_id = self.get_json_value(response, "user_id")

    def test_user_auth(self):

        response_2 = requests.get(url="https://playground.learnqa.ru/api/user/auth",
                                  headers={"x-csrf-token": self.token},
                                  cookies={"auth_sid": self.auth_sid}
                                  )
        assert self.user_id == response_2.json().get("user_id")

    @pytest.mark.parametrize("condition", params)
    def test_negative_auth_check(self, condition):

        if condition is "no_cookies":
            cookies = None
            headers = {"x-csrf-token": self.token}
        elif condition is "no_headers":
            cookies = {"auth_sid": self.auth_sid}
            headers = None
        else:
            raise RuntimeError("Кривые руки")

        assert 0 == requests.get(url="https://playground.learnqa.ru/api/user/auth", headers=headers, cookies=cookies
                                 ).json().get("user_id"), "user_id не равен 0"
