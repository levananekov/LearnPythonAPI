import pytest
from lib import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests, HttpMethod
import allure

@allure.epic("Authorization cases")
@allure.feature("Проверка авторизации")
@pytest.mark.authorization
class TestsUserAuth(BaseCase):
    params = ["no_cookies", "no_headers"]

    def setup(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        # response = requests.post(url="https://playground.learnqa.ru/api/user/login", data=data)
        response = MyRequests.make_request(HttpMethod.POST, "user/login", data=data)
        self.auth_sid = self.get_cookie(response, "auth_sid")
        self.token = self.get_header(response, "x-csrf-token")
        self.user_id = self.get_json_value(response, "user_id")

    @allure.title("Авторизация в ЛК по логину.")
    @allure.description("Авторизация с логином и паролем")
    @allure.id("1")
    def test_user_auth(self):

        response_2 = MyRequests.make_request(HttpMethod.GET, "user/auth",
                                  headers={"x-csrf-token": self.token},
                                  cookies={"auth_sid": self.auth_sid}
                                  )
        Assertions.assert_json_value_by_name(response_2, "user_id", self.user_id, "Нет id")

    @allure.description("Прроверяем статус авторизации без куки или хедера")
    @pytest.mark.parametrize("condition", params)
    @allure.id("2")
    def test_negative_auth_check(self, condition):

        if condition is "no_cookies":
            cookies = None
            headers = {"x-csrf-token": self.token}
        elif condition is "no_headers":
            cookies = {"auth_sid": self.auth_sid}
            headers = None
        else:
            raise RuntimeError("Кривые руки")

        res = MyRequests.make_request(HttpMethod.GET, "user/auth", headers=headers, cookies=cookies)

        Assertions.assert_json_value_by_name(res, "user_id", 0, "user_id не равен 0" )
