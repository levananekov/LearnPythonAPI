from time import sleep

import requests
#
# requests_type = ["post", "get", "put", "delete"]
# params_method = ["POST", "GET", "PUT", "DELETE", "LOL"]
#
# for i in requests_type:
#     print(requests.request(method=i, url="https://playground.learnqa.ru/ajax/api/longtime_job").text)
#
# for req_type in requests_type:
#     print(f"\n Тип метода {req_type}")
#     for method in params_method:
#         data = None
#         params = None
#         if req_type == "get":
#             params = {"method": method}
#             print(f"Значение params = {params}")
#         else:
#             data = {"method": method}
#             print(f"Значение data = {data}")
#
#         print(requests.request(method=req_type,
#                                url="https://playground.learnqa.ru/ajax/api/compare_query_type",
#                                params=params,
#                                data=data).text)


longtime_job_url = "https://playground.learnqa.ru/ajax/api/longtime_job"

res = requests.request(method="get", url=longtime_job_url).json()

res_1 = requests.request(method="get", url=longtime_job_url, params = res).json()
assert res_1.get("status") == "Job is NOT ready"

sleep(res.get("seconds"))

res_2 = requests.request(method="get", url=longtime_job_url, params = res).json()
assert res_2.get("status") == "Job is ready"
assert res_2.get("result") is not None

