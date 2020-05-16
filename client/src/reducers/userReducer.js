import { GET_USER } from "../actions/index.js"

export default function(state = {}, action) {
    switch (action.type){ 
        case GET_USER:
            state = action.payload.data
            return state
        default:
            return state
    }
}