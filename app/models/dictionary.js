const mongoose = require('mongoose')
const Schema = mongoose.Schema

const DictionarySchema = new Schema({
    english: String,
    pinyin: String,
    simplified: String,
    traditional: String,
    posTag: String,
    partOfSpeech: String
})

module.exports = mongoose.model("Dictionary", DictionarySchema)
