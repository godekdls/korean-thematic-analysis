# coding: utf-8
import random
import numpy as np
import matplotlib.pyplot as plt

import sys
from os import path

curdic = path.dirname(path.dirname(path.abspath(__file__)))
sys.path.append(curdic)
sys.path.append(curdic + '/collect')
from collect import mongo
from config import categories

# Number of samples per class
NUM_OF_SAMPLES_PER_CLASS = 10 # TODO


def load_dataset(seed=123):
    """Loads the IMDb movie reviews sentiment analysis dataset.

    # Arguments
        seed: int, seed for randomizer.

    # Returns
        A tuple of training and validation data.
        Number of categories: 31 (0~30)

    """

    # Load the whole data
    total_data = {}

    for category in categories.CATEGORIES:
        collection_name = category['index-name']
        documents = mongo.find(collection_name, limit=NUM_OF_SAMPLES_PER_CLASS)
        datas = []
        for document in documents:
            data = {}
            data['text'] = document['body']
            data['label'] = category['class']
            datas.append(data)
        total_data[collection_name] = datas
    mongo.close()

    # Divide the training data and validation data
    train_texts = []
    train_labels = []
    test_texts = []
    test_labels = []
    for key, value in total_data.items():
        documents = total_data[key]

        # Shuffle the data
        random.seed(seed)
        random.shuffle(documents)

        total_len = len(documents)
        train_len = int(total_len * 2 / 3)
        for i in range(total_len):
            if i < train_len:
                train_texts.append(documents[i]['text'])
                train_labels.append(documents[i]['label'])
            else:
                test_texts.append(documents[i]['text'])
                test_labels.append(documents[i]['label'])

    return ((train_texts, np.array(train_labels)),
            (test_texts, np.array(test_labels)))


def get_num_classes(train_labels):
    num_classes = train_labels[0]
    for idx in range(1, len(train_labels)):
        if train_labels[idx] > num_classes:
            num_classes = train_labels[idx]
    return num_classes + 1


def get_num_words_per_sample(sample_texts):
    """Returns the median number of words per sample given corpus.

    # Arguments
        sample_texts: list, sample texts.

    # Returns
        int, median number of words per sample.
    """
    num_words = [len(s.split()) for s in sample_texts]
    return np.median(num_words)


def plot_sample_length_distribution(sample_texts):
    """Plots the sample length distribution.

    # Arguments
        samples_texts: list, sample texts.
    """
    plt.hist([len(s) for s in sample_texts], 50)
    plt.xlabel('Length of a sample')
    plt.ylabel('Number of samples')
    plt.title('Sample length distribution')
    plt.show()


if __name__ == '__main__':
    dataset = load_dataset()
    train_texts = dataset[0][0]
    train_labels = dataset[0][1]
    print(train_labels)
    test_texts = dataset[1][0]
    test_labels = dataset[1][1]
    print(get_num_words_per_sample(train_texts))
    print(get_num_classes(train_labels))
    plot_sample_length_distribution(train_texts)
