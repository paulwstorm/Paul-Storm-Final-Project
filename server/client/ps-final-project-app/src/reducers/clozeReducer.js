import { GET_POST_CLOZES, REMOVE_GUESSED_CLOZE, GET_USER_CLOZES } from "../actions/index.js"

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
            console.log(newState.clozedPosts[9])
            if (newState.clozedPosts == undefined) {
                newState = []
                return newState
            } else {
                for (var i = 0; i < newState.posts.length; i ++) {
                    newState.posts[i].postClozedTokenizedContent = newState.clozedPosts[i][0]
                    let multipleChoiceWords = newState.clozedPosts[i][2]
                    multipleChoiceWords.push(newState.clozedPosts[i][1][0])
                    let removedWord = newState.clozedPosts[i][1]
                    newState.posts[i].removedWord = removedWord[0]
                    multipleChoiceWords = shuffle(multipleChoiceWords)
                    newState.posts[i].multipleChoiceWords = multipleChoiceWords
                }
                return newState.posts
            }
        case GET_USER_CLOZES:
                state = action.payload.data
                if (state.clozedPosts == undefined) {
                    state = []
                    return state
                } else {
                    for (var i = 0; i < state.posts.length; i ++) {
                        state.posts[i].postClozedTokenizedContent = state.clozedPosts[i][0]
                        let removedWord = state.clozedPosts[i][1]
                        let multipleChoiceWords = state.clozedPosts[i][2]
                        multipleChoiceWords.push(state.clozedPosts[i][1][0])
                        state.posts[i].removedWord = removedWord[0]
                        multipleChoiceWords = shuffle(multipleChoiceWords)
                        state.posts[i].multipleChoiceWords = multipleChoiceWords
                    }
                    return state.posts
                }
        case REMOVE_GUESSED_CLOZE:
            let stateClozeRemove = []
            stateClozeRemove = action.payload
            return stateClozeRemove
        default:
            return state
    }
}