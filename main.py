import time
from nltk.stem import WordNetLemmatizer
from models.search_engine import SearchEngine


class Interface:

    def __init__(self, stops=[]):
        print("Loading search engine :\n")
        word_net_lemmatizer = WordNetLemmatizer()
        self.search_engine = SearchEngine(
            collection_name="cs276",
            stopwords_list=stops,
            lemmatizer=word_net_lemmatizer,
        )
        print("Done !\n")

    def search(self, query):
        """
        This function is the main interface for querying the search engine.
        """
        start_time = time.time()
        print("Searching\n")
        doc_scores_query = self.search_engine.search(query)
        print("Sorting\n")
        sorted_docs = [
            k
            for k, v in sorted(
                doc_scores_query.items(), key=lambda item: item[1], reverse=True
            )
        ]

        finished_time = time.time()
        total_time = round((finished_time - start_time) * 1000, 2)
        print("Found requested queries in {}ms".format(total_time))

        print("Results : \n")

        for i, doc_id in enumerate(sorted_docs[:10]):
            document = self.search_engine.collection.documents[doc_id]
            print("{}.\t{}/{}".format(i, document.folder, document.address))
            print("\t{}\n".format(" ".join(document.key_words)))

    def run(self):

        while True:

            print("Please enter your query : ")
            user_query = input()
            search(user_query)


if __name__ == "__main__":
    interface = Interface()
    interface.run()
