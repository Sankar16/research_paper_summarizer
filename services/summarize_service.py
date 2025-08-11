import tiktoken
import streamlit as st
import os
from openai import OpenAI

client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],  # make sure HF_TOKEN is set in env or secrets
)
def chunk_text(text, max_tokens=1500):
    enc = tiktoken.get_encoding("cl100k_base")
    words = text.split()
    chunks, current_chunk, current_len = [], [], 0

    for word in words:
        token_len = len(enc.encode(word))
        if current_len + token_len > max_tokens:
            chunks.append(" ".join(current_chunk))
            current_chunk, current_len = [word], token_len
        else:
            current_chunk.append(word)
            current_len += token_len
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    return chunks

def summarize_chunks(chunks):
    partial_summaries = []

    # First pass: summarize each chunk
    for i, chunk in enumerate(chunks):
        prompt = (
            "Summarize this text in plain English as short, clear bullet points covering all the key informations. "
            "Do not duplicate information from other chunks. Ignore references.\n\n"
            f"{chunk}"
        )
        with st.spinner(f"🔍 Summarizing part {i+1} of {len(chunks)}..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
        content = None
        try:
            content = response.choices[0].message.content
        except (AttributeError, IndexError):
            content = ""

        if content is None:
            content = ""

        partial_summaries.append(content)

    # Merge partial summaries
    merged_text = "\n".join(partial_summaries)

    # Second pass: create one clean, structured summary
    final_prompt = (
        "You are an expert summarizer. Merge the following partial summaries into ONE cohesive paper summary. "
        "Organize it into the sections Introduction, Data, Methods, Results, and Conclusion. "
        "Under each section, produce concise bullet points capturing the key facts clearly. "
        "Avoid redundancy and references.\n\n"
        f"{merged_text}"
    )

    with st.spinner("🛠 Compiling final summary..."):
        final_response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": final_prompt}],
            max_tokens=700  # Enough for final clean summary
        )

    final_content = final_response.choices[0].message.content if final_response else ""
    return final_content

'''
def summarize_chunks(chunks):
    summaries = []
    for i, chunk in enumerate(chunks):
        prompt = (
            "Summarize the following text in plain English with 3-4 bullet points for each section (e.g., Introduction, Data, Methods, Results). "
            "Ensure that each bullet point captures the key details of the section, without being overly detailed, but still providing a thorough summary. "
            "Do not include the References section. Focus on summarizing the main ideas, methodology, data, results, and conclusions for each section.\n\n"
            f"{chunk}"
        )
        with st.spinner(f"🔍 Summarizing part {i+1} of {len(chunks)}..."):
            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
        summaries.append(response.choices[0].message.content)
    return "\n\n".join(summaries)
'''