from datetime import datetime
from lib.assertions import Assertions

from lib import BaseCase
from lib.my_requests import HttpMethod, MyRequests


class TestsUserGet(BaseCase):

    def setup(self):
        base_part = "learnqa"
        domain = "example.com"
        date_now = datetime.now().strftime("%m%d%e%H%M%S")
        self.email = f"{base_part}{date_now}@{domain}"

    def test_get_user_info_not_auth(self):
        response = MyRequests.make_request(HttpMethod.POST, "user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "email")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    def test_get_user_info_auth(self):
        data = {
            "password": "123",
            "email": "vincotov@example.com"
        }
        response = MyRequests.make_request(HttpMethod.POST, "user/login", data=data)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        user_id = self.get_json_value(response, "user_id")

        response_2 = MyRequests.make_request(HttpMethod.GET, f"user/{user_id}",
                                  headers={"x-csrf-token": token},
                                  cookies={"auth_sid": auth_sid}
                                  )
        Assertions.assert_json_has_keys(response_2, ["username", "email", "firstName", "lastName"])
