from fastapi import FastAPI
from app.schemas import IncidentQuestionRequest, IncidentQuestionResponse
from app.rag import answer_incident_question

app = FastAPI(
    title="AI Ops Copilot",
    description="RAG-powered incident response assistant for IT/data center operations.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "AI Ops Copilot API is running",
        "try": "POST /ask with a JSON body containing a question",
    }


@app.post("/ask", response_model=IncidentQuestionResponse)
def ask_incident_question(request: IncidentQuestionRequest):
    result = answer_incident_question(request.question)
    return result