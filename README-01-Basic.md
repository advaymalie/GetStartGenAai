# A Guide to Generative AI

This repository contains notes and code examples covering the foundational concepts of Generative AI. This guide breaks down the core components of the technology.

---

## The Evolution of AI

AI isn't new, but its capabilities have fundamentally shifted. Here’s a look at the transition from analyzing what exists to generating what's new.

### Before: Analytical AI

* **What?** Systems designed to analyze existing data to find patterns, classify information, and perform specific, predictable tasks.
* **Why?** To understand and interpret the world as it is, automating analytical or repetitive human processes.
* **How?** By training models on labeled datasets to recognize specific features, like identifying spam in emails or detecting fraud.

### After: Generative AI

* **What?** Systems that can create new, original content—like text, images, or code—that is similar to the data they were trained on.
* **Why?** To amplify human creativity and productivity by generating novel ideas and content from a simple prompt.
* **How?** By learning the underlying patterns and structures of data so deeply that they can produce new combinations and variations.

---

## Core Concepts: The Engine of GenAI

How does a machine go from predicting to creating? It starts with these key ideas.

### 1. The Transformer Architecture

The Transformer is a revolutionary neural network architecture that processes text by looking at an entire sequence at once, rather than word-by-word. This overcomes the short-term memory limitations of older models.

* **The Old Way (RNNs):** Imagine a single-threaded process reading a file line by line. By the end of a long document, it has a very fuzzy memory of the beginning.
* **The Transformer Way:** This is like a modern, multi-threaded system. It uses a mechanism called **Self-Attention** to build a relationship map for the entire sentence simultaneously. For every word, it calculates a "relevance score" against every other word, understanding the deep context.

> **Example:** In the sentence, `"The data pipeline, which runs on Azure, failed because the upstream service was down."`, the Attention mechanism allows the model to instantly understand that "failed" is most related to "pipeline" and "service", even though they are far apart.

At its core, all of Generative AI's amazing capabilities emerge from a simple training objective: **the prediction of the next word.** To get good at this, the model must learn grammar, facts, reasoning, and style. "Generation" is simply the model performing this task repeatedly to create new content.

### 2. Tokenization

Tokenization is the process of breaking text into smaller chunks called "tokens," which the model can understand as numbers.

* **Why?** LLMs don't understand words; they understand numbers. Tokenization is the essential first step to translate human language into a numerical format.
* **What?** A token can be a word, a part of a word (e.g., `Gener` + `ative`), or a single character. Each model (GPT, Gemini, etc.) has its own unique tokenizer and vocabulary, which is why the same text can have different token counts on different models.
* **How to Manage Tokens & Costs:**
    * **Be Concise:** Rephrase prompts to be shorter. For example, use "Python file I/O example" instead of "Can you please write me a piece of Python code that can be used to demonstrate how to open a file?".
    * **Clean Your Data:** Remove unnecessary characters, HTML tags, or extra whitespace.
    * **Summarize History:** In chatbots, summarize the past conversation instead of sending the full history each time.
    * **Client-Side Counting:** Use libraries like `tiktoken` to estimate costs *before* making an API call.

### 3. Vector Embeddings

A vector embedding is a list of numbers (a vector) that represents a piece of text in a multi-dimensional "semantic space," capturing its meaning and context.

* **Why?** Simple token IDs (e.g., `Lamborghini`=5, `Pagani`=8) have no inherent relationship. Embeddings capture the meaning, allowing the model to understand that these are both supercars.
* **What?** Words with similar meanings are located close to each other on a giant, complex map. For example, the vector for "Lamborghini" would be very close to the vector for "Pagani", while the vector for "Italy" would be in a different neighborhood.
* **How?** Specialized models (like `text-embedding-ada-002`) generate these vectors. The relationships between them are mathematically meaningful, which enables the classic example:
    ```
    vector("King") - vector("Man") + vector("Woman") ≈ vector("Queen")
    ```
    This "vector math" is fundamental to how AI can reason, perform semantic searches (like in RAG), and understand analogies.

---

## Reference Links

* **Tokenizer Visualizer:** <https://tiktokenizer.vercel.app/>
* **Vector Embedding Visualizer:** <https://projector.tensorflow.org/>
* **The "Attention Is All You Need" Paper:** <https://research.google/pubs/attention-is-all-you-need/>
* **V0 System Prompt Examples:** [Link to GitHub](https://github.com/2-fly-4-ai/V0-system-prompt/blob/main/v0-system-prompt(updated%2022-11-2024\))
* **Cursor prompts for reference:** [CURSOR PROMPTS](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools/tree/main/Cursor%20Prompts)
* **RAG:** [RAG](https://aws.amazon.com/what-is/retrieval-augmented-generation/)
