import { GET_POSTS } from "../actions/index.js"
import { array } from "prop-types";

function shuffle(a) {
    var j, x, i;
    for (i = a.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = a[i];
        a[i] = a[j];
        a[j] = x;
    }
    return a;
  }

export default function(state = [], action) {
    switch (action.type) {
        case GET_POSTS:
            console.log("in postsReducer: ", action)
            state = []
            state = action.payload.data
            state = shuffle(state)
            return state
        default:
            console.log("in postsReducer: ", action)
            return state
    }
}