from os import path, getcwd, chdir
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


STOPWORDS = stopwords.words("english")


class Document:
    """
    This class aims at representing a document extracted from the dataset.
    """

    def __init__(self, id_doc: int, id_folder: int, address: str):
        self.id = id_doc
        self.folder = id_folder
        self.address = address
        self.size = 0
        self.words = []
        self.key_words = []

    def get_content(self, path_to_corpus):
        """
        Read the content of a file and add it into self.words.
        :param path_to_corpus: path to the documents
        """
        #path to the targeted document
        path_to_file = path.join(path_to_corpus, f"{self.folder}/{self.address}")

        with open(path_to_file, "r") as document:
            for line in document.readlines():
                self.words.extend(line.rstrip("\n").split(" "))

    def filter_non_alpha_characters(self):
        """
        Filter non alphanumeric character from the list of words in the document.
        """
        filtered_words = []

        for word in self.words:
            if word.isalpha():
                filtered_words.append(word)
        self.words = filtered_words
        self.size = len(self.words)

    def remove_stopwords(self,stopwords_list):
        """
        Remove stopwords for the document's list of words.
        :param stopwords_list: list of stopwords in a certain language
        """
        words_without_stopwords = []

        for word in self.words:
            if word not in stopwords_list:
                words_without_stopwords.append(word)
        self.words = words_without_stopwords
        self.size = len(self.words)

    def lemmatize_words(self, lemmatizer):
        lemmatized_words = []
        for word in self.words:
            lemmatized_words.append(lemmatizer.lemmatize(word))
        self.words = lemmatized_words

    def compute_frequencies(self):
        """
        Compute term frequency in the document.
        :return: a dictionary whose keys are the terms and values the frequencies of the terms
        """
        dict_frequencies = {}
        for word in self.words:
            if word in dict_frequencies.keys():
                dict_frequencies[word] += 1
            else :
                dict_frequencies[word] = 1
        return dict_frequencies

    def process_document(self, stopwords_list, lemmatizer):
        """
        Processing the document thanks to the methods defined above
        :param stopwords_list: list of stopwords in a certain language
        :return:
        """
        self.filter_non_alpha_characters()
        self.remove_stopwords(stopwords_list)
        self.lemmatize_words(lemmatizer)

    def get_vocabulary(self):
        return list(set(self.words))


if __name__ == "__main__":

    #Change working directory to be at the root
    ### voir comment on peut faire ca mieux
    working_directory = getcwd()
    print(working_directory[:-7])
    chdir(working_directory[:-7])

    #Create a Document instance
    document = Document(id_doc=0, id_folder=0, address="3dradiology.stanford.edu_")

    #Load content and process the documents
    document.get_content("data/cs276")
    lemmatizer_wordnet = WordNetLemmatizer()
    stopwords_nltk = stopwords.words("english")
    document.process_document(stopwords_nltk, lemmatizer_wordnet)
    print(document.words)