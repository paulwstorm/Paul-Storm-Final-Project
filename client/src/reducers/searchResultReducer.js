import { WORD_SEARCH } from "../actions/index.js"

export default function(state = [], action) {
    switch(action.type) {
        case WORD_SEARCH:
            let wordList = action.payload.data

            wordList = wordList.sort((a, b) => {
                    if (a.wordRank > b.wordRank) {
                        return 1
                    } else {
                        return -1
                    }
                })
            wordList = wordList.slice(0,10)
            console.log("searchResultReducer", wordList)
            state = wordList
            return state
        default:
            return state
    }
}