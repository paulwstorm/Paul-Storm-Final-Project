import { INCREMENT_POST_COUNT, DECREMENT_POST_COUNT } from "../actions/index.js"

export default function(state = 0, action) {
    switch (action.type) {
        case INCREMENT_POST_COUNT:
            let incrementState = state + action.payload
            return incrementState
        case  DECREMENT_POST_COUNT:
            let decrementState = state - action.payload
            return decrementState
        default:
            return state
    }

}

