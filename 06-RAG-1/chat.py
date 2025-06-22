# chat.py: The Retrieval and Generation Pipeline
# -----------------------------------------------
# This script is responsible for the "Retrieval & Generation" phase of the RAG pipeline.
# It performs the following steps:
# 1. Takes a query from the user.
# 2. Connects to the existing Qdrant vector database.
# 3. Embeds the user's query into a vector using the same model as the indexing script.
# 4. Performs a similarity search in the vector database to find the most relevant chunks.
# 5. Constructs a detailed prompt for the LLM, including the retrieved chunks as context.
# 6. Sends the prompt to the LLM and prints the final, context-aware answer.

from dotenv import load_dotenv
from langchain_qdrant import Qdrant
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI

# Load environment variables.
load_dotenv()

# Initialize the OpenAI client for the final LLM call.
client = OpenAI()

# --- 1. Connect to the Vector Database ---
# Use the same embedding model and collection name as in the indexing script
# to ensure consistency.
print("Connecting to vector database...")
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = Qdrant.from_existing_collection(
    embedding=embedding_model,
    url="http://localhost:6333",
    collection_name="learning_vectors",
)
print("Connection successful.")

# --- 2. Get User Query ---
user_query = input("\nPlease enter your question about the document: \n> ")

# --- 3. Perform Similarity Search ---
# The user's query is embedded, and the vector database is searched to find
# the chunks with the most similar embeddings. These are the most relevant
# pieces of information from the document to answer the user's query.
print("\nSearching for relevant context...")
search_results = vector_db.similarity_search(
    query=user_query,
    k=3  # Retrieve the top 3 most relevant chunks.
)
print(f"Found {len(search_results)} relevant chunks.")

# --- 4. Format the Context ---
# The retrieved search results are formatted into a single string.
# We include the page content and the page number (from metadata) for each chunk.
# This provides the LLM with both the information and its source.
context = "\n\n---\n\n".join([
    f"Page Content: {result.page_content}\n"
    f"Source File: {result.metadata.get('source', 'N/A')}, "
    f"Page Number: {result.metadata.get('page', 'N/A') + 1}"
    for result in search_results
])

# --- 5. Construct the Final Prompt ---
# A detailed system prompt is created. It instructs the LLM on its role and how to use
# the provided context. This is the core of "Retrieval-Augmented Generation".
SYSTEM_PROMPT = f"""
You are a helpful AI assistant. Your task is to answer the user's query based ONLY on the following context retrieved from a PDF document.

The context below contains excerpts from the document, along with the source file and page number where the information can be found.

When you answer, you must:
1.  Provide a clear and concise answer to the user's question.
2.  Base your answer strictly on the provided context. Do not use any external knowledge.
3.  After your answer, cite the source and page number(s) where the information was found. For example: "(Source: NodeJS.PDF, Page: 15)".

Here is the context:
---
{context}
---
"""

# --- 6. Send to LLM and Get Answer ---
# The final prompt (including the context) and the user's original query are sent
# to the chat model to generate the final answer.
print("Sending request to LLM...")
chat_completion = client.chat.completions.create(
    model="gpt-4-turbo",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
)

# --- 7. Print the Final Answer ---
print("\n🤖 AI Assistant says:\n")
print(chat_completion.choices[0].message.content)
