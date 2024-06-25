from ollama import chat
import json


messages = [
  {
    'role': 'user',
    'content': 'move robot to the toilet<|im_end|><|im_start|>assistant ',
  },
]

response = chat('tiny', messages=messages)

nested_json_string = response["message"]["content"]



# Parse the nested JSON string
#nested_json_data = json.loads(nested_json_string)


try:
    # Try parsing content as JSON
    content_json = json.loads(nested_json_string)
    # If parsing succeeds, content is JSON
    print("Content is JSON:", content_json)
except json.JSONDecodeError:
    # If parsing fails, content is a string
    print("Content is a string:", nested_json_string)

print(response)