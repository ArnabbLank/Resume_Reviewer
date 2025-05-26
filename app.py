import streamlit as st
from main import review_resume
import tempfile
import json

def format_nested_markdown(data, indent=0):
    """
    Format a nested dictionary into Markdown with indentation.
    """
    markdown = ""
    prefix = "    " * indent
    for key, value in data.items():
        if isinstance(value, dict):
            markdown += f"{prefix}- **{key}**:\n"
            markdown += format_nested_markdown(value, indent + 1)
        else:
            val = value.strip() if isinstance(value, str) else str(value)
            markdown += f"{prefix}- **{key}**: {val}\n"
    return markdown


def render_json_collapsible_flat(data):
    """
    Render top-level keys as Streamlit expanders and show nested content as indented Markdown.
    """
    for key, value in data.items():
        with st.expander(f"📌 {key}", expanded=False):
            if isinstance(value, dict):
                md = format_nested_markdown(value)
                st.markdown(md)
            else:
                st.markdown(f"**{key}:** {value}")


st.set_page_config(page_title="Resume Reviewer", layout="wide")

st.title("📄 AI Resume Reviewer")
st.write("Upload your PDF resume and get section-by-section improvement suggestions.")

uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    with st.spinner("Analyzing your resume..."):
        result = review_resume(tmp_path)

    if "error" in result:
        st.error(result["error"])
        st.code(result["raw_output"])
    else:
        st.success("✅ Resume analysis complete!")
        render_json_collapsible_flat(result)


