import os
import pandas as pd
import re
import argparse

def standardize_delimiters(value):
    if isinstance(value, str):
        standardized_value = re.sub(r'[,\n\t\s]+', ';', value)
        return standardized_value.lower()
    return value

def main(filename):
    column_names = pd.read_csv(filename, nrows=0).columns.tolist()
    df = pd.read_csv(filename, skiprows=3, header=None)
    df.columns = column_names

    fields_to_standardize = ["Q22", "Q41"]
    for field in fields_to_standardize:
        df[field] = df[field].apply(standardize_delimiters)

    # Extract the directory and base filename
    directory, base_filename = os.path.split(filename)
    # Create a new filename with 'standardized_' prefix
    new_filename = f"standardized_{base_filename}"

    # If a directory was provided, join it back to the new filename
    if directory:
        new_filename = os.path.join(directory, new_filename)

    df.to_csv(new_filename, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clean and standardize CSV files.')
    parser.add_argument('filename', type=str, help='Name of the CSV file to be processed.')
    args = parser.parse_args()
    main(args.filename)
