import time
from os import system

from PyInquirer import style_from_dict, Token, prompt
from nltk.stem import WordNetLemmatizer
from pyfiglet import Figlet

from models.search_engine import SearchEngine

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})


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

    def menu(self):
        f = Figlet(font='slant')
        system('clear')
        print(f.renderText('Welcome to SE-3000'))
        while True:
            questions = [{
                    'type': 'list',
                    'name': 'Choice',
                    'message': 'Do you want to search a term or compute stats on Stanford queries ?',
                    'choices': ['Search', 'Stats', 'Quit']
            }]
            answer = prompt(questions, style=style)
            if answer['Choice'] == "Search":
                question = [{
                    'type': 'input',
                    'name': 'query',
                    'message': 'What\'s your query?'
                }]
                user_query = prompt(question, style=style)
                self.search(user_query['query'])
            elif answer['Choice'] == "Stats":
                question = [{
                    'type': 'input',
                    'name': 'query',
                    'message': 'What\'s your query?'
                }]

                answer = prompt(question, style=style)
            elif answer['Choice'] == "Quit":
                quit()


if __name__ == "__main__":
    interface = Interface()
    interface.menu()
