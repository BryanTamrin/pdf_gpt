import sys
from pypdf import PdfReader
from pathlib import Path
import ollama
import chromadb

def main():
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

    # convert to numbers
    page_embedding = []
    for page in extracted_page:
        response = ollama.embeddings(model="nomic-embed-text", input=page)
        page_embedding.append(response['embedding'])

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
if __name__ == "__main__":
    main()