import pandas as pd
import json
import sys

def makefile(file: list):
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
    df.to_excel('schedule.xlsx', index=False)

    print("Dados salvos em schedule.xlsx")

argumentos = sys.argv
makefile(argumentos)