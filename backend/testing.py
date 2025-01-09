import requests

# PubMed API endpoint
SEARCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

# Search parameters
search_params = {
    "db": "pubmed",               # Search in PubMed database
    "term": "prevention of autoimmune diseases",  # Search query
    "retmode": "json",            # Return results in JSON format
    "retmax": 5                   # Number of results to return
}

def search_pubmed():
    """Search PubMed and return article IDs."""
    try:
        response = requests.get(SEARCH_URL, params=search_params)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        article_ids = data.get('esearchresult', {}).get('idlist', [])
        
        print("✅ PubMed Search Successful!")
        print("Article IDs:", article_ids)
        
        return article_ids
    
    except requests.exceptions.RequestException as e:
        print("❌ PubMed Search Failed:", e)
        return []

def fetch_article_summary(article_ids):
    """Fetch article summaries based on IDs."""
    try:
        if not article_ids:
            print("❗ No Article IDs to fetch summaries for.")
            return
        
        params = {
            "db": "pubmed",
            "id": ",".join(article_ids),
            "retmode": "json"
        }
        response = requests.get(SUMMARY_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        summaries = []
        for article_id in article_ids:
            summary = data.get('result', {}).get(article_id, {}).get('title', 'No Title Found')
            summaries.append(f"{article_id}: {summary}")
        
        print("✅ Article Summaries Fetched Successfully!")
        for summary in summaries:
            print(summary)
    
    except requests.exceptions.RequestException as e:
        print("❌ Failed to Fetch Summaries:", e)


# Run the functions
if __name__ == "__main__":
    article_ids = search_pubmed()
    fetch_article_summary(article_ids)