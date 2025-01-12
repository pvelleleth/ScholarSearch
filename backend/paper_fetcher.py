import requests
from bs4 import BeautifulSoup
import re

def fetch_paper_content(pmid: str) -> dict:
    """Fetch paper content from PubMed Central."""
    try:
        # First, try to get the PMC ID if available
        url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id={pmid}&retmode=xml"
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'xml')
        
        # Get basic metadata
        title = soup.find('ArticleTitle').text if soup.find('ArticleTitle') else "Title not available"
        abstract = soup.find('Abstract').text if soup.find('Abstract') else "Abstract not available"
        
        # Try to get PMC ID
        pmc_id = None
        article_id_list = soup.find('ArticleIdList')
        if article_id_list:
            for article_id in article_id_list.find_all('ArticleId'):
                if article_id.get('IdType') == 'pmc':
                    pmc_id = article_id.text.replace('PMC', '')
                    break
        
        full_text = ""
        if pmc_id:
            # If PMC ID is available, fetch full text
            pmc_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pmc&id={pmc_id}&rettype=xml"
            pmc_response = requests.get(pmc_url)
            pmc_response.raise_for_status()
            
            pmc_soup = BeautifulSoup(pmc_response.content, 'xml')
            
            # Extract full text content
            body = pmc_soup.find('body')
            if body:
                # Get all paragraphs
                paragraphs = body.find_all('p')
                full_text = "\n\n".join([p.get_text() for p in paragraphs])
        
        # Clean up the text
        full_text = re.sub(r'\s+', ' ', full_text).strip()
        abstract = re.sub(r'\s+', ' ', abstract).strip()
        
        return {
            "title": title,
            "abstract": abstract,
            "full_text": full_text if full_text else abstract,  # Use abstract if full text not available
            "has_full_text": bool(full_text)
        }
        
    except Exception as e:
        print(f"Error fetching paper content: {str(e)}")
        return None 