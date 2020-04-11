from nltk.stem import WordNetLemmatizer

from models.collection import Collection
from models.query import Query


class SearchEngine:
    def __init__(
            self,
            collection_name: str,
            stopwords_list,
            lemmatizer,
    ):

        self.collection = Collection(collection_name, stopwords_list, lemmatizer)
        self.stopwords = stopwords_list
        self.lemmatizer = lemmatizer

    def search(self, string_query: str):
        """ Returns a score of each document, regarding the query """
        query = Query(string_query.lower(), self.stopwords, self.lemmatizer)
        documents_list = self.get_list_of_documents(query)
        doc_scores = self.compute_scores(documents_list, query)
        return doc_scores

    def get_list_of_documents(self, query: Query):
        """Return documents where the words of the query appear"""
        target_documents_list = []
        # Get words of query
        vocabulary = query.get_vocabulary()
        for word in vocabulary:
            if not target_documents_list:
                target_documents_list = self.collection.get_documents_containing_term(word)
                print(
                    f"[Search Engine] the word {word} is present in {len(target_documents_list)} items"
                    )

            else:
                documents_list = self.collection.get_documents_containing_term(word)
                print(
                    f"[Search Engine] the word {word} is present in {len(documents_list)} items"
                    )
                print("Merge ...")
                # merge the two lists and order the final list
                target_documents_list = sorted(list(set(target_documents_list) | set(documents_list)))
        return target_documents_list

    def compute_scores(self, list_of_docs, query: Query):
        """ Scores each document, depending of the tokens it contains."""
        print("Search Engine is computing search scores ...")
        query_tf_idf = {}
        vocab_query = query.get_vocabulary()
        # get the tf_idf for words in the query
        for word in vocab_query:
            tf_idf = query.get_term_frequency(word) * self.collection.compute_idf(word)
            query_tf_idf[word] = tf_idf
        # score the documents which contain the words
        doc_scores = {}
        for doc_id in list_of_docs:
            score = 0
            for word in vocab_query:
                normalized_tf = self.collection.log_normalization(
                    term=word, id_document=doc_id
                )
                if normalized_tf == 0:  # the word is not in the document
                    doc_tf_idf = 0
                else:
                    doc_tf_idf = normalized_tf * self.collection.compute_idf(word) #tf-idf for the word in the document
                score += query_tf_idf[word] * doc_tf_idf
            doc_scores[doc_id] = score
        return doc_scores


if __name__ == "__main__":
    word_net_lemmatizer = WordNetLemmatizer()
    searchEngine = SearchEngine(
        collection_name="cs276", stopwords_list=[], lemmatizer=word_net_lemmatizer
    )
