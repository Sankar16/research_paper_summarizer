def format_arxiv_citation(paper):
    authors_str = ", ".join(paper['authors'])
    return f"{authors_str} ({paper['year']}). {paper['title']}. arXiv preprint arXiv:{paper['arxiv_id']}. https://arxiv.org/abs/{paper['arxiv_id']}"
