from ollama import chat
import json 
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain.schema import HumanMessage
from langchain_community.llms import Ollama


model=OllamaFunctions(model='example')
model = model.bind(
    functions=[
        {
            "name": "move_the_robot",
            "description": "move the robot to the requested location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The locations in the home , " "e.g. Kitchen,TV room,Toilet",
                    },
                },
                "required": ["location"],
            },
        }
    ],
    function_call={"name": "move_the_robot"},
)

llm = Ollama(model="example")

llm.invoke("Tell me a joke")

response=model.invoke("how are you?")
print(response)
