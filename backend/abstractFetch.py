import requests
import xml.etree.ElementTree as ET

# PubMed API efetch endpoint
EFETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

def fetch_abstracts(article_ids):
    """Fetch abstracts for given PubMed article IDs."""
    try:
        params = {
            "db": "pubmed",
            "id": ",".join(article_ids),
            "retmode": "xml",
            "rettype": "abstract"
        }
        response = requests.get(EFETCH_URL, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse XML response
        root = ET.fromstring(response.content)
        abstracts = []
        
        for article in root.findall(".//PubmedArticle"):
            article_id = article.find(".//PMID").text
            abstract = article.find(".//AbstractText")
            abstract_text = abstract.text if abstract is not None else "No Abstract Available"
            abstracts.append((article_id, abstract_text))
        
        print("✅ Abstracts Fetched Successfully!")
        for article_id, abstract in abstracts:
            print(f"ID: {article_id}\nAbstract: {abstract}\n")
        
    except requests.exceptions.RequestException as e:
        print("❌ Failed to Fetch Abstracts:", e)

# Example usage
if __name__ == "__main__":
    article_ids = ["39773054", "39772822"]  # Replace with valid PubMed IDs
    fetch_abstracts(article_ids)