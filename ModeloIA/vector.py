from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import os

def process_pdfs(pdf_folder):
    documents = []
    
    # Cargar todos los PDFs de la carpeta
    for file in os.listdir(pdf_folder):
        if file.endswith(".pdf"):
            loader = PyPDFLoader(os.path.join(pdf_folder, file))
            documents.extend(loader.load())
    
    # Dividir en chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    return text_splitter.split_documents(documents)

# Uso
documents = process_pdfs("leyes_transito")

# Crear embeddings (usando mxbai-embed-large)
embeddings = OllamaEmbeddings(
    model="mxbai-embed-large",
    base_url="http://localhost:11434"
)

# Construir base vectorial
vectorstore = FAISS.from_documents(documents, embeddings)
vectorstore.save_local("legal_embeddings")

print("Embeddings generados y almacenados")
