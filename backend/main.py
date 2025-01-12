from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from typing import List, Optional, Dict
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
from datetime import datetime
import numpy as np
from openai import OpenAI
from paper_fetcher import fetch_paper_content

load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Store paper content in memory cache
paper_cache: Dict[str, dict] = {}

class ChatRequest(BaseModel):
    pmid: str
    message: str

class ChatResponse(BaseModel):
    response: str

def get_chat_response(system_prompt: str, user_message: str) -> str:
    """Get chat response from OpenAI."""
    try:
        response = client.chat.completions.create(
            model="gpt-4",  # or gpt-3.5-turbo if preferred
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint that uses OpenAI to respond to questions about the paper."""
    try:
        # Get paper content (from cache or fetch new)
        if request.pmid not in paper_cache:
            paper_content = fetch_paper_content(request.pmid)
            if not paper_content:
                raise HTTPException(status_code=404, detail="Paper not found or couldn't be fetched")
            paper_cache[request.pmid] = paper_content
        
        paper = paper_cache[request.pmid]
        
        # Create system prompt
        system_prompt = f"""You are a helpful AI assistant that helps users understand research papers. 
You have access to the following paper:

Title: {paper['title']}

Content: {paper['full_text']}

Your task is to help the user understand this paper by answering their questions accurately based on the paper's content.
If the answer cannot be found in the paper, clearly state that. Always maintain scientific accuracy and cite specific sections
when possible. If you're making an inference or connection not explicitly stated in the paper, make that clear."""

        # Get response from OpenAI
        response = get_chat_response(system_prompt, request.message)
        
        return ChatResponse(response=response)
        
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

class SearchResult(BaseModel):
    pmid: str
    title: str
    abstract: str
    authors: List[str]
    publication_date: str
    relevance_score: float

def get_embedding(text: str):
    """Get embedding from OpenAI API"""
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response.data[0].embedding

def parse_pubmed_xml(xml_text: str) -> List[dict]:
    """Parse PubMed XML response and extract paper details"""
    root = ET.fromstring(xml_text)
    papers = []
    
    for article in root.findall(".//PubmedArticle"):
        try:
            # Extract PMID
            pmid = article.find(".//PMID").text
            
            # Extract title
            title = article.find(".//ArticleTitle").text or "No title available"
            
            # Extract abstract
            abstract_element = article.find(".//Abstract/AbstractText")
            if abstract_element is not None and abstract_element.text:
                abstract = abstract_element.text
            else:
                abstract = "No abstract available"  # Ensure abstract is a string
            
            # Log if abstract is still None
            if abstract is None:
                print(f"Warning: Abstract is None for PMID: {pmid}")

            # Extract authors
            authors = []
            author_list = article.findall(".//Author")
            for author in author_list:
                last_name = author.find("LastName")
                fore_name = author.find("ForeName")
                if last_name is not None and fore_name is not None:
                    authors.append(f"{fore_name.text} {last_name.text}")
            
            # Extract publication date
            pub_date = article.find(".//PubDate")
            year = pub_date.find("Year")
            month = pub_date.find("Month")
            day = pub_date.find("Day")
            
            date_str = f"{year.text if year is not None else '2000'}-{month.text if month is not None else '01'}-{day.text if day is not None else '01'}"
            
            papers.append({
                "pmid": pmid,
                "title": title,
                "abstract": abstract,  # This will now always be a string
                "authors": authors,
                "publication_date": date_str
            })
            
        except Exception as e:
            print(f"Error parsing article {pmid if 'pmid' in locals() else 'unknown'}: {str(e)}")
            continue
    
    return papers

def fetch_from_pubmed(query: str, max_results: int = 50) -> List[dict]:
    """Fetch papers from PubMed API"""
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    # First get the PMIDs
    search_url = f"{base_url}/esearch.fcgi"
    search_params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json",
        "sort": "relevance"
    }
    
    try:
        response = requests.get(search_url, params=search_params)
        response.raise_for_status()
        pmids = response.json()["esearchresult"]["idlist"]
        
        # Then fetch the details for each PMID
        fetch_url = f"{base_url}/efetch.fcgi"
        fetch_params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml"
        }
        
        response = requests.get(fetch_url, params=fetch_params)
        response.raise_for_status()
        
        # Parse XML response
        papers = parse_pubmed_xml(response.text)
        return papers
        
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"PubMed API error: {str(e)}")

def rank_results(papers: List[dict], query: str) -> List[SearchResult]:
    """Rank papers using OpenAI's semantic search"""
    if not papers:
        return []
    
    try:
        # Get query embedding
        query_embedding = get_embedding(query)
        
        # Get embeddings for each paper
        ranked_papers = []
        for paper in papers:
            # Combine title and abstract for better semantic understanding
            paper_text = f"Title: {paper['title']}\nAbstract: {paper['abstract']}"
            paper_embedding = get_embedding(paper_text)
            
            # Calculate similarity score using dot product
            score = np.dot(query_embedding, paper_embedding)
            
            ranked_papers.append(
                SearchResult(
                    pmid=paper["pmid"],
                    title=paper["title"],
                    abstract=paper["abstract"],
                    authors=paper["authors"],
                    publication_date=paper["publication_date"],
                    relevance_score=float(score)
                )
            )
        
        # Sort by relevance score
        return sorted(ranked_papers, key=lambda x: x.relevance_score, reverse=True)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

@app.get("/api/search", response_model=List[SearchResult])
async def search(query: str, max_results: Optional[int] = 50):
    """Search endpoint that combines PubMed results with semantic ranking"""
    try:
        # Fetch papers from PubMed
        papers = fetch_from_pubmed(query, max_results)
        
        # Rank results using semantic search
        ranked_results = rank_results(papers, query)
        
        return ranked_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))