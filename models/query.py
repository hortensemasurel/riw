class Query:
    """
    This class represent the query.
    """
    def __init__(self, content, stopwords_list, lemmatizer):
        self.content = content
        self.stopwords = stopwords_list
        self.lemmatizer = lemmatizer
        self.tokens = content.split(" ")
        self.__length = len(self.tokens)
        self.term_frequencies = {}
        self.process_query(self.stopwords, self.lemmatizer)

    def remove_stopwords(self, stopwords_list):
        self.tokens = [token for token in self.tokens if token not in stopwords_list]
        self.__length = len(self.tokens)

    def lemmatize(self, lemmatizer):
        self.tokens = [lemmatizer.lemmatize(token) for token in self.tokens]

    def compute_term_frequencies(self):
        for token in self.tokens:
            if token in self.term_frequencies:
                self.term_frequencies[token] += 1
            else:
                self.term_frequencies[token] = 1

    def process_query(self, stopwords_list, lemmatizer):
        """
        Processes the query: remove stop_words, lematize and get term_frequencies.
        :param stopwords_list: list of stop words
        :param lemmatizer
        """
        self.remove_stopwords(stopwords_list)
        self.lemmatize(lemmatizer)
        self.compute_term_frequencies()

    def get_term_frequency(self, target_term):
        """
        Get a targeted term frequency in the query.
        :param target_term: term for which we want the frequency
        """
        try:
            tf = self.term_frequencies[target_term]
        except KeyError:
            return 0
        return tf

    def get_vocabulary(self):
        return list(self.term_frequencies.keys())