import pandas as pd

def excel_to_python_object(file_path):
    try:
        # Read the Excel file into a pandas DataFrame
        excel_data = pd.read_excel(file_path)

        # Convert the DataFrame to a Python object (e.g., a list of dictionaries)
        python_object = excel_data.to_dict(orient='records')

        return python_object
    except Exception as e:
        print(f"Error converting Excel file to Python object: {e}")
        return None

# Example usage:
excel_file_path = 'path/to/your/excel_file.xlsx'
result = excel_to_python_object(excel_file_path)

if result is not None:
    print(result)
