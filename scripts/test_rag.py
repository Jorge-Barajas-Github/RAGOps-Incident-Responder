from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

VECTORSTORE_PATH = Path("vectorstore/faiss_index")

def main():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    vectorstore = FAISS.load_local(
        str(VECTORSTORE_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )

    query = "critical network outage in a data center"
    results = vectorstore.similarity_search(query, k=5)

    print(f"\nQuery: {query}\n")

    for i, doc in enumerate(results, start=1):
        print("=" * 80)
        print(f"Result {i}")
        print(doc.page_content)
        print("Metadata:", doc.metadata)

if __name__ == "__main__":
    main()