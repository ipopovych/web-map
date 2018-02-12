# Module for saving and loading Python objects


import pickle


def load_obj(name ):
    """
    Loads Python object from file.
    :param name: sting with the name of file to load object from.
    :return: python object from file
    """
    with open('data_obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


def save_obj(obj, name):
    """
    Saves Python object as file.
    :param obj: dict, list, etc.
    :param name: sting with the name of file to save object as.
    :return: None
    """
    with open('data_obj/' + name + '.pkl', 'wb+') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
        return None
