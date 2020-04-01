const express = require('express')
const passport = require('passport')
const mongoose = require('mongoose')
const cors = require("cors");
const bodyParser = require('body-parser')
const Post = require("./models/post")
const Word = require("./models/word")
const User = require("./models/user")
const cookieSession = require('cookie-session')
const session = require("express-session")
const ObjectId = require('mongoose').Types.ObjectId
const querySring = require('querystring')

const LocalStrategy = require('passport-local').Strategy;

const app = express()

mongoose.connect('mongodb://localhost/weiboClozed')

app.use(cookieSession({
  name: 'session',
  keys: ['helloworld'],

  // Cookie Options
  maxAge: 24 * 60 * 60 * 1000 // 24 hours
}))

app.use(passport.initialize());
app.use(passport.session());

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
  const authenticated = (username === "1" || username === "2" || username === "3" || username === "4" || username === "5" || username === "6") && password === "password";

  let user = new User()

  let date = new Date ()
  let userName = `user${date.getSeconds()}${date.getMilliseconds()}`

  user.userName = userName
  user.userPassword = "12345"

  
  userLevel = 1,
  user.userClozes = []
  user.userDictionary = [],
  dateCreated = date

  user.save()

  if (authenticated) {
    return done(null, { myUser:userName, myID: 1234 });
  } else {
    return done(null, false);
  }
}));

passport.serializeUser((user, done) => {
  console.log(user);
  done(null, user);
});

passport.deserializeUser((user, done) => {
  console.log(user);
  done(null, user);
});

function checkAuthentication(req,res,next){
  console.log(req.isAuthenticated())
  if(req.isAuthenticated()){
      //req.isAuthenticated() will return true if user is logged in
      next();
  } else{
      res.redirect("/");
  }
}

// app.post('/login', function(req, res, next) {
//   passport.authenticate('login', function(err, user, info) {
//     if (err) { return next(err); }
//     if (!user) { return res.redirect('http://localhost:3000/'); }
//     req.login(user, function(err) {
//       if (err) { return next(err); }
//       return res.redirect('http://localhost:3000/posts');
//     });
//   })(req, res, next);
// });

app.post('/login', passport.authenticate('login', {
  successRedirect: 'http://localhost:3000/posts',
  failureRedirect: 'http://localhost:3000/'
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

app.get("/test", checkAuthentication, (res, req) => {
  res.send("Success")
})

app.listen(5005, () => {
    console.log("Server listening on port 5005")
})