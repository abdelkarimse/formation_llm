from langchain_community.document_loaders import PyPDFLoader
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate
import shutil
import os

loader = PyPDFLoader("./services/document/ISITCOM_MARS_Lab_Report.pdf")
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=200,
    length_function=len,
    separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
)
all_splits = text_splitter.split_documents(docs)

print(f"Created {len(all_splits)} chunks from {len(docs)} pages\n")


if os.path.exists("./chroma_db"):
    shutil.rmtree("./chroma_db")

embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = Chroma.from_documents(
    documents=all_splits,
    embedding=embeddings,
    persist_directory="./chroma_db"
)


def query_pdf(question: str):
    results = vector_store.similarity_search_with_score(question, k=3)
    
   
    context = "\n\n".join(doc.page_content for doc, _ in results)
    
    prompt_text = f"""Based on the context below, answer the question concisely.

Context:
{context}

Question: {question}

Answer:"""
    
    return prompt_text
