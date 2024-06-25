from ollama import chat
import json 
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain.schema import HumanMessage



model=OllamaFunctions(model='example')
model = model.bind(
    functions=[
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, " "e.g. San Francisco, CA",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                    },
                },
                "required": ["location"],
            },
        }
    ],
    function_call={"name": "get_current_weather"},
)

response=model.invoke("how are you?")
print(response)
