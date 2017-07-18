import numpy as np

def extract_array(path):
    """ Since the experiment data is
    tuple with its string 'tag' such as
        - label: ('label', ndarray)
        - eeg: ('eeg', ndarray)
    extract only ndarray and return them.
    """

    label, eeg = np.load(path).items()
    return label[1], eeg[1]

def combine_data(path):
    # initialize
    data = None
    for p in path:
        label, eeg = extract_array(p)
        if data is None:
            labels, data = label, eeg
        else:
            data = np.concatenate((data, eeg), axis=0)
            labels = np.hstack([labels, label])
    return data, labels


class ParseData(object):
    """Preprocess target data

    - Put all data together
    - Split them into 'train' and 'test'

     Parameter
    --------------------------
    data_paths: list of paths of experiment data

     Attribute
    --------------------------
    train_data: eeg signal of train data
    train_label: labels of train data
    test_data: eeg signal of test data
    test_label: labels of test data
    """

    def __init__(self, data_paths):
        train_data, train_label, test_data, test_label \
            = self.__parse(data_paths)

        self.train_data = train_data
        self.train_label = train_label
        self.test_data = test_data
        self.test_label = test_label

    def __parse(self, data_paths):
        # split 'test' and 'train'
        path_test = []
        path_train = []
        for d_ in data_paths:
            if 'test' in d_:
                path_test.append(d_)
            elif 'train' in d_:
                path_train.append(d_)
        # modify
        train_data, train_label = combine_data(path_train)
        test_data, test_label = combine_data(path_test)
        return train_data, train_label, test_data, test_label
