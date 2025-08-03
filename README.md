# ExtractingAndVerifyingTariffClaims 

## An AI-powered fact-checking pipeline that extracts economic claims (specifically surrounding tariffs) from politically diverse news articles. 

It seems like "tariffs" are one of the hottest topics in the news right now. Given its popularitly, it becomes crucial to be able to differentiate between what is based in evidence and what are based in assumption. Using, GPT-4, retrieval-augmented generation (RAG), and a custom-vector database of academic research, the project aims to bridge misinformation gaps by grounding public claims in credible conomic evidence. 

## Features: 
- Claim Extraction from news articles using OpenAI's GPT-4
- Claim Verification via Retrieval-Augmented Generation with GPT-4
- Custom Vector Database populated with economic research papers from CORE API, textbooks, and manually curated sources
- Semantic Search using Pinecone to retrieve the most relevant evidence
- Automated News Scraping using NewsAPI for politically diverse article sources (when storing the articles, the source was classified as left, left-leaning, center, righ-leaning, or right)
- Storage & Indexing with SQLite (structured data) and Pinecone (vector data)

  ## Future improvements:
  - expand the dataset used for semantic search and RAG to be fully indicative of the scholarly evidence out there
  - add confidence scores for claim verification
  - automate political bias detection
