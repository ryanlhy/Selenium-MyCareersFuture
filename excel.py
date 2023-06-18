import pandas as pd

def export_to_excel(data, filename):
    df = pd.DataFrame(data)
    df.to_excel(f"{filename}",index=False)
    print("Exported to excel")

def combine_old_and_new_data(excel_file_path, new_rows, column_name):
    try:
        existing_data = pd.read_excel(excel_file_path) 
        # Process the data or perform actions on the DataFrame
        print(f"file '{excel_file_path}' found.")
        print('Existing data...........')
        print(existing_data)
        print('strip extra whitespaces..........')
        existing_data.columns = existing_data.columns.str.strip()
        print(existing_data)
    except FileNotFoundError:
        print(f"File '{excel_file_path}' not found. Creating and exporting to {excel_file_path}.")
        return  # Exit the function if file not found

    print("Combining old and new data")
    # Create a new DataFrame from the new rows
    new_data = pd.DataFrame(new_rows)
    print("new data...........")
    print(new_data)
    # Concatenate the new DataFrame with the existing DataFrame
    combined_data = pd.concat([new_data, existing_data], ignore_index=True)
    print("combined data...........")
    print(combined_data)
    # Drop duplicates based on the 'href' column
    combined_data.drop_duplicates(subset=column_name, inplace=True)
    print("combined data without duplicates...........")
    print(combined_data)
    return combined_data

def extract_column_rows(excel_file_path, header_value, start_row=0):
    # initialize href column number
    col_num = 0

    try:
        # Read the Excel file into a pandas DataFrame
        data_frame = pd.read_excel(excel_file_path)

        # Extract the column names from the DataFrame
        column_names = data_frame.columns.tolist()

        # Find the 'href' column number
        col_num = column_names.index(header_value)
        print(f"Column {header_value} found! col_num: {col_num}")

        # Extract the values under the 'header_value' column from the specified row onwards
        header_value_list = data_frame.iloc[start_row:, col_num].tolist()
        return header_value_list

    except ValueError:
        print(f"Column {header_value} not found.")


def get_last_column(excel_file_path):
    # Read the Excel file into a pandas DataFrame
    data_frame = pd.read_excel(excel_file_path)

    # Get the column names from the DataFrame
    column_names = data_frame.columns.tolist()

    # Get the index of the last column
    last_column_index = len(column_names) - 1
    return last_column_index

def find_first_blank_row(excel_file_path, column_name):
    # Read the Excel file into a pandas DataFrame
    data_frame = pd.read_excel(excel_file_path, engine='openpyxl')

    # Use isnull() to get a Boolean Series indicating whether each value in the column is null
    null_values = data_frame[column_name].isnull()

    # Check if the column contains any null values
    if null_values.any():
        # If it does, find the first null value
        first_blank_row = null_values.idxmax()
    else:
        # If it doesn't, return None or another value
        first_blank_row = None  # Or another value

    return first_blank_row

def export_to_existing_excel(excel_file_path, data, start_row):
    # Read the Excel file into a pandas DataFrame
    data_frame = pd.read_excel(excel_file_path, engine='openpyxl')
    print("start exporting to excel..")
    
    # Insert the dictionary values into the DataFrame
    for i, row in enumerate(data):  # Iterate over the list of dictionaries
        for key, value in row.items():  # Iterate over each dictionary
            data_frame.loc[start_row + i, key] = value  # Assign the value to the corresponding cell in the DataFrame

    # Save the modified DataFrame to the Excel file
    data_frame.to_excel(excel_file_path, index=False)
    


# # Save the key-value pairs to a file
# with open('header_dict.txt', 'w') as file:
#     for key, value in header_dict.items():
#         file.write(f"Key: {key}, Value: {value}\n")

# print(extract_column_rows('output.xlsx', 'href'))
# my_dict = {
#     'job_description': ['value1', 'value2', 'value3', 'value4', 'value5'],
#     'keywords': ['value6', 'value7', 'value8', 'value9', 'value10'],
#     'relevance': ['value11', 'value12', 'value13', 'value14', 'value15']
# }

my_dict2 = [
    {'job_description': 'value1', 'keywords': 'value6', 'relevance': 'value11'}, 
    {'job_description': 'value2', 'keywords': 'value7', 'relevance': 'value12'}, 
    {'job_description': 'value3', 'keywords': 'value8', 'relevance': 'value13'}, 
    {'job_description': 'value4', 'keywords': 'value9', 'relevance': 'value14'}, 
    {'job_description': 'value5', 'keywords': 'value10', 'relevance': 'value15'}
]
# export_to_existing_excel('output2.xlsx', my_dict2, 0)
# print(find_first_blank_row('output.xlsx', 'job_description'))