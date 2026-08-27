import sys
from pypdf import PdfReader
from pathlib import Path
import ollama
import chromadb

def pdf_to_page():
    # check input
    if len(sys.argv) != 2:
            sys.exit("valid syntax = python main.py [filename]")
    if not sys.argv[1].endswith(".pdf"):
            sys.exit("file is not a pdf")
    if not Path(sys.argv[1]).exists():
            sys.exit(f"{sys.argv[1]} does not exist")
    # read file
    reader = PdfReader(sys.argv[1])
    extracted_page = []
    for page in reader.pages:
        text = (page.extract_text())
        extracted_page.append(text)
    return extracted_page

def page_to_embedding(extracted_page):
    # convert to numbers
    page_embedding = []
    for page in extracted_page:
        response = ollama.embeddings(model="nomic-embed-text", prompt=page)
        page_embedding.append(response['embedding'])
    return page_embedding

def add_database(extracted_page, page_embedding):
    # add to chromadb database
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("pdf_gpt")

    for i, page in enumerate(extracted_page):
        n_of_page = i + 1
        collection.add(
            documents=[page],
            ids=[f"{sys.argv[1]}_page_{n_of_page}"],
            metadatas=[{"source": sys.argv[1], "page": n_of_page}],
            embeddings=[page_embedding[i]]
            )
def process_question():
    # process user question
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_or_create_collection("pdf_gpt")

    question = input(f"\n What would you like to ask about {sys.argv[1]}? ")
    question_embedding = ollama.embeddings(model="nomic-embed-text", prompt=question)["embedding"]
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )
    retrieved_text = results['documents'][0]
    if not retrieved_text:
        print("No relevant information found in the PDF.")
        return
    total_text = " ".join(retrieved_text)
    prompt = f"Answer the following question based on the provided text. If the text does not contain the answer, respond with 'I don't know'.\n\nText: {total_text}\n\nQuestion: {question}\n\nAnswer:"
    response = ollama.generate(model="gemma3:1b", prompt=prompt)
    return response["response"]