import time
from os import system

from PyInquirer import style_from_dict, Token, prompt
from nltk.stem import WordNetLemmatizer
from pyfiglet import Figlet

from models.search_engine import SearchEngine
from stats import compute_accuracy

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
        This method enables to query the search engine.
        """
        start_time = time.time()
        print("Searching\n")
        doc_scores_query = self.search_engine.search(query)
        print("Sorting\n")
        #sort documents with descending scores, the most relevant documents come first.
        sorted_docs = [
            key
            for key, value in sorted(
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
                'message': 'Do you want to search a term or evaluate engine on Stanford queries ?',
                'choices': ['Search', 'Stats', 'Quit']
            },
                {
                    'type': 'input',
                    'name': 'query',
                    'message': 'What\'s your query?',
                    'when': lambda answers: answers['Choice'] == 'Search'
                },
                {
                    'type': 'checkbox',
                    'name': 'stat',
                    'message': 'On which Stanford query should I compute statistics?',
                    'choices': [
                        {
                            'name': '1'
                        },
                        {
                            'name': '2'
                        },
                        {
                            'name': '3'
                        },
                        {
                            'name': '4',
                        },
                        {
                            'name': '5'
                        },
                        {
                            'name': '6'
                        },
                        {
                            'name': '7'
                        },
                        {
                            'name': '8'
                        },
                        {
                            'name': 'Queries 1 to 8 concatenated'
                        }
                    ],
                    'validate': lambda answers: 'You must choose at least one choice.' if len(
                        answers['stat']) == 0 else True,
                    'when': lambda answers: answers['Choice'] == 'Stats'
                },
                {
                    'type': 'confirm',
                    'name': 'quit',
                    'message': 'Do you really want to quit the program ?',
                    'when': lambda answers: answers['Choice'] == 'Quit'
                }]

            output = prompt(questions, style=style)
            if output['Choice'] == 'Quit':
                if output['quit']:
                    quit()
            elif output['Choice'] == 'Search':
                self.search(output['query'])
            elif output['Choice'] == 'Stats':
                if len(output['stat']) == 0:
                    pass
                elif output['stat'][0] == 'Queries 1 to 8 concatenated':
                    query_all = []
                    for i in range(1, 9):
                        with (open(f"queries/dev_queries/query.{i}", "r")) as file:
                            query = next(file).rstrip("\n")
                        query_all.append(query)
                    q = ' '.join(query_all)
                    self.search(q)
                else:
                    compute_accuracy(self.search_engine, output['stat'])


if __name__ == "__main__":
    interface = Interface()
    interface.menu()
