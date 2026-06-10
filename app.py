import streamlit as st
from graph import graph
st.title("Multi-Agent Research System")

topic = st.text_input("Enter Topic")

uploaded_file = st.file_uploader(
    "Upload PDF",
    type="pdf"
)
pdf_path = None

if uploaded_file is not None:

    pdf_path = "temp.pdf"

    with open(pdf_path, "wb") as f:
        f.write(
            uploaded_file.getbuffer()
        )

if st.button("Research"):

    result = graph.invoke({
        "topic": topic,
        "pdf_path": pdf_path
    })

    with st.expander("Research Agent"):
        st.write(result.get("research", ""))

    with st.expander("Fact Checker"):
        st.write(
            result.get(
                "verified_research",
                "Skipped"
            )
        )

    with st.expander("Summary"):
        st.write(
            result.get(
                "summary",
                "Skipped"
            )
        )

    with st.expander("Final Report", expanded=True):
        st.write(result.get("report", ""))
    report = result["report"]

    if isinstance(report, list):
        report = report[0]["text"]

    st.markdown(report)

    st.download_button(
        "Download Report",
        report,
        file_name="report.txt",
        mime="text/plain"
    )