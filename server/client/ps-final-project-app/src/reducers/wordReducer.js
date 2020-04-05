import { GET_WORDS } from "../actions/index.js"

export default function(state = [], action) {
    switch (action.type) {
        case GET_WORDS:
            state = action.payload.data
            console.log(action.payload.data)
            return state
        default:
            return state
    }
}