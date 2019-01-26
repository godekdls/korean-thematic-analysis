from tensorflow.python.keras.preprocessing import sequence
from tensorflow.python.keras.preprocessing import text

# Vectorization parameters
# Limit on the number of features.
TOP_K = 2000

# Limit on the length of text sequences. Sequences longer than this will be truncated
MAX_SEQUENCE_LENGTH = 500


def vectorize(train_texts, val_texts, test_texts):
    """Vectorizes texts as sequence vectors.

    1 text = 1 sequence vector with fixed length.

    # Arguments
        train_texts: list, training text strings.
        val_texts: list, cross validation text strings.
        test_texts: list, testing text strings

    # Returns
        x_train, x_val, x_test, word_index: vectorized training, cross validation
            and testing texts and word index dictionary.
    """
    # Create vocabulary with training texts.
    tokenizer = text.Tokenizer(num_words=TOP_K)
    tokenizer.fit_on_texts(train_texts)

    # Vectorize training and validation texts.
    x_train = tokenizer.texts_to_sequences(train_texts)
    x_val = tokenizer.texts_to_sequences(val_texts)
    x_test = tokenizer.texts_to_sequences(test_texts)

    # Get max sequence length.
    max_length = len(max(x_train, key=len))
    if max_length > MAX_SEQUENCE_LENGTH:
        max_length = MAX_SEQUENCE_LENGTH

    # Fix sequence length to max value. Sequences shorter than the length are
    # padded in the beginning and sequences longer are truncated
    # at the beginning.
    x_train = sequence.pad_sequences(x_train, maxlen=max_length)
    x_val = sequence.pad_sequences(x_val, maxlen=max_length)
    x_test = sequence.pad_sequences(x_test, maxlen=max_length)
    return x_train, x_val, x_test, tokenizer.word_index
