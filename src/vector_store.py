import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class VectorStore:

    def __init__(self, embeddings, docs):
        self.embeddings = embeddings
        self.docs = docs

    def search(self, query_embedding, k=3):
        sims = cosine_similarity([query_embedding], self.embeddings)[0]
        idx = np.argsort(sims)[::-1][:k]

        results = [self.docs[i] for i in idx]
        score = sims[idx[0]]

        return results, float(score)
