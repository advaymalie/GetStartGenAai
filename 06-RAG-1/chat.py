from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI


load_dotenv()

client = OpenAI()
# Take user query


# Vector Embeddings model
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
)

vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="learning_vectors",
    embedding=embedding_model
)
user_query = input("> ")

# Vector Similarity Search in DB for User Query
search_results = vector_db.similarity_search(
    query=user_query
)

# print("search_results : ", search_results)

# Format the similarity search result from vector DB it contains resuls metadata and content
context = "\n\n".join([f"Page Content: f{result.page_content} \n Page Number: {result.metadata['page_label']} \n File Location: {result.metadata['source']}" for result in search_results])

# PROMPT to be submitted to LLM to prepare answer for user-query 
SYSTEM_PROMPT = f"""
    You are an helpful AI assistant who answers user queries based on the available context retrived from a PDF file along with page_contents and page number

    You should only answer the user based on the following context and navigate the user to open the right page number to more
    Context:
    {context:}

"""

# print(SYSTEM_PROMPT)


chat_completion = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]
)

print(f"🤖 :: {chat_completion.choices[0].message.content}")