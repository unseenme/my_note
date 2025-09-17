# RAG Introduction — Study Notes

## What is RAG  
- **RAG** stands for **Retrieval‑Augmented Generation**.  
- The core idea: combine **a retrieval module** (which fetches relevant documents / contexts) with **a generation module** (a language model) to produce answers.  

## Why RAG  

RAG helps to address issues/limitations of pure generation models:  

1. **Knowledge limitations**  
   - Generation without retrieval is limited by what the model “knows” at training time.  
   - It may be wrong or outdated.  

2. **Hallucination**  
   - Pure generation tends to hallucinate—i.e. produce plausible‐looking but incorrect or invented details.  

3. **Efficiency / Scaling knowledge**  
   - Updating a large LM by retraining or fine‑tuning over huge corpora is expensive.  
   - With retrieval, you can update or add documents without retraining the generation model.  

## How RAG works — Components  

- **Retriever**  
  - Given a query or prompt, fetch top‑k relevant documents (or passages) from a corpus.  

- **Generator**  
  - Takes the query + retrieved documents as input, and outputs the final answer.  

- The retriever may be dense (embedding‑based) or sparse (e.g. TF‑IDF, BM25).  
- The generator is usually a powerful pretrained language model.  

## Workflow / Pipeline  

1. User issues a query.  
2. Retriever fetches relevant documents from external knowledge source.  
3. Retrieved documents are passed along with the query to the generator.  
4. Generator produces the output, ideally grounded in those documents.  

## Benefits and Trade‑Offs  

**Benefits:**

- More **up‑to‑date** knowledge via retrieval.  
- Less hallucination (because generator conditions on real documents).  
- More flexible / scalable: can update the data.  

**Trade‑offs / Challenges:**

- Quality of retrieval matters a lot. Bad or irrelevant retrieved docs lead to bad answers.  
- Latency: retrieval and generation both cost time.  
- Managing/documenting the document corpus (indexing, freshness).  
- The generator still might not faithfully use retrieved info or might still hallucinate.
