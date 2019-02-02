import sys
from os import path
import nl_processing

curdic = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(curdic)
sys.path.append(curdic + '/collect')
from collect import mongo
from config import categories

# Number of samples per class
NUM_OF_SAMPLES_PER_CLASS = 1000  # TODO


def save_nl_processed_data():
    for category in categories.CATEGORIES:
        collection_name = category['index-name']
        print('reading ' + collection_name)
        documents = mongo.find(collection_name, limit=NUM_OF_SAMPLES_PER_CLASS)
        print(' natural language processing ' + collection_name)
        for document in documents:
            try:
                text = nl_processing.extract_nouns(document['body'])
                file_name = './data/blogs/' + category['index-name'] + '/' + document['docId'] + '.txt'
                if not path.isfile(file_name):
                    file = open(file_name, 'w')
                    file.write(text)
                    file.close()
            except Exception as e:
                print('failed to process ', e)
                pass
    mongo.close()


if __name__ == '__main__':
    save_nl_processed_data()