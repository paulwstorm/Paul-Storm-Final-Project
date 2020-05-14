const mongoose = require('mongoose')
const Schema = mongoose.Schema

const PostSchema = new Schema({
    postContent: String,
    dateRetrieved: Date,
    postChars: String,
    postHeader: String,
    postImageUrl: String,
    postLevel: Number, 
    postPopularity: String,
    postSource: String,      
    postTokenizedContent: Array,
    postUrl: String,
    postUser: String,
    postUserImageUrl: String,
    postUserUrl: String,
    postWordsPos: Array
})

module.exports = mongoose.model("Post", PostSchema)

