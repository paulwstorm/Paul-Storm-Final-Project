const express = require('express')
const passport = require('passport')
const mongoose = require('mongoose')
const cors = require("cors");
const bodyParser = require('body-parser')
const Post = require("./models/post")
const Word = require("./models/word")
const User = require("./models/user")
const Dictionary = require("./models/dictionary")
const cookieSession = require('cookie-session')
const session = require("express-session")
const ObjectId = require('mongoose').Types.ObjectId
const querySring = require('querystring')

const port = process.env.PORT || 5005;

const LocalStrategy = require('passport-local').Strategy;

const app = express()

//Adding
// mongoose.connect('mongodb://localhost/weiboClozed')
mongoose.connect('mongodb://paulStorm:w31b020200403@ds231387.mlab.com:31387/heroku_1xm0ffdd')


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

function shuffle(a) {
  var j, x, i;
  for (i = a.length - 1; i > 0; i--) {
      j = Math.floor(Math.random() * (i + 1));
      x = a[i];
      a[i] = a[j];
      a[j] = x;
  }
  return a;
}

app.use(
  cors({
    origin: "http://localhost:3000", // allow to server to accept request from different origin
    methods: "GET,HEAD,PUT,PATCH,POST,DELETE",
    credentials: true // allow session cookie from browser to pass through
  })
);

passport.use('login', new LocalStrategy ((username, password, done) => {
  const authenticated = (username === "1" || username === "2" || username === "3" || username === "4" || username === "5" || username === "6") && password === "password";

  let user = new User()

  let date = new Date ()
  let userName = `user${date.getSeconds()}${date.getMilliseconds()}`

  user.userName = userName
  user.userPassword = "12345"

  
  user.userLevel = parseInt(username),
  user.userClozes = []
  user.userDictionary = [],
  user.visited = [],
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
  console.log(req.url)
  if(req.isAuthenticated()){
      //req.isAuthenticated() will return true if user is logged in
      next();
  } else{
      res.redirect("frontend/");
  }
}

app.get("/backend/wordsearch", (req,res) => {
  if (req.query.lang == "Chinese") {
    Dictionary
      .find({simplified: req.query.query})
      .limit(10)
      .exec((err, result) => {
        if (err) {
          res.send(err)
        } else {
          res.send(result)
        }
    })
  } else if (req.query.lang == "English") {
    const query = (req.query.query).toLowerCase()
    const regExQuery = new RegExp(`/${query}/`, "i")
  
    Dictionary
      .find({english: { $regex: query}})
      .limit(10)
      .exec((err, result) => {
        if (err) {
          res.send(err)
        } else {
          res.send(result)
        }
      })
  }
})

app.get("/backend/userinfo", (req, res) => {
  User.find({userName: req.user.myUser}).exec((err, user) => {
    if (err) {
      res.send(err)
    } else {
      res.send(user[0])
    }
  })
})

app.post("/backend/userinfo", (req, res) => {
  User.find({userName: req.user.myUser}).exec((err, user) => {
    if (err) {
      res.send(err)
    } else {
      user[0].visited.push(req.body.room)
      user[0].save((err, user) => {
        if (err) {
          res.send(err)
        } else {
          res.send(user[0])
        }
      })
    }
  })
})

app.post('/backend/login', passport.authenticate('login', {
  successRedirect: '/posts',
  failureRedirect: '/'
}));

app.get("/backend/posts", checkAuthentication, (req, res) => {
  let viewNum = parseInt(req.query.viewNum)
  let startPost = parseInt(req.query.startPost)
  console.log("154")
  console.log(req.user.myUser)
  User.find({userName: req.user.myUser}).exec((err, user) => {
    console.log("156: ", user)
    if (err) {
      res.send(err)
    } else {
      Post.find({ postLevel: { $lte: user[0].userLevel }}).sort({dateRetrieved: -1}).skip(startPost).limit(viewNum).exec((err, posts) => {
        console.log("163", posts)
        if (err) {
          res.send(err)
        } else {
          res.send(posts)
        }
      })
    }  
  })
})


app.get("/backend/user/words", checkAuthentication, (req, res) => {
  let viewNum = parseInt(req.query.viewNum)
  let startPost = parseInt(req.query.startPost)

  User.find({userName: req.user.myUser}).exec((err, user) => {
    if (err) {
      res.send(err)
    } else {
      let words = []
      if (user[0].userDictionary.length > (startPost + viewNum)) {
        words = user[0].userDictionary.slice(startPost, viewNum)
      } else if (user[0].userDictionary.length > startPost) {
        words = user[0].userDictionary.slice(startPost,)
      } else {
        words = user[0].userDictionary
      }

      res.send(words)
    }  
  })
})

app.get("/backend/posts/clozes",  (req, res) => {
  let viewNum = parseInt(req.query.viewNum)
  let startPost = parseInt(req.query.startPost)

  User.find({userName: req.user.myUser}).exec((err, user) => {
    if (err) {
      res.send(err)
    } else {
      Post.find({ postLevel: { $lte: user[0].userLevel }}).sort({"dateRetrieved":-1}).skip(startPost).limit(viewNum).exec((err, posts) => {
        Word.find({ level:{ $lte: user[0].userLevel }}).countDocuments().exec((err, wordCount) => {
          let wordStartIndex = Math.floor(Math.random() * (wordCount-(viewNum*3)))
          Word.find({ level:{ $lte: user[0].userLevel }}).limit((viewNum*3)).skip(wordStartIndex).exec((err, words) => {
            console.log("line 226")
            let clozedPosts = []
            let count = 0
            words = shuffle(words)
            posts.forEach((post) => {
              let clozedPost = []
              let toRemove = Math.floor(Math.random() * post.postWordsPos.length)
              let removedWord = post.postWordsPos[toRemove]
              let clozedPostTokenizedContent = []
              post.postTokenizedContent.forEach(wordArray => {
                let clozedTokenizedWord = []
                if (wordArray[0] == removedWord[0]) {
                  clozedTokenizedWord.push("[------]")
                  clozedTokenizedWord.push(wordArray[1])
                } else {
                  clozedTokenizedWord.push(wordArray[0])
                  clozedTokenizedWord.push(wordArray[1])
                }

                clozedPostTokenizedContent.push(clozedTokenizedWord)
              })

              replacementWords = []
              replacementWords.push(words[count].word)
              replacementWords.push(words[count + 1].word)
              replacementWords.push(words[count + 2].word)

              clozedPost.push(clozedPostTokenizedContent)
              clozedPost.push(removedWord)
              clozedPost.push(replacementWords)

              clozedPosts.push(clozedPost)

              count += 3
            })
            console.log("line 264")
            res.send({posts, clozedPosts})
          })
        })
      })
    }
  })
})

app.get("/backend/user/clozes",  (req, res) => {
  let viewNum = parseInt(req.query.viewNum)
  let startPost = parseInt(req.query.startPost)

  User.find({userName: req.user.myUser}).lean().exec((err, user) => {
    if (err) {
      res.send(err)
    } else {
      if (user[0].userClozes.length > 0) {
        Word.find({ level:{ $lte: user[0].userLevel }}).countDocuments().exec((err, wordCount) => {
          let wordStartIndex = Math.floor(Math.random() * (wordCount-(user[0].userClozes.length*3)))

          Word.find({ level:{ $lte: user[0].userLevel }}).limit((user[0].userClozes.length*3)).skip(wordStartIndex).exec((err, words) => {
            let posts = []
            if (req.query.view == "incorrect") {
              posts = user[0].userClozes.filter(cloze => {
                return cloze.lastAttempt == "incorrect"
              }) 
            } else {
              posts = user[0].userClozes
            }    

            let clozedPosts = []
            let count = 0
            words = shuffle(words)
            posts.forEach((cloze) => {
              let clozedPost = []
              let toRemove = Math.floor(Math.random() * cloze.postWordsPos.length)
              let removedWord = cloze.postWordsPos[toRemove]
              let clozedPostTokenizedContent = []
              cloze.postTokenizedContent.forEach(wordArray => {
                let clozedTokenizedWord = []
                if (wordArray[0] == removedWord[0]) {
                  clozedTokenizedWord.push("[------]")
                  clozedTokenizedWord.push(wordArray[1])
                } else {
                  clozedTokenizedWord.push(wordArray[0])
                  clozedTokenizedWord.push(wordArray[1])
                }

                clozedPostTokenizedContent.push(clozedTokenizedWord)
              })

              replacementWords = []
              replacementWords.push(words[count].word)
              replacementWords.push(words[count + 1].word)
              replacementWords.push(words[count + 2].word)

              clozedPost.push(clozedPostTokenizedContent)
              clozedPost.push(removedWord)
              clozedPost.push(replacementWords)

              clozedPosts.push(clozedPost)

              count += 3
            })

            res.send({posts, clozedPosts})
          })
        })
      } else {
        res.send({})
      }  
    }
  })
})

app.post("/backend/posts/clozes", (req, res) => {
  let markedCloze = req.body

  User.findOne({userName: req.user.myUser}).exec((err, user) => {
    if (err) {
      res.send(err)
    } else {
      updatedUserClozes = []
      updatedUserClozes = user.userClozes.filter(cloze => {
        return !(cloze.postContent == markedCloze.postContent)
      })
      updatedUserClozes.push(markedCloze)
      user.userClozes = updatedUserClozes
      user.save((err) => {
        if (err) {
          res.send(err)
        } else {
          res.send("Cloze added to userClozes")
        }
      })
    }
  })
})

app.post("/backend/addWordToDict", (req, res) => {
  let word = req.body
  User.findOne({userName: req.user.myUser}).exec((err, user) => {
    if (err) {
      res.send(err)
    } else {
      user.userDictionary.push(word)
      user.save((err, user) => {
        if (err) {
          res.send(err)
        } else {
          console.log(user)
          res.send("Word added to userDictionary")
        }
      })
    }
  })
})

app.get("/backend/clozes/newCloze", (req, res) => {

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
            let clozedPostContent = post.postTokenizedContent.map(wordArray => {
              if (wordArray[0] == removedWord) {
                wordArray[0] = "____"
              }
              return wordArray
            })

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

if (process.env.NODE_ENV === 'production') {
  // Express will serve up production assets
  // like our main.js file, or main.css file!
  app.use(express.static('client/build'));

  // Express will serve up the index.html file
  // if it doesn't recognize the route
  const path = require('path');

  app.get('*', (req, res, next) => {
    res.sendFile(path.join(__dirname, 'client', 'build', 'index.html'));
  });
}

app.listen(port, () => {
    console.log("Server listening on port", port)
})