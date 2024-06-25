
import json
import torch
from ctransformers import AutoModelForCausalLM
from transformers import AutoTokenizer,pipeline

def get_prompt(user_query: str, functions: list = []) -> str:
    """
    Generates a conversation prompt based on the user's query and a list of functions.

    Parameters:
    - user_query (str): The user's query.
    - functions (list): A list of functions to include in the prompt.

    Returns:
    - str: The formatted conversation prompt.
    """
    if len(functions) == 0:
        return f"USER: <<question>> {user_query}\nASSISTANT: "
    functions_string = json.dumps(functions)
    return f"USER: <<question>> {user_query} <<function>> {functions_string}\nASSISTANT: "

# Device setup
device : str = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Model and tokenizer setup
model_id : str = "/home/tolasing/main_ws/ml_ws/gorilla_config"
#tokenizer = AutoTokenizer.from_pretrained(model_id)
#model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True)
model = AutoModelForCausalLM.from_pretrained("/home/tolasing/main_ws/ml_ws/gorilla_config", model_file="gorilla-openfunctions-v1.Q4_K_M.gguf", model_type="llama", gpu_layers=0,hf=True)
tokenizer = AutoTokenizer.from_pretrained(model_id)
# Move model to device
model.to(device)

# Pipeline setup
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=128,
    batch_size=16,
    torch_dtype=torch_dtype,
    device=device,
)

# Example usage
query: str = "move the robot to the toilet"
functions = [
   
      {
        "name": "move Robot",
        "api_name": "move.robot",
        "description": "move the robot depending on the users request to different location of the home like kitchen,tv room,toilet,office",
        "parameters":  [
            {"name": "location", "description": "Location to move the robot to"},
            ]
    }
]

# Generate prompt and obtain model output
prompt = get_prompt(query, functions=functions)
#output = pipe(prompt)

print(prompt)
