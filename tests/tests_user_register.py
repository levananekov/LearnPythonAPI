import string

import pytest
import random

from lib.assertions import Assertions

from lib import BaseCase
from lib.my_requests import HttpMethod, MyRequests


class TestsUserRegister(BaseCase):
    test_data = ["password",
          "username",
          "firstName",
          "lastName",
          "email"]

    def test_create_user(self):
        data = self.prepare_registration_data()
        res = MyRequests.make_request(HttpMethod.POST, "user/", data=data)
        Assertions.assert_status_code(res, 200)
        Assertions.assert_json_has_key(res, "id")

    @pytest.mark.parametrize("test_data", test_data)
    def test_create_user_without_one_field(self, test_data):
        data = self.prepare_registration_data()
        data.pop(test_data)
        res = MyRequests.make_request(HttpMethod.POST, "user/", data=data)
        Assertions.assert_status_code(res, 400)
        assert res.text == f'The following required params are missed: {test_data}'

    def test_create_user_without_at(self):
        data = self.prepare_registration_data()
        data["email"] = data.get("email").replace("@", "")
        res = MyRequests.make_request(HttpMethod.POST, "user/", data=data)
        Assertions.assert_status_code(res, 400)
        assert res.content.decode("utf-8") == "Invalid email format"

    def test_create_user_name_length_one(self):
        data = self.prepare_registration_data()
        data["username"] = "".join(random.choices(string.ascii_lowercase, k=1))
        res = MyRequests.make_request(HttpMethod.POST, "user/", data=data)
        Assertions.assert_status_code(res, 400)
        assert res.text == "The value of 'username' field is too short"


    def test_create_user_name_max_length(self):
        data = self.prepare_registration_data()
        data["username"] = "".join(random.choices(string.ascii_lowercase, k=250))
        res = MyRequests.make_request(HttpMethod.POST, "user/", data=data)
        Assertions.assert_status_code(res, 200)
        Assertions.assert_json_has_key(res, "id")

    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        res = MyRequests.make_request(HttpMethod.POST, "user/", data=data)
        Assertions.assert_status_code(res, 400)
        assert res.content.decode("utf-8") == "Users with email 'vinkotov@example.com' already exists"
