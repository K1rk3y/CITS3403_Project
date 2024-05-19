import sqlite3
import pandas as pd
import numpy as np
from ast import literal_eval
import pandas as pd
from scipy.spatial.distance import cosine
import tiktoken
from openai import OpenAI

# Load OpenAI client
client = OpenAI(api_key='sk-')

# Function to remove newlines from a Series
def remove_newlines(serie):
    serie = serie.str.replace('\n', ' ')
    serie = serie.str.replace('\\n', ' ')
    serie = serie.str.replace('  ', ' ')
    serie = serie.str.replace('  ', ' ')
    return serie


# Function to split the text into chunks of a maximum number of tokens
def split_into_many(tokenizer, text, max_tokens):
    sentences = text.split('. ')
    n_tokens = [len(tokenizer.encode(" " + sentence)) for sentence in sentences]
    chunks = []
    tokens_so_far = 0
    chunk = []
    for sentence, token in zip(sentences, n_tokens):
        if tokens_so_far + token > max_tokens:
            chunks.append(". ".join(chunk) + ".")
            chunk = []
            tokens_so_far = 0
        if token > max_tokens:
            continue
        chunk.append(sentence)
        tokens_so_far += token + 1
    if chunk:
        chunks.append(". ".join(chunk) + ".")
    return chunks


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return client.embeddings.create(input = [text], model=model).data[0].embedding


# Define functions for answering questions
def create_context(question, df, max_len=1800, size="ada"):
    q_embeddings = get_embedding(question)
    df["distances"] = df["embeddings"].apply(lambda x: cosine(q_embeddings, x))
    returns = []
    cur_len = 0
    for i, row in df.sort_values('distances', ascending=True).iterrows():
        cur_len += row['n_tokens'] + 4
        if cur_len > max_len:
            break
        returns.append(row["text"])
    return "\n\n###\n\n".join(returns)


def answer_question(df, model="gpt-3.5-turbo", question="Who are you", condition_prompt='', max_len=1800, size="ada", debug=False, max_tokens=300, stop_sequence=None):
    context = create_context(question, df, max_len=max_len, size=size)
    if debug:
        print("Context:\n" + context)
        print("\n\n")
    try:
        prompt=f"Answer the question based on the context below, and if the question can't be answered based on the context, say \"I don't have that infomation at this moment.\"\n\nContext: {context}\n\n---\n\nQuestion: {question}\n" + condition_prompt + "\nAnswer:"
        response = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=stop_sequence,
            model=model
        )

        return response.choices[0].message.content
    
    except Exception as e:
        print(e)
        return ""


def Wrapper(condition_prompt, question):
    # Load tokenizer
    tokenizer = tiktoken.get_encoding("cl100k_base")

    # Connect to the database
    conn = sqlite3.connect('instance/site.db')

    # Read data from the "Order" table into a DataFrame
    df = pd.read_sql_query("SELECT * FROM 'Order'", conn)

    # Check if any text column exists in the DataFrame
    text_columns = [col for col in df.columns if df[col].dtype == 'object']
    if len(text_columns) == 0:
        print("No text column found in the 'Order' table. Exiting.")
        exit()

    # Concatenate all text columns into a single 'text' column
    df['text'] = df[text_columns].apply(lambda row: ' '.join(row.dropna()), axis=1)

    # Tokenize the text and save the number of tokens to a new column
    df['n_tokens'] = df['text'].apply(lambda x: len(tokenizer.encode(x)))

    # Visualize the distribution of the number of tokens per row using a histogram
    df['n_tokens'].hist()

    # Set max_tokens
    max_tokens = 500

    # Shorten the text
    shortened = []
    for _, row in df.iterrows():
        if row['n_tokens'] > max_tokens:
            shortened += split_into_many(tokenizer, row['text'], max_tokens)
        else:
            shortened.append(row['text'])

    # Create DataFrame from shortened texts
    df = pd.DataFrame(shortened, columns=['text'])
    df['n_tokens'] = df['text'].apply(lambda x: len(tokenizer.encode(x)))
    df['n_tokens'].hist()

    df['embeddings'] = df['text'].apply(get_embedding)

    # Save embeddings to CSV
    df.to_csv('processed/embeddings_Order.csv')

    # Read embeddings from CSV
    df = pd.read_csv('processed/embeddings_Order.csv', index_col=0)
    df['embeddings'] = df['embeddings'].apply(literal_eval).apply(np.array)

    return answer_question(df, question=question, condition_prompt=condition_prompt, debug=False)