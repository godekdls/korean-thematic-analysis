# coding: utf-8
import random
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

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


def load_dataset(seed=123):
    """
    # Arguments
        seed: int, seed for randomizer.
    # Returns
        A tuple of training and validation data.
        Number of categories: 31 (0~30)
    """

    # Load the whole data
    total_texts = []
    total_labels = []

    for category in categories.CATEGORIES:
        collection_name = category['index-name']
        print('reading ' + collection_name)
        documents = mongo.find(collection_name, limit=NUM_OF_SAMPLES_PER_CLASS)
        print(' natural language processing ' + collection_name)
        for document in documents:
            body = document['body']
            total_texts.append(nl_processing.extract_nouns(body))
            total_labels.append(category['class'])
    mongo.close()

    # Shuffle the data
    print('start shuffling')
    random.seed(seed)
    random.shuffle(total_texts)
    random.seed(seed)
    random.shuffle(total_labels)

    # Divide the training data and validation data
    print('Divide the training data and validation data')
    total_len = len(total_labels)
    train_len = int(total_len * 4 / 5)  # 80%
    train_texts = total_texts[:train_len]
    train_labels = total_labels[:train_len]
    test_texts = total_texts[train_len:]
    test_labels = total_labels[train_len:]

    return ((np.array(train_texts), np.array(train_labels)),
            (np.array(test_texts), np.array(test_labels)))


def get_num_classes(train_labels):
    num_classes = train_labels[0]
    for idx in range(1, len(train_labels)):
        if train_labels[idx] > num_classes:
            num_classes = train_labels[idx]
    return num_classes + 1


def get_num_samples_per_class(num_classes, labels):
    temp = np.empty(num_classes)
    temp.fill(0)
    result = ''
    for label in labels:
        temp[label] += 1
    for label in range(len(temp)):
        result += ' / category[' + str(label) + '] : ' + str(temp[label])
    return result


def get_median_num_words_per_sample(sample_texts):
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


def plot_unigram_distribution(sample_texts, top_count=30):
    plt.rc('font', family='NanumGothicOTF')
    plt.rcParams["figure.figsize"] = (14, 4)

    c_vec = CountVectorizer(ngram_range=(1, 1))
    ngrams = c_vec.fit_transform(sample_texts)
    sum_words = ngrams.sum(axis=0)
    words_freq = [(word, sum_words[0, idx]) for word, idx in c_vec.vocabulary_.items()]
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    words_freq = words_freq[:top_count]
    test = []
    for word, count in words_freq:
        for i in range(count):
            test.append(word)
    plt.hist(test, 50)
    plt.xlabel('Uni-grams')
    plt.ylabel('Frequencies')
    plt.title('Sample length distribution')
    plt.show()


if __name__ == '__main__':
    ((train_texts, train_labels), (test_texts, test_labels)) = load_dataset()
    print('number of samples : train data - ', len(train_texts), ' test data - ', len(test_texts))
    num_classes = get_num_classes(train_labels)
    print('number of classes : ', num_classes)
    print('number of samples per class : ')
    print(' train data :', get_num_samples_per_class(num_classes, train_labels))
    print(' test data :', get_num_samples_per_class(num_classes, test_labels))
    print(
        'median number of words per sample : train data - ', get_median_num_words_per_sample(train_texts),
        ' test data - ',
        get_median_num_words_per_sample(test_texts))
    plot_sample_length_distribution(train_texts)
    plot_unigram_distribution(train_texts)
