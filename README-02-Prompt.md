# The Art of Writing Prompts: A Simple Guide

Think of a Large Language Model (LLM) like a very powerful car engine. The prompt is the instruction you give the driver. A vague instruction like "Go north" will lead to a confusing journey. A clear instruction like "Go to Delhi via the Yamuna Expressway" gets you there perfectly. For a tech guy like you, it's the difference between a half-baked requirement and a clear user story.

## Why Are Good Prompts So Important?

**Why?** The quality of the result depends directly on the quality of your prompt. A clear prompt removes confusion and gives you the exact answer you want, much faster.

**What?** A prompt is not just a question. It's a full set of instructions, including some background info, rules, examples, and what kind of answer you want.

**How?** By being specific and giving proper context. A bad prompt is, "Tell me about Japan." A good prompt is:
> "Make a 7-day plan for a first-time solo trip to Japan in October. Focus on culture in Tokyo and Kyoto, and using trains. Give a budget estimate in Rupees."

## Types of Prompts: Your Traveller's Guide

Here are some simple but powerful ways to write prompts, using examples a world traveller like you will find familiar.

### 1. Zero-Shot vs. Few-Shot Prompting

This is about how much you teach the model before asking your question.

**Zero-Shot (Direct Question):** You just ask the model something directly, without giving any examples. It uses its own general knowledge to answer.
> **Example:**
> "Which currency is used in Switzerland?"

**One-Shot / Few-Shot (Show an Example):** You first show the model one or more examples of what you want. This is a great trick to get the answer in the right tone and format.
> **Example:**
> "Here is how to show currency details:
> India -> Rupee (INR)
>
> Now, do the same for South Africa."
>
> **Expected Answer:**
> South Africa -> Rand (ZAR)

### 2. The System Prompt & Personas

A system prompt is like setting the ground rules for the whole chat. A big part of this is giving the AI a persona, which tells it who it should act like.

**Why?** To control the AI's behaviour, making sure it sticks to the topic and talks in a consistent style.

**What?** It's a background instruction that controls the AI's personality, knowledge area, and what it should not do.

**How?** By telling the AI its role right at the start of the chat.

**Persona Example based on myself:**

System Prompt:
"You are 'Globetrotter AI,' an expert travel guide for senior tech guys. Your user is a Staff Engineer from India who has worked in America, Switzerland, and South Africa. He understands complex things and prefers efficient plans and deep cultural experiences, not just the usual tourist spots. Give practical, well-planned advice. When you suggest something, talk about it like a system (e.g., 'the Japanese rail system,' not just 'a train'). No generic tourist gyaan. Assume he will understand technical details. Here are some examples of how you should respond:

Q: 'What are some must-see places in Kyoto?'
A: 'Instead of a simple list, let's structure your Kyoto exploration. The city is best tackled by geographic clusters to optimize travel time. 1. Eastern Kyoto (1-2 days): Focus on the Higashiyama District. Key nodes are Kiyomizu-dera, Sannenzaka, and Gion. This forms a single, walkable system. 2. Northern Kyoto (1 day): Kinkaku-ji (Golden Pavilion) and Ryoan-ji (Zen Garden). Avoid trying to cross the city multiple times a day; it's inefficient.'

Q: 'Is it easy to get vegetarian food in Tokyo?'
A: 'Yes, the system for finding vegetarian food is robust if you know the right keywords and apps. Use 'Shojin Ryori' for Buddhist vegetarian cuisine. For casual dining, use 'Saishoku-shugisha'. The 'HappyCow' app is the most reliable database.'

Q: 'I'm landing in Mumbai for a 2-day work trip. What's the best way to travel between the airport, my hotel in BKC, and meetings in South Mumbai?'
A: 'Let's break down Mumbai's transport system into its components. For your route, you have three main options with different trade-offs: 1. Ride-Sharing (Uber/Ola): This offers the highest comfort and is best for your airport luggage. However, it's the least efficient system during peak traffic. 2. Auto-rickshaws: This system is optimal for short-distance, cost-effective travel within BKC. It is not suitable for the long BKC to South Mumbai route. 3. Local Trains: This is the most efficient system for covering long distances and bypassing traffic (e.g., Bandra to Churchgate). It offers predictable travel time but comes with crowding.'"


With this persona, if you ask "How to travel in Japan?", you will get a proper plan about the Japan Rail Pass, Suica cards, and using the HyperDia app, not just a simple list of trains.


### 3. Chain of Thought (CoT) Prompting

For difficult questions, you can make the model explain its thinking process. This makes the final answer much more accurate.

**Why?** It breaks a big problem into smaller, logical steps. This reduces mistakes. As an engineer, you know it's easier to check work when you can see all the steps.

**What?** It's a trick where you tell the model to "think step by step" before giving the final answer.

**How?** Just add a simple line like "Let's think step by step" to your prompt.

> **Example:**
> User: "I'm in Zurich and want to take a day trip to a town in the Jungfrau area. I have to leave after 8 AM and be back by 10 PM. I want to spend maximum time in the mountains. Which is the best town to visit and what's the train plan? Let's think step by step."

**Expected Step-by-Step Answer:**

1.  **Goal:** User wants a day trip from Zurich to Jungfrau with time limits (8 AM-10 PM) to get the most mountain time.
2.  **Options:** The main towns are Grindelwald, Wengen, and Mürren. The journey first goes to Interlaken Ost station.
3.  **Travel Time:**
    *   Zurich to Interlaken is about 2 hours.
    *   Interlaken to Grindelwald is about 30 mins.
    *   Total travel one way is about 2.5 to 3 hours.
4.  **Make Plan:** Leaving Zurich at 8 AM means you reach the area by 11 AM. To get back to Zurich by 10 PM, you must leave the town by 7 PM. This gives you about 8 hours there.
5.  **Final Suggestion:** Grindelwald is the best option for a day trip. It's easy to reach and has great views of the Eiger mountain.
    *   **Going:** Take the 8:02 AM train from Zurich, you'll reach Grindelwald by 11:11 AM.
    *   **Returning:** Take the 6:49 PM train from Grindelwald, you'll be back in Zurich by 9:58 PM.
