from nltk.stem import WordNetLemmatizer

from models.search_engine import SearchEngine


def compute_accuracy(search_engine, query):
    for i in query:
        dev_output = []
        with (open(f"queries/dev_queries/query.{i}", "r")) as file:
            query = next(file).rstrip("\n")
        query_output = search_engine.search(query)
        docs = [
            k for k, v in sorted(query_output.items(), key=lambda item: item[1], reverse=True)
        ]
        se_output = []
        for id_query in docs:
            document = search_engine.collection.documents[id_query]
            line = f"{document.folder}/{document.address}"
            se_output.append(line)

        with open(f"queries/dev_output/{i}.out", "r") as file:
            reader = file.readlines()
            for line in reader:
                parsed_line = line.rstrip("\n").split(" ")
                dev_output.append(parsed_line[0])

        se_output = se_output[: len(dev_output)]

        dev_output = sorted(dev_output)
        se_output = sorted(se_output)
        final_list = merge_list(dev_output, se_output)
        score = len(final_list) / len(dev_output)

        print(
            'For Query {} : "{}" the accuracy score is {}%'.format(
                i, query, "{0:.2f}".format(score * 100)
            )
        )


def merge_list(list1, list2):
    result = []
    index1 = 0
    index2 = 0
    n1 = len(list1)
    n2 = len(list2)
    while index1 < n1 and index2 < n2:
        if list1[index1] == list2[index2]:
            result.append(list1[index1])
            index1 += 1
            index2 += 1
        elif list1[index1] > list2[index2]:
            index2 += 1
        elif list1[index1] < list2[index2]:
            index1 += 1
    return result


if __name__ == "__main__":
    word_net_lemmatizer = WordNetLemmatizer()
    print("Loading search engine :\n")
    engine = SearchEngine(
        collection_name="cs276",
        stopwords_list=[],
        lemmatizer=word_net_lemmatizer,
    )
    compute_accuracy(engine)
