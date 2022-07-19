from lib.assertions import Assertions

from lib import BaseCase
from lib.my_requests import HttpMethod, MyRequests


class TestsUserRegister(BaseCase):

    def test_create_user(self):
        data = self.prepare_registration_data()

        res = MyRequests.make_request(HttpMethod.POST, "user/", data=data)
        Assertions.assert_status_code(res, 200)
        Assertions.assert_json_has_key(res, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        res = MyRequests.make_request(HttpMethod.POST, "user/", data=data)
        Assertions.assert_status_code(res, 400)
        assert res.content.decode("utf-8") == "Users with email 'vinkotov@example.com' already exists"