from typing import Union

from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value: Union[str, int], error_massage: str):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, "Response in not in JSON format."
        assert name in response_as_dict, f"Response JSON doesnt have key {name}"
        assert response_as_dict[name] == expected_value, error_massage

    @staticmethod
    def assert_json_value_by_name_not_equal(response: Response, name, expected_value: Union[str, int], error_massage: str):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, "Response in not in JSON format."
        assert name in response_as_dict, f"Response JSON doesnt have key {name}"
        assert response_as_dict[name] != expected_value, error_massage

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, "Response in not in JSON format."
        assert name in response_as_dict, f"Response JSON dosnt have key {name}"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, "Response in not in JSON format."
        for name in names:
            assert name in response_as_dict, f"Response JSON dosnt have key {name}"

    @staticmethod
    def assert_json_has_no_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, "Response in not in JSON format."
        assert name not in response_as_dict, f"Response JSON have key {name}"

    @staticmethod
    def assert_json_has_no_keys(response: Response, names):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, "Response in not in JSON format."
        for name in names:
            assert name not in response_as_dict, f"Response JSON have key {name}"

    @staticmethod
    def assert_status_code(response: Response, expected_status_code: int):
        assert response.status_code == expected_status_code, "Неверный status_code"
