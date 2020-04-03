import { GET_POST_CLOZES, REMOVE_GUESSED_CLOZE } from "../actions/index.js"

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

export default function(state = [], action) {
    switch (action.type) {
        case GET_POST_CLOZES:
            let newState = []
            newState = action.payload.data
            for (var i = 0; i < newState.posts.length; i ++) {
                let unclozedPost = newState.posts[i].postContent
                newState.posts[i].unclozedPost = unclozedPost
                newState.posts[i].postContent = newState.clozedPosts[i][0]
                let removedWord = newState.clozedPosts[i][1]
                let multipleChoiceWords = newState.clozedPosts[i][2]
                multipleChoiceWords.push(newState.clozedPosts[i][1][0])
                newState.posts[i].removedWord = removedWord[0]
                multipleChoiceWords = shuffle(multipleChoiceWords)
                newState.posts[i].multipleChoiceWords = multipleChoiceWords
            }
            console.log(newState.posts)
            return newState.posts
        case REMOVE_GUESSED_CLOZE:
            let stateClozeRemove = []
            stateClozeRemove = action.payload
            console.log(action.payload)
            return stateClozeRemove
        default:
            return state
    }
}