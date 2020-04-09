from os import path, listdir, getcwd, walk
from pickle import load, dump
from typing import List, Dict
from math import log, sqrt

from nltk.stem import WordNetLemmatizer


from models.document import Document

class Collection:
    """
    This class aims at representing a collection of documents
    """

    def __init__(self, name: str, stopwords_list: List[str], lemmatizer, weighting_model: str = "tf-idf"):
        self.name = name
        self.documents = []
        self.inverted_index = {}
        self.weighting_model = weighting_model
        self.stopwords = stopwords_list
        self.lemmatizer = lemmatizer
        self.path_to_corpus = path.join(getcwd(), f"data/{name}")
        self.number_of_docs = 0

        self.load_docs()
        self.load_inverted_index(weighting_model)

    def load_docs(self):
        """
        Aims at loading all the collection's documents (processed) in the collection instance.
        """
        number_document_loaded = 0
        for id_directory in range(10):
            path_directory = path.join(self.path_to_corpus, str(id_directory))
            for textfile in listdir(path_directory):
                #create a document instance
                document = Document(
                    id_doc=number_document_loaded,
                    id_folder=id_directory,
                    address=textfile,
                )
                #load data and process documents (filter, remove stopwords and lemmatize)
                document.get_content(self.path_to_corpus)
                document.process_document(
                    stopwords_list=self.stopwords, lemmatizer=self.lemmatizer
                )
                self.documents.append(document)
                number_document_loaded += 1
        self.number_of_docs = number_document_loaded

    def create_inverted_index(self):
        """
        Creates the inverted index for the collection
        """
        for document in self.documents:
            dict_term_weights = document.compute_frequencies()
            for term, weight in dict_term_weights.items():
                if term in self.inverted_index:
                    #the term was already found in another document, we add a key with the current document
                    self.inverted_index[term][document.id] = weight
                else:
                    #the term was not found in another document, we create a key for this term
                    self.inverted_index[term] = {document.id: weight}

    def compute_term_frequency_in_collection(self, term, id_document):
        """
        Computes a targeted term frequency in the targeted document in the collection.
        :param term: term for which we want the frequency
        :param id_document: the document we analyse
        :return: term frequency (TF)
        """
        try :
            tf = self.inverted_index[term][id_document]
            return tf
        except KeyError:
            return 0

    def log_normalization(self, term, id_document):
        """
        Computes the logarithmically scaled frequency: tf(t,d) = log (1 + ft,d)
        :param term: term for which we want to compute a normalized tf
        :param id_document: the document we analyse
        :return: normalized tf
        """
        tf = self.compute_term_frequency_in_collection(term, id_document)
        if tf == 0:
            return 0
        normalized_tf = 1 + log(tf)
        return normalized_tf

    def compute_idf(self, term):
        """
        Computes the inverse document frequency
        :param term: targeted term
        :return: idf of the term in the collection
        """
        try:
            #thanks to the inverted index, we have access to all the documents containing the term
            docs = self.inverted_index[term].keys()
            df = len(docs)
        except KeyError:
            return 0
        return log(self.number_of_docs/df)

    def compute_tf_idf(self, term, id_document):
        """
        Computes tf-idf for a term in a document
        :param term: targeted term
        :param id_document: targeted document we want to analyse
        :return: tf-idf for this term in this document
        """
        tf_idf = self.log_normalization(term, id_document)v* self.compute_idf(term)
        return tf_idf

if __name__ == "__main__":
    word_net_lemmatizer = WordNetLemmatizer()
    collection = Collection(
        name="cs276", stopwords_list=[], lemmatizer=word_net_lemmatizer
    )
