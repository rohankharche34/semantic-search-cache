from embeddings import EmbeddingPipeline
from clustering import FuzzyClusterer
from vector_store import VectorStore
from cache import SemanticCache

class SearchSystem:

    def __init__(self):

        self.embedder = EmbeddingPipeline()

        docs = self.embedder.load_dataset()

        embeddings = self.embedder.fit_transform(docs)

        self.vector_store = VectorStore(embeddings, docs)

        self.clusterer = FuzzyClusterer()
        self.clusterer.fit(embeddings)

        self.cache = SemanticCache()

    def query(self, text):

        q_emb = self.embedder.transform_query(text)

        cache_hit = self.cache.lookup(q_emb)

        if cache_hit:

            entry, score = cache_hit

            return {
                "query": text,
                "cache_hit": True,
                "matched_query": entry["query"],
                "similarity_score": score,
                "result": entry["result"],
                "dominant_cluster": entry["cluster"]
            }

        results, score = self.vector_store.search(q_emb)

        cluster = self.clusterer.dominant_cluster(q_emb)

        result = results[0][:500]

        self.cache.add(text, q_emb, result, cluster)

        return {
            "query": text,
            "cache_hit": False,
            "matched_query": None,
            "similarity_score": score,
            "result": result,
            "dominant_cluster": cluster
        }
