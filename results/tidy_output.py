import re
import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter

def find_csv_files(directory):
    """
    Finds all CSV files in the specified directory and its subdirectories.
    
    Args:
        directory (str): The path to the directory to search.
        
    Returns:
        list: A list of strings representing the paths to the CSV files.
    """
    csv_files = []
    for file_path in Path(directory).rglob('*.csv'):
        if file_path.is_file():
            csv_files.append(str(file_path))
    return csv_files

root = Path.cwd()
all_csv_files = find_csv_files(root)
counter = Counter()
for csv_file in all_csv_files:
    df = pd.read_csv(csv_file)
    df_filtered = df.filter(like='output', axis=1)
    for i in df_filtered.index:
        for j in df_filtered.columns:
            text = df_filtered.loc[i, j]
            if text is not np.nan:
                text = re.sub('â€¢ ', '- ', text)
                text = re.sub(r'Â\\xa0', ' ', text)
                text = re.sub('â€“', '-', text)
                text = re.sub('Â°', '°', text)
                text = re.sub('â€™', '\'', text)
                text = re.sub('â‰¥', '>=', text)
                text = re.sub('Ã¶', 'o', text)
                text = re.sub('Ã©', 'e', text)
                df_filtered.loc[i, j] = text
    df.loc[:, df_filtered.columns] = df_filtered
    df.to_csv(csv_file)