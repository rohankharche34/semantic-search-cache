from sklearn.mixture import GaussianMixture

class FuzzyClusterer:

    def __init__(self, n_clusters=20):
        self.model = GaussianMixture(
            n_components=n_clusters,
            covariance_type="diag",
            random_state=42
        )

    def fit(self, embeddings):
        self.model.fit(embeddings)

    def get_memberships(self, embeddings):
        return self.model.predict_proba(embeddings)

    def dominant_cluster(self, embedding):
        probs = self.model.predict_proba([embedding])[0]
        return int(probs.argmax())
