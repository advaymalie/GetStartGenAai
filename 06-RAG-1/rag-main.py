
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore


load_dotenv()
pdf_path = Path(__file__).parent / "NodeJS.PDF"

#Loading
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load()

# print("Docs[0]", docs[1])
# docs[0].split("\n")

# Chunking 
text_spliter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

split_docs = text_spliter.split_documents(documents=docs)

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# Using [embedding_model] create embedding of [split_docs] and store in vector DB
# Vector DB -  Pinecone DB (cloud and paid), Weaviate DB, Astra DB, Chroma DB, Milvus DB, PG Vector DB, QDrant DB
vector_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)

print("Indexing of documents Done...")

