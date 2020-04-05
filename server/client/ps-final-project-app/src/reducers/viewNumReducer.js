import { SET_VIEW_NUM } from "../actions/index"

export default function(state = 10, action) {
    switch (action.type) {
        case SET_VIEW_NUM:
            let newState = action.payload
        default:
            return state
    }
}