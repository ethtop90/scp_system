import pandas as pd
import json
from pathlib import Path


base_path = Path(__file__).parent

base_url = "https://ymgfg.co.jp//wp-json/wp/v2/"

taxonomi_babai = {}
taxonomi_chintai = {}

def taxonomi_excel_handler(source, type):

    # Read the Excel file into a pandas DataFrame``
    # 賃貸 売買
    # sheet_name = "賃貸" if type == 'chintai' else "売買"
    xfile = pd.read_excel(source, sheet_name=type)
    json_data = xfile.to_json(orient='records')
    datas = json.loads(json_data)
    # print(json_data)
    # final_json_data = json.dumps(json.loads(json_data), ensure_ascii=False, default=str)
    # print(final_json_data)
    # return final_json_data
    keys = datas[0].keys()
    taxonomi_dic = {}
    for key in keys:
        taxonomi_dic[key] = []
        for data in datas:
            if data.get(key):
                taxonomi_dic[key].append(data.get(key))
                
     # Define the file name based on the 'type' parameter
    file_name = f"{type}.json"
    # Create the full path for the file
    file_path = base_path / '../base_data/' / str('taxonomi_' + file_name)
    
    # Write the dictionary to a JSON file
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(taxonomi_dic, json_file, ensure_ascii=False, indent=4)
        
    return taxonomi_dic
    
taxonomi_chintai = taxonomi_excel_handler(base_path / '../base_data/yamaguchi_taxonomi.xlsx', 'chintai')
taxonomi_babai = taxonomi_excel_handler(base_path / '../base_data/yamaguchi_taxonomi.xlsx', 'baibai')