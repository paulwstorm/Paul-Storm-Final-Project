const mongoose = require('mongoose')
const Schema = mongoose.Schema

const WordSchema = new Schema({
    word: String,
    level: Number,
    posTag: String
})

module.exports = mongoose.model("Word", WordSchema)

