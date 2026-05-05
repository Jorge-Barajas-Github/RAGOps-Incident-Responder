import json
from pathlib import Path
from dotenv import load_dotenv

from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

PROCESSED_PATH = Path("data/processed/incidents.jsonl")
VECTORSTORE_PATH = Path("vectorstore/faiss_index")

def load_documents():
    docs = []

    with PROCESSED_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)

            docs.append(
                Document(
                    page_content=item["text"],
                    metadata=item["metadata"]
                )
            )

    return docs

def main():
    docs = load_documents()
    print(f"Loaded {len(docs)} documents")

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local(str(VECTORSTORE_PATH))

    print(f"Saved vectorstore to {VECTORSTORE_PATH}")

if __name__ == "__main__":
    main()