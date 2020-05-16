import { WORD_SEARCH } from "../actions/index.js"

export default function(state = [], action) {
    switch(action.type) {
        case WORD_SEARCH:
            console.log("searchResultReducer", action.payload.data)
            let wordList = action.payload.data

            wordList.sort((a, b) => {
                if (a.wordRank < b.wordRank) {
                    return 1
                } else {
                    return -1
                }
            })
            wordList = wordList.slice(0,10)
            state = wordList
            return state
        default:
            return state
    }
}