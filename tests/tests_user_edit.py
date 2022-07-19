import random
import string

from lib.assertions import Assertions
from lib import BaseCase
from lib.my_requests import MyRequests, HttpMethod


class TestsUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.make_request(HttpMethod.POST, "user", data=register_data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")

        # login
        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }

        response2 = MyRequests.make_request(HttpMethod.POST, "user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_name = "Change name"
        response3 = MyRequests.make_request(HttpMethod.PUT, f"user/{user_id}",
                                            headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid},
                                            data={"firstName": new_name})

        Assertions.assert_status_code(response3, 200)

        # get
        response4 = MyRequests.make_request(HttpMethod.GET, f"user/{user_id}",
                                            headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid}
                                            )
        Assertions.assert_json_value_by_name(response4, "firstName", new_name, "у меня болит тут)")

    def test_edit_unauthorized_user(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.make_request(HttpMethod.POST, "user", data=register_data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")

        new_name = "Change name"
        response3 = MyRequests.make_request(HttpMethod.PUT, f"user/{user_id}",
                                            headers={"x-csrf-token": None},
                                            cookies={"auth_sid": None},
                                            data={"firstName": new_name})

        Assertions.assert_status_code(response3, 400)
        assert response3.text == 'Auth token not supplied'

    def test_edit_authorized_another_user(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.make_request(HttpMethod.POST, "user", data=register_data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")

        # login
        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }

        response2 = MyRequests.make_request(HttpMethod.POST, "user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_name = "Change name"
        response3 = MyRequests.make_request(HttpMethod.PUT, f"user/{int(user_id) - 1}",
                                            headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid},
                                            data={"firstName": new_name})

        Assertions.assert_status_code(response3, 200)

        response4 = MyRequests.make_request(HttpMethod.GET, f"user/{int(user_id) - 1}",
                                            headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid}
                                            )
        Assertions.assert_json_value_by_name_not_equal(response4, "username", new_name, "Ооу нет имя поменялось")

    def test_edit_just_created_user_without_at(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.make_request(HttpMethod.POST, "user", data=register_data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")

        # login
        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }

        response2 = MyRequests.make_request(HttpMethod.POST, "user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        new_email = login_data.get("email").replace("@", "")
        response3 = MyRequests.make_request(HttpMethod.PUT, f"user/{user_id}",
                                            headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid},
                                            data={"email": new_email})

        Assertions.assert_status_code(response3, 400)
        assert response3.text == 'Invalid email format', 'мыло поменяло на кривое'

    def test_edit_just_created_user_length_one_symbol(self):
        register_data = self.prepare_registration_data()
        response = MyRequests.make_request(HttpMethod.POST, "user", data=register_data)
        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, "id")

        user_id = self.get_json_value(response, "id")

        # login
        login_data = {
            "email": register_data["email"],
            "password": register_data["password"]
        }

        response2 = MyRequests.make_request(HttpMethod.POST, "user/login", data=login_data)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        first_name = "".join(random.choices(string.ascii_lowercase, k=1))
        response3 = MyRequests.make_request(HttpMethod.PUT, f"user/{user_id}",
                                            headers={"x-csrf-token": token},
                                            cookies={"auth_sid": auth_sid},
                                            data={"firstName": first_name})

        Assertions.assert_status_code(response3, 400)
        assert response3.text == '{"error":"Too short value for field firstName"}', 'Неверная ощибка'
