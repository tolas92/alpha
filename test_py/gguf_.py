from ctransformers import AutoModelForCausalLM

# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
llm = AutoModelForCausalLM.from_pretrained("/home/tolasing/main_ws/ml_ws/gorilla_config", model_file="gorilla-openfunctions-v1.Q4_K_M.gguf", model_type="llama", gpu_layers=0)

print(llm("AI is going to"))
