import sys
import glob
from os import path

curdic = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(curdic)
sys.path.append(curdic + '/collect')
from collect import mongo, progress_bar, nl_processing
from config import categories

# Number of samples per class
NUM_OF_SAMPLES_PER_CLASS = 10000  # TODO


def test():
    num_of_categories = len(categories.CATEGORIES)
    for i in range(num_of_categories):
        category = categories.CATEGORIES[i]
        collection_name = category['index-name']
        print('\nreading', collection_name, '... (' + str(i + 1) + '/' + str(num_of_categories) + ')')
        path = './data/blogs/' + collection_name
        file_names = glob.glob(path + "/*.txt")
        total = len(file_names)
        print(' updating...')
        progress_bar.progress(0, total)
        for i in range(total):
            progress_bar.progress(i, total)
            file_name = file_names[i]
            split = file_name.split("/")
            doc_id = split[len(split) - 1].split(".")[0]
            query = {"docId": doc_id}
            document = mongo.find_one(collection_name, query)
            try:
                document['tokens']
            except Exception:
                file = open(file_name)
                tokens = file.read()
                data = {
                    "$set": {
                        "tokens": tokens
                    }
                }
                mongo.update_one(collection_name, query, data)
    mongo.close()


def test2():
    num_of_categories = len(categories.CATEGORIES)
    for i in range(num_of_categories):
        category = categories.CATEGORIES[i]
        collection_name = category['index-name']
        print('\nreading', collection_name, '... (' + str(i + 1) + '/' + str(num_of_categories) + ')')
        query = {'tokens': {'$exists': False}}
        documents = mongo.find_query(collection_name, query)
        total = documents.count()
        if total > 0:
            progress_bar.progress(0, total)
            for i in range(total):
                document = documents[i]
                data = {
                    "$set": {
                        "tokens": nl_processing.extract_nouns(document['body'])
                    }
                }
                mongo.update_one(collection_name, {"docId": document['docId']}, data)
                progress_bar.progress(i, total)
            progress_bar.progress(total, total)
        else:
            progress_bar.progress(1, 1)
    mongo.close()


if __name__ == '__main__':
    test2()
