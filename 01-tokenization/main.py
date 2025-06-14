import tiktoken

enc = tiktoken.encoding_for_model("gpt-4o")
# https://tiktokenizer.vercel.app/?model=gpt-4o

text = "Hello, India is great country"
tokens = enc.encode(text)

print("Tokens:", tokens)

tokens = [13225, 11, 8405, 382, 2212, 4931]
decoded = enc.decode(tokens)

print("Decoded Text:", decoded)