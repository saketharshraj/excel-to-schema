
import { Application } from '../declarations';
import { Model, Mongoose } from 'mongoose';

export default function (app: Application): Model<any> {
    const modelName = 'product';
    const mongooseClient: Mongoose = app.get('mongooseClient');
    const { Schema } = mongooseClient;
    const { ObjectId } = Schema.Types;
    const schema = new Schema(
        {
            name: {
                type: String,
                required: true,
            },
            createdBy: {
                type: ObjectId,
                required: true,
                ref: 'user',
            },
            avatar: {
                type: String,
                required: true,
            },
            description: {
                type: String,
            },
            originalPrice: {
                type: Number,
                required: true,
            },
            sellingPrice: {
                type: Number,
                required: true,
            },
            ongoingSale: {
                type: ObjectId,
                ref: 'offerSale',
            },
            categories: {
                type: [String],
            },
            orderCount: {
                type: Number,
            },
            status: {
                type: Number,
                default: 1,
                enum: [
                    1, // Active,
                    0, // disabled,
                    -1, // Deleted,
                ],
            },
            quantity: {
                type: Number,
                required: true,
            },
            productCode: {
                type: String,
                required: true,
            },
            averageRating: {
                type: Number,
            },
            stock: {
                type: Number,
            },
        },
        {
            timestamps: true,
        },
    );
    // This is necessary to avoid model compilation errors in watch mode
    // see https://mongoosejs.com/docs/api/connection.html#connection_Connection-deleteModel
    if (mongooseClient.modelNames().includes(modelName)) {
        (mongooseClient as any).deleteModel(modelName);
    }
    return mongooseClient.model<any>(modelName, schema);
}
