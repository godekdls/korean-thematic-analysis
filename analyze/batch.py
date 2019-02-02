import sys
import os
from os import path

curdic = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(curdic)
sys.path.append(curdic + '/collect')
from collect import mongo, progress_bar
from config import categories

# Number of samples per class
NUM_OF_SAMPLES_PER_CLASS = 10000  # TODO


def save_into_local():
    for category in categories.CATEGORIES:
        directory = './data/blogs/' + category['index-name']
        if not os.path.exists(directory):
            os.makedirs(directory)

    num_of_categories = len(categories.CATEGORIES)
    for i in range(num_of_categories):
        category = categories.CATEGORIES[i]
        collection_name = category['index-name']
        print('\nreading', collection_name, '... (' + str(i + 1) + '/' + str(num_of_categories) + ')')
        documents = mongo.find(collection_name, limit=NUM_OF_SAMPLES_PER_CLASS)
        total = documents.count()
        suffix = 'downloading'
        progress_bar.progress(0, total, suffix)
        for i in range(total):
            document = documents[i]
            try:
                file_name = './data/blogs/' + category['index-name'] + '/' + document['docId'] + '.txt'
                if not path.isfile(file_name):
                    text = document['tokens']
                    if text:
                        file = open(file_name, 'w')
                        file.write(text)
                        file.close()
            except Exception as e:
                print('failed to process ', e)
                pass
            progress_bar.progress(i, total, suffix)
        progress_bar.progress(total, total, suffix)
    mongo.close()


if __name__ == '__main__':
    save_into_local()
