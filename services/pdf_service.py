import fitz  # PyMuPDF
import tempfile
import requests

def extract_text_from_pdf(url):
    try:
        with tempfile.NamedTemporaryFile(delete=True) as tmp_file:
            response = requests.get(url)
            tmp_file.write(response.content)
            tmp_file.flush()
            doc = fitz.open(tmp_file.name)
            text = "".join([page.get_text("text") + "\n" for page in doc])

        # Remove references if present
        lower_text = text.lower()
        if "references" in lower_text:
            text = text[:lower_text.rfind("references")]

        return text.strip()
    except Exception:
        return ""
