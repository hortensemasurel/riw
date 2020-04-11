class Query:
    """
    This class represents a query.
    """
    def __init__(self, content, stopwords_list, lemmatizer):
        self.content = content
        self.stopwords = stopwords_list
        self.lemmatizer = lemmatizer
        self.words = content.split(" ")
        self.size = len(self.words)
        self.term_frequencies = {}
        self.process_query(self.stopwords, self.lemmatizer)

    def remove_stopwords(self, stopwords_list):
        """
        Remove stopwords from the query's list of words.
        :param stopwords_list: list of stopwords in a certain language
        """
        words_without_stopwords = []
        for word in self.words:
            if word not in stopwords_list:
                words_without_stopwords.append(word)
        self.words = words_without_stopwords
        self.size = len(self.words)

    def lemmatize(self, lemmatizer):
        lemmatized_words = []
        for word in self.words:
            lemmatized_words.append(lemmatizer.lemmatize(word))
        self.words = lemmatized_words

    def compute_term_frequencies(self):
        """
        Compute terms' frequencies in the query.
        """
        for word in self.words:
            if word in self.term_frequencies:
                self.term_frequencies[word] += 1
            else:
                self.term_frequencies[word] = 1

    def process_query(self, stopwords_list, lemmatizer):
        """
        Processes the query: remove stop_words, lemmatize and get term_frequencies.
        :param stopwords_list: list of stop words
        :param lemmatizer
        """
        self.remove_stopwords(stopwords_list)
        self.lemmatize(lemmatizer)
        self.compute_term_frequencies()

    def get_term_frequency(self, term):
        """
        Get a targeted term frequency in the query.
        :param term: term for which we want the frequency
        """
        try:
            tf = self.term_frequencies[term]
        except KeyError:
            return 0
        return tf

    def get_vocabulary(self):
        """ Returns the unique words of the query"""
        return list(self.term_frequencies.keys())