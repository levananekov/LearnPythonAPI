import json

from requests import Response


class BaseCase:
    def get_cookie(self, response: Response, cookie_name: str):
        assert cookie_name in response.cookies, f"Cannot find cookie with name {cookie_name} in the last response"
        return response.cookies.get(cookie_name)

    def get_header(self, response: Response, headers_name: str):
        assert headers_name in response.headers, f"Cannot find headers with name {headers_name} in the last response"
        return response.headers.get(headers_name)

    def get_json_value(self,  response: Response, name: str):
        try:
            if json_as_dict := response.json():
                assert name in json_as_dict, f"Response JSON does`t have key {name}"
                return json_as_dict.get(name)
        except json.JSONDecoder:
            assert False, "Response in not in JSON format."
