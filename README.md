# Semantic Search System with Fuzzy Clustering and Semantic Cache

## Overview

This project implements a **lightweight semantic search system** built on the **20 Newsgroups dataset**.
The system combines **vector embeddings**, **fuzzy clustering**, and a **custom semantic cache** to provide efficient query retrieval through a **FastAPI service**.

Unlike traditional keyword search systems, this implementation performs **semantic retrieval**, meaning queries that are phrased differently but share similar meaning can retrieve relevant results.

The system also includes a **semantic caching mechanism** that avoids recomputation for similar queries without relying on external caching tools such as Redis or Memcached.

---

# Architecture

The system is composed of four primary components:

### 1. Embedding Pipeline

Documents are converted into vector representations using:

* **TF-IDF vectorization**
* **Truncated SVD (Latent Semantic Analysis)**

This approach reduces high-dimensional sparse vectors into a compact semantic representation.

Pipeline:

Dataset → TF-IDF Vectorizer → Truncated SVD → Dense Embeddings

---

### 2. Fuzzy Clustering

Instead of assigning each document to a single cluster, the system uses **Gaussian Mixture Models (GMM)** to compute **soft cluster memberships**.

This reflects the real-world nature of documents, where content can belong to multiple topics.

For each document:

Cluster Membership = Probability Distribution across clusters

Example:

Document →
Cluster 3 : 0.62
Cluster 7 : 0.28
Cluster 12 : 0.10

The **dominant cluster** is the cluster with the highest probability.

---

### 3. Vector Search

Document embeddings are stored in an in-memory **vector store**.

Query processing works as follows:

1. Query is converted to embedding
2. Cosine similarity is computed against document embeddings
3. Top-k most similar documents are retrieved

This provides semantic similarity rather than keyword matching.

---

### 4. Semantic Cache

Traditional caches only work when queries are identical.

This project implements a **semantic cache**, which detects when a query is **similar to a previously asked query**.

Steps:

1. Query embedding is generated
2. Similarity is computed against cached query embeddings
3. If similarity exceeds a threshold → **cache hit**
4. Otherwise → **cache miss and computation**

Similarity metric: **Cosine similarity**

Default cache threshold:

0.90

This value controls how strict the cache matching is.

---

# Project Structure

```
semantic-search-cache
│
├── src
│   ├── api.py              # FastAPI application
│   ├── search.py           # Main search system logic
│   ├── cache.py            # Semantic cache implementation
│   ├── embeddings.py       # TF-IDF + SVD embedding pipeline
│   ├── clustering.py       # Gaussian Mixture fuzzy clustering
│   └── vector_store.py     # Vector similarity search
│
├── run.sh                  # Startup script
├── requirements.txt        # Python dependencies
└── README.md
```

---

# Dataset

This project uses the **20 Newsgroups dataset** available through **scikit-learn**.

It contains approximately **20,000 documents** across **20 categories**, including:

* politics
* religion
* computer graphics
* space
* sports
* electronics

The dataset is loaded directly via:

```
sklearn.datasets.fetch_20newsgroups
```

Noise such as **headers, footers, and quotes** is removed during loading to improve semantic quality.

---

# API Endpoints

### 1. Query Endpoint

POST `/query`

Request:

```
{
  "query": "space shuttle launch failure"
}
```

Response:

```
{
  "query": "...",
  "cache_hit": true,
  "matched_query": "...",
  "similarity_score": 0.91,
  "result": "...",
  "dominant_cluster": 3
}
```

Fields:

| Field            | Description                              |
| ---------------- | ---------------------------------------- |
| query            | user query                               |
| cache_hit        | indicates whether result came from cache |
| matched_query    | cached query matched                     |
| similarity_score | cosine similarity score                  |
| result           | retrieved document snippet               |
| dominant_cluster | cluster ID with highest probability      |

---

### 2. Cache Statistics

GET `/cache/stats`

Example response:

```
{
  "total_entries": 42,
  "hit_count": 17,
  "miss_count": 25,
  "hit_rate": 0.405
}
```

---

### 3. Cache Reset

DELETE `/cache`

Clears all cached entries and resets statistics.

---

### 4. Health Check

GET `/health`

Response:

```
{
  "status": "ok"
}
```

---

# Setup Instructions

The project can be run on **Linux, macOS, or Windows**.

---

# Linux / macOS Setup

### 1. Clone repository

```
git clone <repository-url>
cd semantic-search-cache
```

### 2. Create virtual environment

```
python3 -m venv venv
```

### 3. Activate environment

```
source venv/bin/activate
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

### 5. Run the service

```
chmod +x run.sh
./run.sh
```

The API will start at:

```
http://localhost:8000
```

Interactive API documentation:

```
http://localhost:8000/docs
```

---

# Windows Setup

### 1. Clone repository

```
git clone <repository-url>
cd semantic-search-cache
```

### 2. Create virtual environment

```
python -m venv venv
```

### 3. Activate environment

```
venv\Scripts\activate
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

### 5. Run the server

Navigate to the src folder and run:

```
python -m uvicorn api:app --host 0.0.0.0 --port 8000
```

Open in browser:

```
http://localhost:8000/docs
```

---

# Example Queries

```
space shuttle launch
gun control debate
computer graphics rendering
religion vs atheism
hockey playoffs
```

---

# Design Decisions

### Embeddings

TF-IDF + Truncated SVD was chosen because:

* Lightweight
* No external model downloads
* Good semantic compression for news articles

---

### Clustering

Gaussian Mixture Models provide **soft clustering**, allowing documents to belong to multiple topics.

This is important because many news articles contain **mixed themes**.

---

### Cache Design

The cache is implemented from scratch using:

* Query embeddings
* Cosine similarity
* Threshold based lookup

No external caching systems were used.

---

# Cache Threshold Behavior

The threshold controls **how strict the semantic cache is**.

| Threshold | Behaviour          |
| --------- | ------------------ |
| 0.70      | aggressive caching |
| 0.85      | balanced           |
| 0.95      | very strict        |

Lower threshold → more cache hits but risk of incorrect matches.

Higher threshold → more accurate but fewer hits.

---

# Future Improvements

Possible improvements include:

* Cluster-aware cache lookup
* FAISS vector database
* transformer embeddings (Sentence Transformers)
* persistent cache storage
* distributed deployment

---

# Running the Demo

Start the service and send queries through the API documentation interface:

```
http://localhost:8000/docs
```

Repeat a similar query to observe **semantic cache hits**.

Example:

Query 1:

```
space shuttle launch
```

Query 2:

```
nasa rocket launch failure
```

The second query may be served from the cache if similarity exceeds the threshold.

---
