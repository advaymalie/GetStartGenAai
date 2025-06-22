# RAG Engineering: From 50MB PDF to Queryable Knowledge Base

We know RAG(Retrieval-Augmented Generation) is the "open-book exam" for LLMs. But what does it take to create that "book" and help the LLM find the right page? Let's break down the engineering challenges of turning a massive, 50MB PDF document into a queryable knowledge base.
```
+--------------------------------------------------------------------------------------------------+
|                                                                                                  |
|   Phase 1: Indexing (Offline Process)                                                            |
|   +-----------------+      +-----------------+      +--------------------+      +--------------+ |
|   |  50MB PDF Doc   |----->|   Chunker       |----->|  Embedding Model   |----->| Vector DB    | |
|   | (Source Data)   |      | (Splits into    |      | (Creates vectors   |      | (Stores Text | |
|   +-----------------+      |   paragraphs)   |      |  from each chunk)  |      |  & Vectors)  | |
|                            +-----------------+      +--------------------+      +--------------+ |
|                                                                                                  |
+--------------------------------------------------------------------------------------------------+
                ^
                | Populates
+-----------------------------------------------------------------------------------------------------+
|                                                                                                     |
|   Phase 2: Retrieval & Generation (Real-time Process)                                               |
|                                                                                                     |
|   [User Query] -> [Embedding Model] -> [Search Vector DB] -> [Relevant Chunks] -> [LLM] -> [Answer] |
|                                       (Finds similar vectors) |                                     |
|                                                               |                                     |
|                                                               +-> [Augmented Prompt] ---------------+
|                                                                   (Context + Query)                 |
|                                                                                                     |
+-----------------------------------------------------------------------------------------------------+

```

## 1. Ingestion & Indexing: Preparing the Knowledge Base

This is the entire offline process of teaching our system about the 50MB PDF.

**Why?** We can't just feed a 50MB PDF to an LLM. It would be like asking someone to read a 10,000-page book in one second and then answer a specific question about page 7,432. The primary technical barrier is the problem with token size; LLMs have a fixed context window (e.g., 8k, 128k tokens), which is the maximum amount of text they can "see" at once. Our huge PDF far exceeds this limit.

**What?** Ingestion and Indexing is the data engineering pipeline where we process the large document, break it down, and store it in a way that's optimized for fast and relevant information retrieval.

**How?** This process involves two critical sub-steps: Chunking and Vectorization.

## 2. Chunking / Splitting: The Art of Breaking Down Text

**Why?** To solve the token size problem. By breaking the massive document into small, logical pieces (chunks), we create a library of bite-sized facts. We can then find the most relevant fact-chunks to answer a question, instead of trying to stuff the whole book into the LLM's memory.

**What?** Chunking is the strategy of splitting a large document into smaller, semantically coherent segments of text.

**How?** There are several methods for chunking/splitting, each with its own trade-offs:

- **By Paragraph:** This is often the best starting point, as paragraphs naturally group related ideas.
- **Fixed-Size Chunks:** You can split the text every 500 characters, for example. This is simple but can awkwardly cut sentences in half.
- **Recursive Splitting:** A smarter method that tries to split by paragraph first, then by sentence if a paragraph is too long, preserving the semantic meaning.

**Crucial Step — Storing Metadata:** As we create each chunk, we must store its original location as metadata. For our 50MB PDF, each chunk would be stored not just with its text, but also with its page number and source filename (e.g., {'text': '...', 'source': 'annual_report.pdf', 'page': 247}).

## 3. Vectorization: Turning Meaning into Math

**Why?** Computers don't understand "meaning"; they understand numbers. To find chunks that are "semantically similar" to a user's question, we need to represent both the chunks and the question in a mathematical format.

**What?** Vectorization is the process of using an embedding model to convert each text chunk into a vector (a long list of numbers). This vector represents the chunk's position in a high-dimensional "meaning space."

**How?** We iterate through every text chunk created in the previous step and send it to an embedding model (like text-embedding-ada-002). The model returns a vector for each chunk. We then store these vectors, along with their original text and metadata (page_number, etc.), in a specialized vector database. Now, our 50MB PDF is no longer a single block of text; it's a searchable database of thousands of semantically indexed knowledge snippets.

## 4. Retrieval and Generation: Answering the User's Query

This is the real-time process that happens when a user asks a question.

**Why?** To provide the LLM with only the most relevant, targeted information from our massive document, enabling a fast and accurate answer.

**What?** The retrieval pipeline is a series of steps that finds the right context and uses it to generate a final, cited answer.

**How?** It follows a precise sequence:

1. **User Query:** A user asks, "What were the key risks identified in the 2023 annual report?"

2. **Vectorize Query:** The user's question is converted into a vector using the same embedding model we used for indexing.

3. **Retrieval of Relevant Chunks:** The system queries the vector database: "Find me the top 3 chunks whose vectors are closest to this query vector." The database returns the most relevant chunks, including their text and metadata.

4. **LLM Call with Context:** The system constructs a detailed prompt for the LLM. This is where the magic happens

**Prompt Sent to LLM:**
```
"You are a helpful assistant. Based on the following context, which includes the source and page number for each piece of information, answer the user's question. After your answer, you MUST cite the page number for the information you used.

Context: 
Source: annual_report.pdf, Page: 8 
[Text of the first retrieved chunk...]

Source: annual_report.pdf, Page: 9 
[Text of the second retrieved chunk...]

User's Question: What were the key risks identified in the 2023 annual report?"
```

## 5. Result with Page Number

The LLM, now armed with the exact context and instructions to cite its sources, generates the answer. Because the page_number was included in the context, it can accurately report where it found the information.

**Final AI Answer:** "The key risks identified were market volatility and supply chain disruptions. (Source: annual_report.pdf, Page: 8-9)"

This end-to-end process, from ingestion to the final result with page number, is the complete architecture of a robust and trustworthy RAG system.