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
