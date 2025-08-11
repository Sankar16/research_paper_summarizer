# 📄 Research Paper Summarizer (arXiv Edition)

A **Streamlit** web app that searches **arXiv** for research papers, downloads and extracts full-text PDFs, chunks them to avoid token limits, and generates **clear, section‑wise bullet-point summaries** using an **OpenAI‑compatible model hosted on Hugging Face**.  
It also generates **formatted citations** with copy/download options.

---

## ✨ Features

- 🔍 Search open-access research papers from **arXiv** API  
- 📄 Download and parse full paper text from PDF (when available)  
- ✂️ Split long text into manageable **chunks** to stay within model token limits  
- 📝 Summarize each chunk & merge into a **deduplicated structured summary**  
- 📌 **3–4 bullet points per section** (Introduction, Data, Methods, Results, Conclusion)  
- 📑 Generate formatted citations with copy & download buttons  
- 🔗 Direct link to the paper on arXiv  
- 💾 Summaries & citations persist until cleared

---

## 📂 Project Structure

research_paper_summarizer/
│
├── app.py # Main Streamlit app entry point
├── requirements.txt # Python dependencies
├── .streamlit/
│ └── secrets.toml # Private Hugging Face API key
│
├── services/
│ ├── search_service.py # arXiv API search
│ ├── pdf_service.py # PDF download and text extraction
│ ├── summarize_service.py # Text chunking & summarization logic
│ └── citation_service.py # Format citations

text

---

## ⚙️ Installation

### 1️⃣ Clone the repository
git clone https://github.com/Sankar16/research_paper_summarizer.git
cd research_paper_summarizer
text

### 2️⃣ Create and activate virtual environment
python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
text

### 3️⃣ Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
text

---

## 🔑 API Key Setup

We are using the **OpenAI‑compatible API on Hugging Face**.

1. Sign up at [Hugging Face](https://huggingface.co/) and generate an Access Token.  
2. Create `.streamlit/secrets.toml` in your project and add:
HF_TOKEN = "hf_your_secret_access_token_here"
text
3. This token will be loaded automatically in the app with:
from openai import OpenAI
import streamlit as st
client = OpenAI(
base_url="https://router.huggingface.co/v1",
api_key=st.secrets["HF_TOKEN"]
)
text

---

## 🚀 Running the App

Run inside your activated virtual environment:

streamlit run app.py
text

The app will be available at:

- Local: `http://localhost:8501` (port may vary)  
- Network: accessible on your LAN if needed

---

## 🛠 Usage Steps

1. Enter keywords or a sentence related to your research interest.
2. Click **Search** to fetch relevant arXiv papers.
3. For each paper:
   - **Summarize** → Generates a clean, bullet‑point summary.
   - **Cite** → Displays a formatted citation with copy & download options.
4. Citation and summary persist until removed or the session ends.

---

## ⚠️ Notes

- If no PDF link is available, the app will summarize the **abstract** instead.
- Hugging Face free tier inference calls are capped; you may see:
Error code: 402 - You have exceeded your monthly included credits
text
In that case, wait for quota reset or upgrade your plan.
- Large PDFs are split into chunks before summarization to avoid hitting token or length limits.

---

## 📋 Example Output

**Summary**
Introduction

Genome-wide DNA methylation profiles can assist cancer detection
Deep learning enables classification without manual biomarker selection
CNN can process methylation data as image-like matrices
Methods

DNA methylation β-values reshaped into 2D arrays
Mini-batch SGD with Adam optimizer
Early stopping with validation loss criteria
text

**Citation**
Author A., Author B. (2023). Paper Title. arXiv preprint arXiv:1234.56789. https://arxiv.org/abs/1234.56789
text

---

## 📜 License
MIT License — free to use, modify, and distribute.