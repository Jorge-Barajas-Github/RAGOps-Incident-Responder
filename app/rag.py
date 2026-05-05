from pathlib import Path
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

VECTORSTORE_PATH = Path("vectorstore/faiss_index")


def load_vectorstore():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

    return FAISS.load_local(
        str(VECTORSTORE_PATH),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def format_sources(docs):
    sources = []

    for doc in docs:
        meta = doc.metadata
        sources.append(
            {
                "incident_id": meta.get("incident_id"),
                "incident_type": meta.get("incident_type"),
                "priority": meta.get("priority"),
                "department": meta.get("department"),
                "location": meta.get("location"),
                "resolution_type": meta.get("resolution_type"),
                "resolution_time_hours": meta.get("resolution_time_hours"),
                "status": meta.get("status"),
            }
        )

    return sources


def answer_incident_question(question: str):
    vectorstore = load_vectorstore()

    docs = vectorstore.similarity_search(question, k=5)

    context = "\n\n---\n\n".join([doc.page_content for doc in docs])

    prompt = f"""
You are an AI Ops Copilot for enterprise incident response.

Use the retrieved incident records below to help answer the user's question.
Do not claim certainty beyond the data.
If the data is limited, say what is missing.

Retrieved incident records:
{context}

User question:
{question}

Respond in this structure:

Likely Pattern:
- Summarize what similar incidents suggest.

Recommended Actions:
- Give practical next steps.

Relevant Past Incidents:
- Mention the most relevant incident IDs and what happened.

Limitations:
- Mention any limitation in the available data.
"""

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": format_sources(docs),
    }