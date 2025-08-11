import streamlit as st
from services.search_service import search_papers_arxiv
from services.pdf_service import extract_text_from_pdf
from services.summarize_service import chunk_text, summarize_chunks
from services.citation_service import format_arxiv_citation

st.set_page_config(page_title="Research Paper Summarizer", layout="wide")
st.title("📄 Research Paper Summarizer")

# Session State
if "papers" not in st.session_state:
    st.session_state.papers = []
if "summaries" not in st.session_state:
    st.session_state.summaries = {}
if "citations" not in st.session_state:
    st.session_state.citations = {}

# Search UI
query = st.text_input("Enter keywords or a sentence to search for papers:")
search_clicked = st.button("Search")

if search_clicked and query.strip():
    with st.spinner("🔍 Searching arXiv papers..."):
        st.session_state.papers = search_papers_arxiv(query)

# Display papers
for paper in st.session_state.papers:
    st.subheader(paper['title'])
    st.write(f"**Authors:** {', '.join(paper['authors'])}")
    st.write(f"**Year:** {paper['year']}")
    st.write(paper['abstract'])
    st.markdown(f"🔗 **[View Full Paper on arXiv](https://arxiv.org/abs/{paper['arxiv_id']})**")

    # Summarize Button
    if st.button(f"Summarize: {paper['title']}", key=f"sum_{paper['arxiv_id']}"):
        if paper.get('pdf_link'):
            pdf_text = extract_text_from_pdf(paper['pdf_link'])
            if pdf_text.strip():
                chunks = chunk_text(pdf_text)
            else:
                chunks = chunk_text(paper['abstract'])
        else:
            chunks = chunk_text(paper['abstract'])

        summary = summarize_chunks(chunks)
        st.session_state.summaries[paper['arxiv_id']] = summary

    if paper['arxiv_id'] in st.session_state.summaries:
        st.markdown("### 📝 Summary")
        st.markdown(st.session_state.summaries[paper['arxiv_id']])

    # Citation Button
    if st.button(f"Cite: {paper['title']}", key=f"cite_{paper['arxiv_id']}"):
        citation_text = format_arxiv_citation(paper)
        st.session_state.citations[paper['arxiv_id']] = citation_text

    if paper['arxiv_id'] in st.session_state.citations:
        st.markdown("### 📌 Citation")
        st.text_area("Copy this citation:", st.session_state.citations[paper['arxiv_id']], height=80)
        st.download_button(
            "📥 Download Citation as .txt",
            st.session_state.citations[paper['arxiv_id']],
            file_name="citation.txt",
            key=f"download_{paper['arxiv_id']}"
        )

    st.markdown("---")
