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