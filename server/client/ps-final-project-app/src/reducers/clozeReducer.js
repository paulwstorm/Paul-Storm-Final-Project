import { GET_POST_CLOZES } from "../actions/index.js"

export default function(state = [], action) {
    switch (action.type) {
        case GET_POST_CLOZES:
            let newState = []
            newState = action.payload.data
            return newState
        default:
            return state
    }
}