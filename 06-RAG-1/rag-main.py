# rag-main.py: The Indexing Pipeline
# ------------------------------------
# This script is responsible for the "Indexing" phase of the RAG pipeline.
# It performs the following steps:
# 1. Loads a PDF document from a specified path.
# 2. Splits the document into smaller, manageable chunks.
# 3. Uses an embedding model to convert each chunk into a vector.
# 4. Stores these vectors and their corresponding text in a Qdrant vector database.
# This script only needs to be run once to populate the database with the document's knowledge.

from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import Qdrant

# Load environment variables from a .env file (e.g., for API keys).
load_dotenv()

# Define the path to the PDF file to be indexed.
pdf_path = Path(__file__).parent / "NodeJS.PDF"

# --- 1. Loading the Document ---
# PyPDFLoader is used to load and parse the PDF file into a list of Document objects.
# Each Document object represents a page in the PDF.
print("Loading document...")
loader = PyPDFLoader(file_path=str(pdf_path))
docs = loader.load()
print(f"Loaded {len(docs)} pages from the document.")

# --- 2. Chunking the Document ---
# The document is split into smaller chunks to fit into the model's context window
# and to allow for more precise retrieval of relevant information.
# RecursiveCharacterTextSplitter tries to split text based on a hierarchy of separators
# (like paragraphs, then sentences) to keep related text together.
print("Splitting document into chunks...")
text_spliter = RecursiveCharacterTextSplitter(
    chunk_size=1000,    # The maximum size of each chunk (in characters).
    chunk_overlap=200   # The number of characters to overlap between chunks to maintain context.
)
split_docs = text_spliter.split_documents(documents=docs)
print(f"Document split into {len(split_docs)} chunks.")

# --- 3. Creating Vector Embeddings ---
# An embedding model is used to convert the text chunks into numerical vectors.
# These vectors capture the semantic meaning of the text.
print("Creating vector embeddings...")
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

# --- 4. Storing in Vector Database ---
# The vectorized chunks are stored in a vector database for efficient similarity search.
# We are using Qdrant for this purpose. The `from_documents` method handles the
# embedding and storing process in one step.
# This requires a Qdrant instance to be running at the specified URL.
print("Storing chunks in Qdrant vector database...")
vector_store = Qdrant.from_documents(
    documents=split_docs,
    embedding=embedding_model,
    url="http://localhost:6333",              # URL of your Qdrant instance.
    collection_name="learning_vectors",     # Name for the collection in Qdrant.
    force_recreate=True,                    # Set to True to overwrite the collection if it exists.
)

print("\n--- Indexing of documents is Done! ---")
print("You can now run chat.py to ask questions about your document.")
