# Vector Embedding & Vector DB

## Vector Embedding Basics

### Fundamental Concepts  
- In machine learning, an **embedding** is a mapping that converts high‑dimensional or discrete data (e.g. words, sentences, images) into a dense vector in a continuous vector space, preserving semantic relationships.  
- Within the embedding space, items that are semantically similar lie closer (by cosine similarity, Euclidean distance, etc.).  
- Common embedding forms: word embeddings (Word2Vec, GloVe, etc.), sentence embeddings, document embeddings, multimodal embeddings (text + images, etc.).  

### Role of Embedding in RAG  
- In a **Retrieval‑Augmented Generation (RAG)** system, embeddings are used to transform both the query and the text chunks (from the corpus) into vector form so that semantic similarity can be computed.  
- The process is:  
  1. Preprocess and chunk your document corpus into smaller units (paragraphs, segments).  
  2. Compute embeddings for each chunk and store them in a vector database.  
  3. At query time: convert the incoming user query into its embedding (using the same model).  
  4. Retrieve the nearest neighbor chunks in the embedding space (i.e. semantically similar chunks).  
  5. Feed those retrieved chunks plus the query context into the LLM to generate an answer.  
- Embeddings thus serve as the “bridge” enabling semantic retrieval rather than keyword matching.

## Embedding Model Training Principles

### Core Architecture: BERT (as an example)  
- BERT is a transformer‑based model pretrained via self‑supervised tasks. Although BERT is often used for classification, its internal representations (hidden states) can serve as embedding vectors (especially via the [CLS] token or pooled output).  
- Pure BERT output often needs adaptation (fine‑tuning, pooling, or siamese networks) to produce strong embeddings for similarity tasks.  
- For sentence embedding tasks, **SBERT** (Sentence‑BERT) improves over raw BERT by training a siamese architecture to optimize embedding distances for sentence pairs (e.g. on SNLI, etc.).  

### Core Training Tasks  
#### Masked Language Model (MLM)  
- In MLM, some tokens in input are masked out and the model must predict them based on context. This encourages contextual understanding.  
- The hidden layers thus learn to encode context in their representations.  
- This helps the model learn deeper semantic structures.

#### Next Sentence Prediction (NSP)  
- BERT’s original training includes predicting whether two sentences follow in original text order. This helps the model grasp inter‑sentence coherence.  
- However, many newer models drop NSP (or replace it with alternatives) because its utility is debated.

### Techniques for Enhancing Embedding Quality  
- **Fine‑tuning for similarity tasks**: further train the embedding model on pairs/triplets (e.g. contrastive loss, triplet loss) so that semantically similar items are drawn together and dissimilar ones are pushed apart.  
- **Hard negative mining**: selecting difficult negative examples in training to sharpen the embedding boundaries.  
- **Multi‑task training**: combining embedding objectives with downstream tasks (e.g. classification) to regularize representations.  
- **Quantization / compression**: e.g. reduce embedding precision (4-bit quantization) to save storage and speed up search.  

## Embedding Model Selection Guide

### Key Evaluation Dimensions  
- **Embedding dimension**: higher dimensional embeddings may capture richer features but cost more storage and compute.  
- **Retrieval performance**: e.g. top‑k recall, MRR, embedding space separation on your validation queries.  
- **Latency & cost**: embedding speed, API or inference cost, memory/storage for vectors.  
- **Domain match / vocabulary coverage**: how well does the model’s training domain overlap your data domain? Out‑of‑vocabulary handling matters.  
- **License, support, language coverage**: whether the model supports your languages, license terms, ecosystem support.  

### Iterative Testing & Optimization  
1. Start with a strong general embedding model (e.g. from a leaderboard or prior art).  
2. Sample representative documents & user queries from your domain.  
3. Compute embeddings, run retrieval tests (compute distances, nearest neighbor ranking).  
4. Visualize embedding clusters (e.g. via t‑SNE) to see how queries and relevant chunks align.  
5. Adjust: if performance is poor, consider fine‑tuning on domain data, adjusting loss functions, or trying alternative models.  
6. Monitor cost and latency tradeoffs.

## Multimodal Embedding

### Why Multimodal Embedding?  
- Many applications involve **text + images (or other modalities)** (e.g. document + figures, web pages, product descriptions + photos).  
- Multimodal embedding maps different modalities into a **shared embedding space**, so that, e.g. a textual query can retrieve relevant images (and vice versa).  
- Example: Vertex AI’s multimodal embedding model outputs a 1408‑dimensional vector for mixed input.  
- In practice, pipelines chunk both text and image regions and produce embeddings, then index them together so cross‑modal retrieval is possible.  

## Vector Database

### Purpose of a Vector Database  
- A vector database (or vector store) is tailored to **store, index, and query high‑dimensional vector embeddings** efficiently.  
- It enables **similarity search** (e.g. nearest neighbor) rather than exact match queries.  
- It is a core component in RAG: embeddings for chunks are stored here, and queries are answered via similarity search first.

### Main Functionalities  
- **Insertion / upsert**: add new vectors with metadata (IDs, document pointers, filters).  
- **Indexing / internal structure**: build internal data structures (e.g. approximate nearest neighbor indices).  
- **Search / query**: given a query vector, return nearest neighbors (top‑k) based on similarity metric (cosine, L2, etc.).  
- **Filtering & metadata support**: ability to filter by metadata (e.g. by document type, date).  
- **Hybrid support / combination with sparse indexes** (some systems support combining dense + sparse retrieval).  

### Vector DB vs. Traditional DB  
| Aspect | Traditional DB | Vector DB |
|---|---|---|
| Data type | Structured (relational, key‑value) | Dense numerical vectors + metadata |
| Query mode | Exact matches, range queries | Nearest neighbor / similarity search |
| Indexing method | B‑trees, hash indexes | ANN (HNSW, IVF, PQ, etc.) |
| Use case | Transactions, relational joins | Semantic search, embedding retrieval |

## Indexing & Optimization Strategies

### Context Expansion  
- You can **augment query or chunk contexts** before embedding, e.g. include neighboring sentences or document-level context to reduce semantic mismatch.  
- Another strategy is to represent hierarchical context: embed both small chunk and larger context, then combine results.  
- “Context-aware query grouping” (e.g. CaGR‑RAG) groups similar queries to reduce cache misses and improve disk I/O efficiency in vector search.  

### Structured Indexing  
- Use **structured metadata filters or hybrid indexing**: e.g. partition or prefilter by categories, dates, authors, before doing dense search.  
- Use **multi-index schemes**: e.g. combining a coarse index (cluster-level) with fine per-cluster index.  
- Employ **quantization, compression, or pruning** to reduce index size and speed up search (e.g. 4‑bit quantization).  
- Use **poly-vector retrieval** (for specialized domains) where each item has multiple embeddings (e.g. label embedding + content embedding) to improve retrieval for reference queries.  
