const express = require('express')
const passport = require('passport')
const mongoose = require('mongoose')
const cors = require("cors");
const User = require('./models/user')
const bodyParser = require('body-parser')
const ObjectId = require('mongoose').Types.ObjectId
const querySring = require('querystring')

const app = express()

mongoose.connect('mongodb://localhost/homebase')


app.use(bodyParser.json())
app.use(bodyParser.urlencoded({
  extended: true
}))

if (process.env.NODE_ENV === 'production') {
  // Express will serve up production assets
  // like our main.js file, or main.css file!
  app.use(express.static('client/build'));

  // Express will serve up the index.html file
  // if it doesn't recognize the route
  const path = require('path');
  app.get('*', (req, res) => {
    res.sendFile(path.resolve(__dirname, 'client', 'build', 'index.html'));
  });
}

