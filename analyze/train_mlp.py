import explore_data
import build_model
import ngram
import tensorflow as tf
import matplotlib.pyplot as plt

LEARNING_RATE = 1e-3
EPOCHS = 1000
BATCH_SIZE = 128
LAYERS = 2
UNITS = 64
DROPOUT_RATE = 0.5  # 0.2 ~ 0.5


def train_mlp_model(data,
                    learning_rate=LEARNING_RATE,
                    epochs=EPOCHS,
                    batch_size=BATCH_SIZE,
                    layers=LAYERS,
                    units=UNITS,
                    dropout_rate=DROPOUT_RATE):
    """Trains n-gram model on the given dataset.

    # Arguments
        data: tuples of training and test texts and labels.
        learning_rate: float, learning rate for training model.
        epochs: int, number of epochs.
        batch_size: int, number of samples per batch.
        layers: int, number of `Dense` layers in the model.
        units: int, output dimension of Dense layers in the model.
        dropout_rate: float: percentage of input to drop at Dropout layers.

    # Raises
        ValueError: If validation data has label values which were not seen
            in the training data.
    """
    (train_texts, train_labels), (test_texts, test_labels) = data

    # Verify that validation labels are in the same range as training labels.
    num_classes = explore_data.get_num_classes(train_labels)
    unexpected_labels = [v for v in test_labels if v not in range(num_classes)]
    if len(unexpected_labels):
        raise ValueError('Unexpected label values found in the validation set:'
                         ' {unexpected_labels}. Please make sure that the '
                         'labels in the validation set are in the same range '
                         'as training labels.'.format(
            unexpected_labels=unexpected_labels))

    # divide Cross Validation Set
    print('Divide cross validation set')
    total_len = len(train_labels)
    train_len = int(total_len * 3 / 4)
    val_texts = train_texts[train_len:]
    val_labels = train_labels[train_len:]
    train_texts = train_texts[:train_len]
    train_labels = train_labels[:train_len]

    # Vectorize texts.
    print('Vectorizing...')
    x_train, x_val, x_test = ngram.vectorize(train_texts, train_labels, val_texts, test_texts)
    # Create model instance.
    model = build_model.mlp_model(layers=layers,
                                  units=units,
                                  dropout_rate=dropout_rate,
                                  input_shape=x_train.shape[1:],  # shape : (row, column) / shape[1:] : (column)
                                  num_classes=num_classes)

    optimizer = tf.keras.optimizers.Adam(lr=learning_rate)
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['acc'])

    # Create callback for early stopping on validation loss. If the loss does
    # not decrease in two consecutive tries, stop training.
    callbacks = [tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=10)]

    # Train and validate model.
    history = model.fit(
        x_train,
        train_labels,
        epochs=epochs,
        callbacks=callbacks,
        validation_data=(x_val, val_labels),
        verbose=2,  # Logs once per epoch.
        batch_size=batch_size)

    history = history.history
    print_history(history)

    accuracy = model.evaluate(x_test, test_labels, batch_size=batch_size)
    print("\n%s : %.2f%%" % (model.metrics_names[1], accuracy[1] * 100))
    plot_history(history)

    # Save model.
    # model.save('mlp_model.h5')
    # return history['val_acc'][-1], history['val_loss'][-1]


def print_history(history):
    print('Validation accuracy: {acc}, loss: {loss}'.format(
        acc=history['val_acc'][-1], loss=history['val_loss'][-1]))


def plot_history(history):
    fit, loss_ax = plt.subplots()
    acc_ax = loss_ax.twinx()
    loss_ax.plot(history['loss'], 'y', label='train loss')
    loss_ax.plot(history['val_loss'], 'r', label='val loss')
    acc_ax.plot(history['acc'], 'b', label='train acc')
    acc_ax.plot(history['val_acc'], 'g', label='val acc')
    loss_ax.set_xlabel('epoch')
    loss_ax.set_ylabel('loss')
    acc_ax.set_ylabel('accuracy')
    loss_ax.legend(loc='upper left')
    acc_ax.legend(loc='lower left')
    plt.show()


if __name__ == '__main__':
    dataset = explore_data.load_dataset()
    train_mlp_model(dataset)
