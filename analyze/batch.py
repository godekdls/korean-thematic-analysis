import sys
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
        collection_name = category['index-name']
        print('reading', collection_name)
        documents = mongo.find(collection_name, limit=NUM_OF_SAMPLES_PER_CLASS)
        total = len(documents)
        progress_bar.progress(0, total)
        print(' natural language processing ' + collection_name)
        for i in range(text):
            document = documents[i]
            try:
                file_name = './data/blogs/' + category['index-name'] + '/' + document['docId'] + '.txt'
                if not path.isfile(file_name):
                    file = open(file_name, 'w')
                    text = document['tokens']
                    file.write(text)
                    file.close()
            except Exception as e:
                print('failed to process ', e)
                pass
            progress_bar.progress(i, total)
    mongo.close()


if __name__ == '__main__':
    save_into_local()