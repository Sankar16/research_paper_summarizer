import requests
import xml.etree.ElementTree as ET

def search_papers_arxiv(query):
    base_url = "http://export.arxiv.org/api/query?search_query=all:"
    url = f"{base_url}{query}&max_results=10"
    resp = requests.get(url)
    root = ET.fromstring(resp.content)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    papers = []
    for entry in root.findall('atom:entry', ns):
        title = entry.find('atom:title', ns).text.strip()
        authors = [a.find('atom:name', ns).text.strip() for a in entry.findall('atom:author', ns)]
        summary = entry.find('atom:summary', ns).text.strip()
        published = entry.find('atom:published', ns).text[:10]
        arxiv_id = entry.find('atom:id', ns).text.split('/abs/')[-1]

        pdf_link = None
        for link in entry.findall('atom:link', ns):
            if link.attrib.get('title') == 'pdf':
                pdf_link = link.attrib['href']

        papers.append({
            'title': title,
            'authors': authors,
            'year': published,
            'abstract': summary,
            'arxiv_id': arxiv_id,
            'pdf_link': pdf_link
        })
    return papers
