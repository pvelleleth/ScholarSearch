# AI-Powered search tool for PubMed

## 1. Overview
**Product Name:** ScholarSearch

**Description:**  
ScholarSearch is a search tool designed to enhance the PubMed search experience through AI summarization and an interactive chat interface. This application allows users to efficiently discover, understand, and engage with medical literature.

**Purpose:**  
To streamline the process of discovering and understanding research papers, saving researchers, students, and professionals time while improving insight extraction.

---

## 2. Goals and Objectives
- Provide **accurate, AI-powered summaries** for PubMed search results.  
- Enable users to interact conversationally with research papers through a **Chat feature**.  
- Deliver a seamless user experience with **modern UI/UX** and robust backend performance.  

---

## 3. Target Audience
- **Researchers and Academics:** Looking for efficient ways to explore and analyze biomedical literature.  
- **Students:** Seeking simplified summaries and direct engagement with research content.  
- **Professionals:** Needing quick, actionable insights from academic papers.  

---

## 4. Features
### **Find Tab (AI Search Engine for PubMed)**
- **PubMed API Integration:** Fetch papers, abstracts, and metadata.  
- **AI Summarization:** Use GPT4o to summarize abstracts and extract key insights.  
- **Search Filters:** Include filters for publication date, authors, journals, and open access.  
- **Query Suggestions:** Provide autocomplete and related topic suggestions.  

### **Chat Tab (Interactive Research Paper Chat)**
- **Document Loading:** Users can specify a PubMed paper to interact with.  
- **Conversational Interface:** Users can ask questions like:
  - "What are the main findings?"
  - "Explain the methodology in simple terms."
- **AI-Powered Insights:** Use GPT4o to extract answers based on the paper's content.    

---

## 5. Tools & Tech Stack
### **Backend:**
- **Framework:** FastAPI (Python) for API development.  
- **LLM Integration:** GPT4o for AI-powered summarization and chat functionality.  
- **Caching:** Redis for temporary storage of frequently queried data. (To Be Implemented)  
- **PubMed API:** To fetch research metadata, abstracts, and full-text links.  

### **Frontend:**
- **Framework:** React for building the user interface.  
- **Styling:** Tailwind CSS for responsive and modern design.  

---

## 6. Application Workflow
### **Find Tab Workflow**
1. User enters a query in the search bar.  
2. Backend queries the PubMed API to fetch relevant papers and abstracts.  
3. GPT4o summarizes abstracts and extracts key insights.  
4. Results are displayed in a list format with summaries, filters, and sort options.  

### **Chat Tab Workflow**
1. User specifies a paper via search result selection.  
2. Backend fetches the paper’s abstract or full text (if available).  
3. GPT4o processes the document to create embeddings stored in Pinecone/Qdrant.  
4. User asks questions; backend retrieves relevant content  

---

## 7. Installation Instructions
To set up and run the application locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/pvelleleth/ScholarSearch.git
   cd ScholarSearch
   ```

2. **Set Up Environment Variables**:
   - Create a `.env` file in the root of the backend directory and add your OpenAI API key:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key_here
     ```

3. **Install Backend Dependencies**:
   - Navigate to the backend directory and install the required packages:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Run the FastAPI Server**:
   ```bash
   uvicorn main:app --reload
   ```

5. **Install Frontend Dependencies**:
   - Open a new terminal, navigate to the frontend directory, and install the required packages:
   ```bash
   cd frontend/scholarfront
   npm install
   ```

6. **Start the Frontend Development Server**:
   ```bash
   npm run dev
   ```

7. **Access the Application**:
   - Open your web browser and go to `http://localhost:3000` to access the application.
