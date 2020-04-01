const express = require('express')
const passport = require('passport')
const mongoose = require('mongoose')
const cors = require("cors");
const bodyParser = require('body-parser')
const Post = require("./models/post")
const Word = require("./models/word")
const User = require("./models/user")
const ObjectId = require('mongoose').Types.ObjectId
const querySring = require('querystring')

const LocalStrategy = require('passport-local').Strategy;

const app = express()

mongoose.connect('mongodb://localhost/weiboClozed')


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

passport.use('login', new LocalStrategy ((username, password, done) => {

  const authenticated = username === "username" && password === "password";

  if (authenticated) {
    let user = new user()

    let date = new Date ()
    let userName = `user${date.getSeconds()}${date.getMilliseconds()}`

    user.userName = userName
    user.userPassword = "12345"

    
    userLevel = 1,
    user.userClozes = []
    user.userDictionary = [],
    dateCreated = date

    user.save()

    return done(null, { myUser:nameName, myID: 1234 });
  } else {
    return done(null, false);
  }
}));

app.post('/login', passport.authenticate('login', {
  successRedirect: 'http://localhost:3000/selectLevel',
  failureRedirect: 'http://localhost:3000/login',
  session: false
}));

app.get("/posts", (req, res) => {
    Post.find({}).exec((err, posts) => {
      if (err) {
        res.writeHead(500)
        res.send(err)
      } else {
        res.send(posts)
      }
    })
})

app.get("/clozes/newCloze", async (req, res) => {

  Post.estimatedDocumentCount().exec((err, count) => {
    let startIndex = Math.floor(Math.random() * count)

    if ( startIndex > 50) {
      startIndex -= 50
    }

    Post.find({}).limit(50).skip(startIndex).exec((err, posts) => {
      Word.estimatedDocumentCount().exec((err, wordCount) => {
        let wordStartIndex = Math.floor(Math.random() * wordCount)

        if ( startIndex > 150) {
          startIndex -= 150
        }

        Word.find({}).limit(150).skip(wordStartIndex).exec((err, words) => {
          let clozedPosts = []
          let count = 0
          posts.forEach((post) => {
            let clozedPost = []
            let toRemove = Math.floor(Math.random() * post.postWordsPos.length)
            let removedWord = post.postWordsPos[toRemove]
            let clozedPostContent = post.postContent.replace(removedWord[0], "____") 

            replacementWords = []
            replacementWords.push(words[count].word)
            replacementWords.push(words[count + 1].word)
            replacementWords.push(words[count + 2].word)

            clozedPost.push(clozedPostContent)
            clozedPost.push(removedWord)
            clozedPost.push(replacementWords)

            clozedPosts.push(clozedPost)

            count += 3
          })

          res.send({posts, clozedPosts})
        })
      })
    })
  })
})

app.post("/post", (req, res) => {
  let post = new Post()

  post.save((err, post) => {
    if (err) {
      res.writeHead(500)
      res.send(err)
    } else {
      res.send("Post saved")
    }
  })
})

app.listen(5005, () => {
    console.log("Server listening on port 5005")
})