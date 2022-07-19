from lib import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests, HttpMethod


class TestUserDelete(BaseCase):


    def test_delete_user_2(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response = MyRequests.make_request(HttpMethod.POST, "user/login", data=data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        user_id = self.get_json_value(response, "user_id")

        res = MyRequests.make_request(HttpMethod.DELETE, f"user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )

        Assertions.assert_status_code(res, 400)
        response2 = MyRequests.make_request(HttpMethod.GET, "user/auth",
                                headers={"x-csrf-token": token},
                                cookies={"auth_sid": auth_sid}
                                )
        Assertions.assert_json_value_by_name(response2, "user_id", user_id, "Нет id")
        assert res.text == 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.', "Не по плану"

    def test_delete_my_user(self):
        data = self.prepare_registration_data()
        response = MyRequests.make_request(HttpMethod.POST, "user/", data=data)
        data_login = {
            "email": data.get("email"),
            "password": data.get("password")
        }
        response2 = MyRequests.make_request(HttpMethod.POST, "user/login", data=data_login)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        user_id = self.get_json_value(response2, "user_id")

        response3 = MyRequests.make_request(HttpMethod.DELETE, f"user/{user_id}",
                                      headers={"x-csrf-token": token},
                                      cookies={"auth_sid": auth_sid}
                                      )
        Assertions.assert_status_code(response3, 200)

        response4 = MyRequests.make_request(HttpMethod.GET, f"user/{user_id}",
                                             headers={"x-csrf-token": token},
                                             cookies={"auth_sid": auth_sid}
                                             )
        Assertions.assert_status_code(response4, 404)
        assert response4.text == 'User not found', "неверный текст ошибки"