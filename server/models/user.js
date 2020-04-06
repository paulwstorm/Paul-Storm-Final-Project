const mongoose = require("mongoose")
const Schema = mongoose.Schema

const UserSchema = new Schema({
    userName: String,
    userPassword: String,
    userLevel: Number,
    userClozes: Array,
    userDictionary: Array,
    visited: Array,
    dateCreated: Date
})


module.exports = mongoose.model("User", UserSchema)