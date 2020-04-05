import { NEW_SEARCH_TERM } from "../actions/index.js"

export default function(state = "", action) {
    switch(action.type) {
        case NEW_SEARCH_TERM:
            state = action.payload
            return state
        default:
            return state
    }
}