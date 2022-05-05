import pandas as pd
import convert
import helpers


def make_file(name, mode, data):
    with open(name, mode) as files:
        files.writelines(data)


if __name__ == '__main__':
    file = pd.ExcelFile('Data Model.xlsx')
    models = file.sheet_names
    for model in models:
        df = pd.read_excel(file, sheet_name=model)
        dfT = df.T
        schema = dfT.to_dict()
        model_name = helpers.fix_model_name(model)
        result = convert.excel_to_schema(schema, model_name)
        make_file(f'models/{model_name}.model.ts', 'w', result)
