import requests
import json
from ast import literal_eval
import numpy as np
import csv

# Define the OpenAI API endpoint
OPENAI_API_URL = "https://api.openai.com/v1/engines/gpt-3.5-turbo/completions"

# Set your OpenAI API key
API_KEY = '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'

# Load the pre-generated embeddings
def load_embeddings(file_path):
    embeddings = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            embeddings.append((row[0], literal_eval(row[1])))
    return embeddings

# Function to generate response using ChatGPT
def generate_response(prompt, max_tokens=150, stop_sequence=None):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    data = {
        "prompt": prompt,
        "max_tokens": max_tokens
    }
    if stop_sequence:
        data["stop"] = stop_sequence
    response = requests.post(OPENAI_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()['choices'][0]['text'].strip()
    else:
        print(f"Error: {response.status_code}")
        print("Response content:", response.text)
        return ""

# Main function to generate response using embeddings
def generate_response_with_embeddings(prompt, embeddings, model="gpt-3.5-turbo", max_tokens=150, stop_sequence=None):
    # Create context based on the prompt
    context = create_context(prompt, embeddings)

    # Generate response using ChatGPT
    response = generate_response(prompt, model, max_tokens, stop_sequence)

    return response

# Function to create context based on the prompt
def create_context(prompt, embeddings):
    # Get embeddings for the prompt
    prompt_embedding = None
    for row in embeddings:
        if row[0] == prompt:
            prompt_embedding = row[1]
            break

    if prompt_embedding is None:
        return ""

    # Calculate distances between prompt embedding and embeddings in list
    distances = []
    for row in embeddings:
        context_embedding = row[1]
        distance = np.dot(prompt_embedding, context_embedding) / (np.linalg.norm(prompt_embedding) * np.linalg.norm(context_embedding))
        distances.append((row[0], distance))

    # Sort embeddings by distances and select top similar contexts
    sorted_embeddings = sorted(distances, key=lambda x: x[1], reverse=True)
    similar_contexts = [row[0] for row in sorted_embeddings[:5]]

    # Join similar contexts into one string
    context = "\n\n###\n\n".join(similar_contexts)

    return context

# Example usage
def main():
    # Load pre-generated embeddings
    #embeddings = load_embeddings('processed/embeddings.csv')

    # Prompt for the chat
    prompt = "Who are you"

    # Generate response using ChatGPT and embeddings
    response = generate_response(prompt)

    print("ChatGPT Response:", response)

if __name__ == "__main__":
    main()
