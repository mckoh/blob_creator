"""
Functions module of Blob Creator

Author: Michael Kohlegger
Date: 2021-09
"""

def dictionary_filter(dictionary, cols) -> dict:
    """Can be used to filter certain keys from a dict
    
    :param dictionary: The original dictionary
    :param cols: The searched columns
    :return: A filtered dictionary
    """
    return dict([(i, dictionary[i]) for i in dictionary if i in set(cols)])
