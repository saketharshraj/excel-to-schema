import pandas as pd


def fix_model_name(s):
    return s


def fix_key(s):
    s = s.split()[0]
    s = s[0].lower() + s[1:]
    return s


def fix_types(s):

    s = s.lower().strip()
    if s == 'string':
        return 'String'
    elif s == 'number':
        return 'Number'
    elif s == 'objectid':
        return 'ObjectId'
    elif s == 'date':
        return 'Date'
    elif s in ('array(strings)', '[strings]', '[string]', 'array[string]'):
        return '[String]'
    elif s in ('array(objectid)', '[objectid]'):
        return '[ObjectId]'


def fix_required(s):
    s = str(s).strip().lower()
    if s.lower() == 'true':
        return 1
    else:
        return 0


def fix_ref(s):
    s = s.strip()
    if s in ('-', '', 'null'):
        return ''
    else:
        return s


def fix_default(s, kt):
    if s in ('-', '', 'null'):
        return ''
    else:
        if kt == 'Number':
            return int(s)
        return s


def fix_enum(s):
    if s in ('-', '', 'null'):
        return ''
    s = s.split()
    final_enum = f"""
                enum: ["""
    for i in range(0, len(s), 2):
        final_enum += f"""
                    {s[i]}, // {s[i + 1]},"""
    final_enum += f"""
                ]"""

    return final_enum


if __name__ == '__main__':
    file = pd.ExcelFile('Data Model.xlsx')
    sheet_name = 'product'
    df = pd.read_excel(file, sheet_name=sheet_name)
    dfT = df.T
    schema = dfT.to_dict()
    model_name = fix_model_name(sheet_name)
    result = f"""
import {{ Application }} from '../declarations';
import {{ Model, Mongoose }} from 'mongoose';

export default function (app: Application): Model<any> {{
    const modelName = '{model_name}';
    const mongooseClient: Mongoose = app.get('mongooseClient');
    const {{ Schema }} = mongooseClient;
    const {{ ObjectId }} = Schema.Types;
    const schema = new Schema(
        {{"""
    for data_model in schema:
        data = schema[data_model]
        key = fix_key(data['key'])
        key_type = fix_types(data['type'])
        required = fix_required(data['required'])
        reference = fix_ref(data['ref'])
        default = fix_default(data['default'], key_type)
        enum = fix_enum(data['enum'])

        result += f"""
            {key}: {{
                type: {key_type},"""

        if required:
            result += f"""
                required: true,"""

        if reference:
            result += f"""
                ref: '{reference}',"""

        if default:
            result += f"""
                default: {default},"""

        if enum:
            result += f"""{enum},"""

        result += f"""
            }},"""

    result += f"""
        }},
        {{
            timestamps: true,
        }},
    );
    // This is necessary to avoid model compilation errors in watch mode
    // see https://mongoosejs.com/docs/api/connection.html#connection_Connection-deleteModel
    if (mongooseClient.modelNames().includes(modelName)) {{
        (mongooseClient as any).deleteModel(modelName);
    }}
    return mongooseClient.model<any>(modelName, schema);
}}
"""
    with open(f'{model_name}.model.ts', 'w') as file:
        file.writelines(result)
