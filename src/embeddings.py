from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

class EmbeddingPipeline:

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            max_df=0.7,
            min_df=5
        )

        self.svd = TruncatedSVD(n_components=200)

    def load_dataset(self):
        dataset = fetch_20newsgroups(
            subset="all",
            remove=("headers","footers","quotes")
        )
        return dataset.data

    def fit_transform(self, docs):
        tfidf = self.vectorizer.fit_transform(docs)
        embeddings = self.svd.fit_transform(tfidf)
        return embeddings

    def transform_query(self, query):
        vec = self.vectorizer.transform([query])
        return self.svd.transform(vec)[0]
