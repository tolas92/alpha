from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community import embeddings
from langchain_community.chat_models import ChatOllama
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.text_splitter import CharacterTextSplitter
from langchain.text_splitter import RecursiveCharacterTextSplitter

model_local = ChatOllama(model="gemma:7b",temperature=1.0)
"""
# 1. Split data into chunks
urls = [
    "https://ollama.com/",
    "https://ollama.com/blog/windows-preview",
    "https://ollama.com/blog/openai-compatibility",
]
docs = [WebBaseLoader(url).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]
"""

loader = PyPDFLoader("/home/tolasing/main_ws/ml_ws/allPages.pdf",extract_images=True)
pdf_file_=loader.load() 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)
#doc_splits = loader.load_and_split(text_splitter=text_splitter)
doc_splits = text_splitter.split_documents(documents=pdf_file_)
print("Number of chunks:", len(doc_splits))

# 2. Convert documents to Embeddings and store them
vectorstore = Chroma.from_documents(
    documents=pdf_file_,
    collection_name="rag-chroma",
    embedding=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text:latest'),
    persist_directory="./perak_maintain_db"
   )
vectorstore.persist()
retriever = vectorstore.as_retriever(search_kwargs={"k":1})

# 4. After RAG
print("\n########\nAfter RAG\n")
after_rag_template = """Answer the question based on the below content:
{page}
Question: {question}
"""
after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
after_rag_chain = (
    {"page": retriever, "question": RunnablePassthrough()}
    | after_rag_prompt
    | model_local
    | StrOutputParser()
)
print(after_rag_chain.invoke("whats in page 82?"))

# loader = PyPDFLoader("Ollama.pdf")
# doc_splits = loader.load_and_split()
