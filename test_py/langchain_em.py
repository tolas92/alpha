from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import AutoModel

model = AutoModel.from_pretrained('/home/tolasing/Downloads/hindi_intfloat', trust_remote_code=True) 
model_name = "/home/tolasing/Downloads/hindi_intfloat"
model_kwargs={"trust_remote_code":True}

embed=HuggingFaceEmbeddings(model_name="/home/tolasing/Downloads/hindi_s2")

text = "This is a test document."

query_result = embed.embed_query(text)

print(query_result[:3])