import { WORD_SEARCH } from "../actions/index.js"

export default function(state = [], action) {
    switch(action.type) {
        case WORD_SEARCH:
            state = action.payload.data
            return state
        default:
            return state
    }
}