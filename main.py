import json

json_text = '{"messages":[' \
                '{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},' \
                '{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}' \
            ']}'

json_messages = json.loads(json_text).get("messages")
second_json_message = json_messages[1].get("message")

print(second_json_message)
