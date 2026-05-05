import requests
import streamlit as st

st.set_page_config(page_title="AI Ops Copilot", page_icon="🛠️", layout="wide")

st.title("AI Ops Copilot")
st.caption("RAG-powered incident response assistant for IT and data center operations.")

question = st.text_area(
    "Describe the incident",
    value="We have a critical network outage at Data Center A. What should the team check first?",
    height=120,
)

if st.button("Analyze Incident"):
    if not question.strip():
        st.warning("Please enter an incident description.")
    else:
        with st.spinner("Retrieving similar incidents and generating response..."):
            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": question},
                timeout=60,
            )

        if response.status_code == 200:
            data = response.json()

            st.subheader("AI Recommendation")
            st.markdown(data["answer"])

            st.subheader("Retrieved Incident Sources")
            st.dataframe(data["sources"])
        else:
            st.error(f"API error: {response.status_code}")
            st.text(response.text)