import os
import zipfile
import Levenshtein as lev
import pandas as pd

# Auxiliary Functions

def create_folder(path):
    if not os.path.exists(path):
        os.mkdir(path)

def unzip(folder, filepath):
    with zipfile.ZipFile(filepath, 'r') as zip_ref:
        zip_ref.extractall(folder)

def int_to_code(x: int):
    return f'0{x}' if x<10 else str(x)

def matrix_lev(list1, list2):
    """
    Create a matrix with the leveshteins distances compare 1 with 1 between two lists. 
    """
    mlev = pd.DataFrame(index = list1, columns = list2)
    for i in mlev.index:
        for j in mlev.columns:
            mlev.loc[i, j] = lev.distance(i, j)
    return mlev
