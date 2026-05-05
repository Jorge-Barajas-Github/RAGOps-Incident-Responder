import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))


from app.rag import answer_incident_question


def main():
    question = "We have a critical network outage at Data Center A. What should the operations team check first?"

    result = answer_incident_question(question)

    print("\nQUESTION:")
    print(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES:")
    for source in result["sources"]:
        print(source)


if __name__ == "__main__":
    main()