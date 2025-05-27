from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logging import logging
import yaml
import os, sys
import numpy as np
import dill
import pickle


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    
    Args:
        file_path (str): Path to the YAML file.
        
    Returns:
        dict: Content of the YAML file.
    """
    try:
        with open(file_path, 'rb') as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def write_yaml_file(file_path: str, content: dict, replace: bool = False) -> None:
    """
    Writes a dictionary to a YAML file.
    
    Args:
        file_path (str): Path to the YAML file.
        content (dict): Data to write to the file.
        replace (bool): If True, replaces the file if it exists.
    """
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Saves a NumPy array to a file.
    
    Args:
        file_path (str): Path to the file where the array will be saved.
        array (np.array): NumPy array to save.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file:
            np.save(file, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_object(file_path: str, obj: object):
    """
    Saves an object to a file using dill.
    
    Args:
        file_path (str): Path to the file where the object will be saved.
        obj (object): Object to save.
    """
    try:
        logging.info(f"Entering the save_object function of main_utils")
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
        logging.info(f"Exiting the save_object function of main_utils")
    except Exception as e:
        raise NetworkSecurityException(e, sys)