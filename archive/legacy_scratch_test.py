import os
import sys

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

DB_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vectorstore = Chroma(
    collection_name="dojo_knowledge",
    embedding_function=embeddings,
    persist_directory=DB_PATH
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 6})

query = "(Estoy trabajando activamente en la Campaña py-basico, Misión b00_assessment). de que trata esta mision?"
docs = retriever.invoke(query)

for i, d in enumerate(docs):
    print(f"--- Doc {i+1} : {d.metadata.get('source')} ---")
    print(d.page_content[:200])
