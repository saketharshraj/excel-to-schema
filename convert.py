import helpers


def excel_to_schema(schema, model_name):
    result = f"""import {{ Application }} from '../declarations';
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
        key = helpers.fix_key(data['key'])
        key_type = helpers.fix_types(data['type'])
        required = helpers.fix_required(data['required'])
        reference = helpers.fix_ref(data['ref'])
        default = helpers.fix_default(data['default'], key_type)
        enum = helpers.fix_enum(data['enum'])

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

    return result
