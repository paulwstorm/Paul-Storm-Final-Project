import { GET_POSTS } from "../actions/index.js"

export default function(state = [], action) {
    switch (action.type) {
        case GET_POSTS:
            state = []
            state = action.payload.data
            console.log(action)
            return state
        default:
            return state
    }
}