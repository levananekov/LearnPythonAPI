import logging

import allure
import requests
from yarl import URL
from typing import Any, Dict, Mapping, Optional, Union

import enum

from environment import StageSettings

LOGGER = logging.getLogger(__name__)


class HttpMethod(str, enum.Enum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class MyRequests:

    @staticmethod
    def _tail_url(tail_url: str) -> URL:
        url = StageSettings().connection_url
        return url / tail_url

    @staticmethod
    def make_request(
            method: HttpMethod,
            url: str,
            params: Optional[Dict[str, Any]] = None,
            json: Optional[Dict[str, Any]] = None,
            data: Optional[Union[str, bytes, Mapping[Any, Any]]] = None,
            verify: bool = True,
            **kwargs
    ) -> requests.Response:
        with allure.step(f"{method.value.upper()} запрос по url {url}"):
            url = MyRequests._tail_url(url).human_repr()
            LOGGER.info("Request: method-%s, url-%s, params-%s, json-%s, kwargs-%s", method.value, url, params, json,
                        {**kwargs})
            response = requests.request(
                method=method.value,
                url=url,
                params=params,
                json=json,
                data=data,
                verify=verify,
                **kwargs)
        LOGGER.info("Response: code - %s, text - %s,headers-%s, cookies-%s", response.status_code, response.text,
                    response.headers, response.cookies)
        return response
