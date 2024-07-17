import pandas as pd
import json
import sys
from termcolor import colored
import os
import pathlib
from datetime import datetime


def makefile(file: list):
    
    path_save = os.path.join(pathlib.Path.home(), "Desktop",  f'{datetime.now().strftime("%d-%m-%Y %H-%M-%S")}.xlsx')
    # Load the JSON file
    file_path = file[1]
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Convert the JSON data to a DataFrame
    def json_to_dataframe(data):
        records = []
        for vara, dates in data.items():
            for date, entries in dates.items():
                for entry in entries:
                    record = {'Vara': vara, 'Data': date}
                    record.update(entry)
                    records.append(record)
        df = pd.DataFrame(records)
        return df

    df = json_to_dataframe(data)

    # Salvar o DataFrame em uma planilha Excel
    df.to_excel(path_save, index=False)

    print(colored("Dados salvos em schedule.xlsx", "green", attrs=["bold"]))
    os.system("pause")

argumentos = sys.argv
makefile(argumentos)