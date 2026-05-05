import pandas as pd
import json
from pathlib import Path

RAW_PATH = Path("data/raw/incident_reports.csv")
OUT_PATH = Path("data/processed/incidents.jsonl")

def row_to_document(row):
    return {
        "id": str(row["Incident_ID"]),
        "text": f"""
Incident ID: {row["Incident_ID"]}
Incident Type: {row["Incident_Type"]}
Priority: {row["Priority"]}
Assigned Department: {row["Assigned_Department"]}
Location: {row["Location"]}
Reported Time: {row["Reported_Time"]}
Resolved Time: {row["Resolved_Time"]}
Resolution Time Hours: {row["Resolution_Time_Hours"]}
Status: {row["Status"]}
Resolution Type: {row["Resolution_Type"]}

This incident involved a {row["Priority"]} priority {row["Incident_Type"]} at {row["Location"]}.
It was handled by {row["Assigned_Department"]} and resolved using {row["Resolution_Type"]}.
""".strip(),
        "metadata": {
            "incident_id": str(row["Incident_ID"]),
            "incident_type": row["Incident_Type"],
            "priority": row["Priority"],
            "department": row["Assigned_Department"],
            "location": row["Location"],
            "resolution_type": row["Resolution_Type"],
            "resolution_time_hours": float(row["Resolution_Time_Hours"]),
            "status": row["Status"],
        }
    }

def main():
    df = pd.read_csv(RAW_PATH)

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUT_PATH.open("w", encoding="utf-8") as f:
        for _, row in df.iterrows():
            doc = row_to_document(row)
            f.write(json.dumps(doc) + "\n")

    print(f"Prepared {len(df)} documents")
    print(f"Saved to {OUT_PATH}")

if __name__ == "__main__":
    main()