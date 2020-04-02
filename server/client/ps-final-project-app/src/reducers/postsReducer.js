import { GET_POSTS } from "../actions/index.js"

export default function(state = [], action) {
    switch (action.type) {
        case GET_POSTS:
            console.log(action.payload.data)
            return action.payload.data
        default:
            return state
    }
}