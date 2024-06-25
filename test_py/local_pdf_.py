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

model_local = ChatOllama(model="gemma:2b")

loader = PyPDFLoader("/home/tolasing/Downloads/pages.pdf",extract_images=True)
pdf_file_=loader.load() 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
#doc_splits = loader.load_and_split(text_splitter=text_splitter)
doc_splits = text_splitter.split_documents(documents=pdf_file_)
print("Number of chunks:", len(doc_splits))
"""
# 2. Convert documents to Embeddings and store them
vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text'),
    persist_directory="./chroma_db"
   )
vectorstore.persist()
"""
vectorstore = Chroma(
    persist_directory="./perak_maintain_db",
    collection_name="rag-chroma",
    embedding_function=embeddings.ollama.OllamaEmbeddings(model='nomic-embed-text:latest'),
    
   )
retriever = vectorstore.as_retriever(search_kwargs={"k":1})

query = "page 82"
docs = vectorstore.similarity_search(query)

# print results
print(docs[0].page_content)

# 4. After RAG

print("\n########\nAfter RAG\n")
after_rag_template = """Answer the question based only on the following context:
{context}
Question: {question}
"""

after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
after_rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | after_rag_prompt
    | model_local
    | StrOutputParser()
)
print(after_rag_chain.invoke("what is the power of the starter motor?"))

# loader = PyPDFLoader("Ollama.pdf")
# doc_splits = loader.load_and_split()
