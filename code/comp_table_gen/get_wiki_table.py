# NOTE: I did not end up using this & the wiki_data.json and instead just typed the data into excel.

import pandas as pd
import json


def save_dataframes_to_json(dfs_list, filename):
    """
    Save multiple DataFrames to a single JSON file.
    
    Parameters:
    - dfs_list (list): List of DataFrames.
    - filename (str): Name of the JSON file.
    """
    data = {}
    for idx, df in enumerate(dfs_list):
        data[f"DataFrame_{idx}"] = df.to_dict(orient='records')
    
    with open(filename, 'w') as file:
        json.dump(data, file)


# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/Comparison_of_source-code-hosting_facilities#Features"


# Extract tables from the Wikipedia page
tables = pd.read_html(url)

# Write to JSON file
save_dataframes_to_json(tables, 'wiki_data.json')
