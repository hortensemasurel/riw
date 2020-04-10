from math import sqrt
from time import time

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

        self.collection = Collection(
            collection_name, stopwords_list, lemmatizer
        )
        self.stopwords = stopwords_list
        self.lemmatizer = lemmatizer

    def search(self, string_query: str):
        print("in search")
        """ Returns the score of each document, regarding the query """
        query = Query(string_query.lower(), self.stopwords, self.lemmatizer)
        documents_list = self.get_list_of_documents(query)
        doc_scores = self.get_scores(documents_list, query)
        return doc_scores

    def get_list_of_documents(self, query: Query):
        """Return documents where the tokens of the query appear"""
        final_documents_list = []
        # Get tokens of query
        vocabulary = query.get_vocabulary()
        for token in vocabulary:
            if not final_documents_list:
                final_documents_list = self.collection.get_documents_containing_term(token)
                print(
                    "[Search Engine] Token: {} | Posting list: {} items".format(
                        token, len(final_documents_list)
                    )
                )
            else:
                documents_list = self.collection.get_documents_containing_term(token)
                print(
                    "[Search Engine] Token: {} | Posting list: {} items".format(
                        token, len(documents_list)
                    )
                )
                print("Merge posting list needed")
                # merge the two lists and order the final list
                final_documents_list = sorted(list(set(final_documents_list) | set(documents_list)))
        return final_documents_list

    def get_scores(self, documents_list, query: Query):
        """ Score each document, depending of the tokens it contains"""
        print("[Search Engine] Computing search scores ...")
        query_tf_idf = {}
        query_vocabulary = query.get_vocabulary()
        # get the tf_idf of the tokens of the query
        for token in query_vocabulary:
            tf_idf = query.get_term_frequency(token) * self.collection.compute_idf(token)
            query_tf_idf[token] = tf_idf
        # score the documents which contain the tokens
        doc_scores = {}
        for doc_id in documents_list:
            score = 0
            for token in query_vocabulary:
                normalized_tf = self.collection.log_normalization(
                    term=token, id_document=doc_id
                )
                if normalized_tf == 0:  # the token is not in the document
                    weight = 0
                else:
                    weight = normalized_tf * self.collection.compute_idf(token)
                score += query_tf_idf[token] * weight
            doc_scores[doc_id] = score
        return doc_scores


if __name__ == "__main__":
    word_net_lemmatizer = WordNetLemmatizer()
    searchEngine = SearchEngine(
        collection_name="cs276", stopwords_list=[], lemmatizer=word_net_lemmatizer
    )
