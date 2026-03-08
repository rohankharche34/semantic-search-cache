import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SemanticCache:

    def __init__(self, threshold=0.9):
        self.threshold = threshold
        self.entries = []

        self.hit_count = 0
        self.miss_count = 0

    def lookup(self, embedding):

        if not self.entries:
            self.miss_count += 1
            return None

        vectors = np.array([e["embedding"] for e in self.entries])

        sims = cosine_similarity([embedding], vectors)[0]

        best = sims.argmax()

        if sims[best] >= self.threshold:
            self.hit_count += 1
            return self.entries[best], float(sims[best])

        self.miss_count += 1
        return None

    def add(self, query, embedding, result, cluster):

        self.entries.append({
            "query": query,
            "embedding": embedding,
            "result": result,
            "cluster": cluster
        })

    def stats(self):

        total = self.hit_count + self.miss_count

        hit_rate = self.hit_count / total if total else 0

        return {
            "total_entries": len(self.entries),
            "hit_count": self.hit_count,
            "miss_count": self.miss_count,
            "hit_rate": hit_rate
        }

    def clear(self):
        self.entries = []
        self.hit_count = 0
        self.miss_count = 0
